import argparse
import requests
import time
import urllib.parse
import threading
from tqdm import tqdm  # For progress bar
import os

DEFAULT_PAYLOAD_FILE = 'Basic-payload.txt'
TOOL_NAME = 'R4Tw1z(DirTr0n)'

def fetch_url(full_url, method, headers, timeout, delay, status_codes, output_file, verbose):
    try:
        if method.upper() == 'GET':
            response = requests.get(full_url, headers=headers, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(full_url, headers=headers, timeout=timeout)
        else:
            print(f"[ERROR] {TOOL_NAME} - Unsupported HTTP method: {method}")
            return
        
        if status_codes and response.status_code in status_codes:
            result = f"[+] {TOOL_NAME} FOUND: {full_url} (Status Code: {response.status_code})"
            if verbose:
                print(result)
            if output_file:
                with open(output_file, 'a') as out_file:
                    out_file.write(result + '\n')
        elif not status_codes and response.status_code == 200:
            result = f"[+] {TOOL_NAME} FOUND: {full_url}"
            if verbose:
                print(result)
            if output_file:
                with open(output_file, 'a') as out_file:
                    out_file.write(result + '\n')
        else:
            if verbose:
                print(f"[-] {TOOL_NAME} NOT FOUND: {full_url} (Status Code: {response.status_code})")

        time.sleep(delay)
    except requests.RequestException as e:
        print(f"[ERROR] {TOOL_NAME} Connection error for {full_url}: {str(e).split(':')[0]}")

def traversal_attack(url, payloads, method='GET', headers=None, timeout=10, delay=0, output_file=None, status_codes=None, verbose=False, concurrency=5):
    print(f"\n[*] {TOOL_NAME}")
    print(f"[*] Target URL: {url}")
    print(f"[*] HTTP Method: {method}")
    print(f"[*] Number of Payloads: {len(payloads)}")
    print(f"[*] Concurrency Level: {concurrency}\n")
    
    # Show progress bar
    with tqdm(total=len(payloads), desc="Scanning") as pbar:
        def worker(payload):
            encoded_payload = urllib.parse.quote(payload)
            full_url = f"{url}/{encoded_payload}"
            fetch_url(full_url, method, headers, timeout, delay, status_codes, output_file, verbose)
            pbar.update(1)

        # Create thread pool
        threads = []
        for i in range(0, len(payloads), concurrency):
            batch = payloads[i:i+concurrency]
            for payload in batch:
                thread = threading.Thread(target=worker, args=(payload,))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

def load_payloads(payload_source):
    if os.path.isfile(payload_source):
        # Load payloads from a file
        with open(payload_source, 'r') as f:
            return f.read().splitlines()
    else:
        # Treat the payload_source as a comma-separated list of payloads
        return payload_source.split(',')

def main():
    parser = argparse.ArgumentParser(description=TOOL_NAME)
    parser.add_argument('-u', '--url', dest='url', required=True, help='Target URL')
    parser.add_argument('-p', '--payloads', dest='payloads', 
                        help='Comma-separated list of payloads or a file containing payloads (one per line). Default is "Basic-payload.txt" if not specified.')
    parser.add_argument('-m', '--method', dest='method', default='GET', choices=['GET', 'POST'], 
                        help='HTTP method to use for requests (default: GET)')
    parser.add_argument('--header', dest='headers', action='append', metavar='KEY:VALUE',
                        help='Additional headers in the format KEY:VALUE (can be specified multiple times)')
    parser.add_argument('--timeout', dest='timeout', type=int, default=10,
                        help='Timeout for each request in seconds (default: 10)')
    parser.add_argument('--delay', dest='delay', type=int, default=0,
                        help='Delay between requests in seconds (default: 0)')
    parser.add_argument('--output', dest='output_file', help='File to write results to')
    parser.add_argument('--status-codes', dest='status_codes', type=int, nargs='*', 
                        help='List of HTTP status codes to consider as success (e.g., 200 403)')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Enable verbose output for debugging')
    parser.add_argument('--concurrency', dest='concurrency', type=int, default=5,
                        help='Number of concurrent requests (default: 5)')
    
    args = parser.parse_args()
    
    headers = {}
    if args.headers:
        for header in args.headers:
            try:
                key, value = header.split(':', 1)
                headers[key.strip()] = value.strip()
            except ValueError:
                print(f"[WARNING] {TOOL_NAME} - Ignoring invalid header format: \"{header}\". Expected format is KEY:VALUE.")

    payloads_file = args.payloads if args.payloads else DEFAULT_PAYLOAD_FILE
    payloads = load_payloads(payloads_file)

    traversal_attack(args.url, payloads, args.method, headers, args.timeout, args.delay, args.output_file, args.status_codes, args.verbose, args.concurrency)

if __name__ == '__main__':
    main()
