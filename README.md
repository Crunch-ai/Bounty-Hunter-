# BountyHunter
  
  BountyHunter automates Web Application scanning for Bug Bounty Hunting. 

## Description

Work in Progress

## Getting Started 
  
### Dependencies 
* Beautifulsoup4

  ```
  apt install beautifulsoup4
  ```

### Execution 

  1) Prepare the Environment:

     * Ensure directory ./Active_Targets/ exists and have permission to write in this directory
    
  2)  Run the Code:

     python your_script.py 

  4) Input Valid Target:

     http://valid.url
     
  6) Monitor for Errors 

## Example Output 

```
Enter target (e.g., example.com): [+] Created directory: ./Active_Targets/www.nmap.org/2026-01-20_1653/recon
[+] Created directory: ./Active_Targets/www.nmap.org/2026-01-20_1653/crawled_data
[+] Created directory: ./Active_Targets/www.nmap.org/2026-01-20_1653/reports
[*] Crawling https://www.nmap.org for parameters...
[!] Request failed: HTTPSConnectionPool(host='www.nmap.org', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='www.nmap.org', port=443): Failed to resolve 'www.nmap.org' ([Errno -3] Temporary failure in name resolution)"))
[-] No parameters found to test.
```

## ⚙️ Debugging Notes:

  - Print Debugging: Add additional print statements to check values of variables (i.e. before network requests and file writes)
  - Check Response Status: If you encounter an HTTP error, print the response.status_code and response.text for more context

## ‼️ Potential Issues:

  - Network Errors: "Request Failed" if URL is unreachable
  - HTML Parsing Errors: BeautifulSoup may fail to find links or forms resulting in an empty discovered_params dictionary
  - File Writing Issues: Writing output files due to permissions or file path
