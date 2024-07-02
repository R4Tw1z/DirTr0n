# DirTr0n

 ## This Tool is based on **CVE-2024-28995 Critical Directory Traversal Vulnerability**


DirTr0n is an directory traversal and vulnerability scanning tool designed to help security professionals identify hidden directories and sensitive files on web servers. With its powerful features, including concurrency for faster scans, customizable headers, and detailed response analysis, DirTr0n provides a comprehensive solution for testing and securing web applications.

# Features
  **Concurrency:** Perform multiple requests simultaneously to speed up the scanning process.
  
 **Customizable Headers:** Add custom headers, including User-Agent strings, to tailor requests.

 **Progress Indicator:** Monitor the scan progress with a dynamic progress bar.
 
  **Output to File:** Save results to a file for easy review and analysis.
 
 **Status Code Filtering**: Specify which HTTP status codes to look for as indicators of success.
 
  **Verbose Mode:** Get detailed output for debugging and analysis.
  
  **URL Encoding:** Automatically encodes payloads to handle special characters.

# Installation and Run
    git clone https://github.com/R4Tw1z/DirTr0n.git
    cd DirTr0n
    pip3 install -r requirements.txt
    python3 dirtr0n.py -u <target_url> <payloads_file>

  # Usage Examples
  
  python3 dirtr0n.py -u https://example.com -p payloads.txt

  python3 dirtr0n.py -u https://example.com -p payloads.txt --verbose

  python3 dirtr0n.py -u https://example.com -p payloads.txt --output results.txt
  
  python3 dirtr0n.py -u https://example.com -p payloads.txt --header "User-Agent: DirTr0n" --delay 2
  
  python3 dirtr0n.py -u https://example.com -p payloads.txt --concurrency 10
  
