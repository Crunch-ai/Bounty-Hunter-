import os
import requests
import datetime
import urllib.parse
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class ProfessionalHunter:
    def __init__(self, target_url):
        if not target_url.startswith(("http://", "https://")):
            target_url = f"https://{target_url}"

        self.target_url = target_url.rstrip("/")
        self.domain = urllib.parse.urlparse(self.target_url).netloc

        # Workspace setup
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        self.base_dir = f"./Active_Targets/{self.domain}/{self.timestamp}"

        self.headers = {"User-Agent": "Bug-Bounty-Crawler/1.0"}
        self.discovered_params = {}  # {path: set(params)}

        self.create_workspace()

    def create_workspace(self):
        """Creates the professional folder structure"""
        try:
            for folder in ("recon", "crawled_data", "reports"):
                folder_path = os.path.join(self.base_dir, folder)
                os.makedirs(folder_path, exist_ok=True)
                print(f"[+] Created directory: {folder_path}")
        except OSError as e:
            print(f"[!] Failed to create directory {self.base_dir}: {e}")
            raise # Re-raise the exception after logging
           
    def crawl_and_extract_params(self):
        """Phase 3: Parameter Discovery"""
        print(f"[*] Crawling {self.target_url} for parameters...")

        try:
            response = requests.get(
                self.target_url,
                headers=self.headers,
                verify=False,
                timeout=10,
            )
            response.raise_for_status() # Raises an HTTPError for bad responses

            soup = BeautifulSoup(response.text, "html.parser")

            # 1. Extract parameters from links
            for link in soup.find_all("a", href=True):
                full_url = urllib.parse.urljoin(self.target_url, link["href"])
                parsed = urllib.parse.urlparse(full_url)
                params = urllib.parse.parse_qs(parsed.query)

                if params:
                    path = parsed.path or "/"
                    self.discovered_params.setdefault(path, set()).update(params.keys())

            # 2. Extract parameters from forms
            for form in soup.find_all("form"):
                action = form.get("action") or "/"
                full_action = urllib.parse.urljoin(self.target_url, action)
                parsed = urllib.parse.urlparse(full_action)
                path = parsed.path or "/"

                inputs = {
                    field.get("name")
                    for field in form.find_all(["input", "textarea"])
                    if field.get("name")
                }

                if inputs:
                    self.discovered_params.setdefault(path, set()).update(inputs)

            # Save results
            output_file = os.path.join(
                self.base_dir, "crawled_data", "parameters.txt"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                for path, params in self.discovered_params.items():
                    f.write(f"Path: {path} | Params: {', '.join(sorted(params))}\n")

            print(f"[+] Found {len(self.discovered_params)} endpoints with parameters.")

        except requests.exceptions.RequestException as e:
            print(f"[!] Request failed: {e}")        
        except Exception as e:
            print(f"[!] Crawl failed: {e}")

    def test_vulnerabilities(self):
        """Phase 4: Vulnerability Assessment"""
        if not self.discovered_params:
            print("[-] No parameters found to test.")
            return

        payload = "<script>alert('XSS')</script>"

        for path, params in self.discovered_params.items():
            url = f"{self.target_url}{path}"

            for param in params:
                print(f"[*] Testing param '{param}' on {path}")
                try:
                    res = requests.get(
                        url,
                        params={param: payload},
                        headers=self.headers,
                        verify=False,
                        timeout=10,
                    )

                    if payload in res.text:
                        self.generate_report(
                            title="Reflected_XSS",
                            severity="Medium",
                            url=url,
                            param=param,
                            payload=payload,
                        )

                except Exception:
                    continue

    def generate_report(self, title, severity, url, param, payload):
        """Standard Finding Template"""
        safe_param = "".join(c for c in param if c.isalnum() or c in ("_", "-"))

        report = (
            f"TITLE: {title}\n"
            f"SEVERITY: {severity}\n"
            f"ASSET: {url}\n"
            f"PARAM: {param}\n"
            f"PAYLOAD: {payload}\n"
        )

        report_path = os.path.join(
            self.base_dir, "reports", f"{title}_{safe_param}.txt"
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        print("    [!] Potential vulnerability found. Report generated.")


# --- Execution ---
if __name__ == "__main__":
    target = input("Enter target (e.g., example.com): ").strip()
    hunter = ProfessionalHunter(target)
    hunter.crawl_and_extract_params()
    hunter.test_vulnerabilities()
