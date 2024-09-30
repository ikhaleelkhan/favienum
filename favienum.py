import requests
import mmh3
import argparse
import subprocess
import os
import sys
from termcolor import colored

# Function to validate the URL
def validate_url(url):
    if not url.startswith("http"):
        print(colored("[-] Invalid URL format. Please include http or https.", "red"))
        sys.exit(1)
    return url

# Function to download the favicon
def download_favicon(url, ignore_ssl=False):
    try:
        print(colored("[+] Downloading favicon...", "blue"))
        response = requests.get(url, allow_redirects=True, verify=not ignore_ssl)
        if response.status_code == 200:
            with open('favicon.ico', 'wb') as file:
                file.write(response.content)
            print(colored("[+] Favicon downloaded successfully.", "green"))
            return 'favicon.ico'
        else:
            print(colored(f"[-] Failed to download favicon. Status code: {response.status_code}", "red"))
            return None
    except requests.exceptions.SSLError as e:
        print(colored(f"[-] SSL Error: {e}", "red"))
        return None
    except Exception as e:
        print(colored(f"[-] Error: {e}", "red"))
        return None

# Function to generate the Murmur3 hash of the favicon
def generate_favicon_hash(file_path):
    try:
        print(colored("[+] Generating Favicon hash...", "blue"))
        with open(file_path, 'rb') as f:
            favicon = f.read()
        favicon_hash = mmh3.hash(favicon)
        print(colored(f"[+] Favicon Hash: {favicon_hash}", "green"))
        return favicon_hash
    except Exception as e:
        print(colored(f"[-] Error generating hash: {e}", "red"))
        return None

# Function to check if Shodan API is initialized
def check_shodan_api(api_key=None):
    try:
        if api_key:
            print(colored("[+] Initializing Shodan with provided API key...", "blue"))
            subprocess.run(f"shodan init {api_key}", shell=True, check=True)
        else:
            print(colored("[+] Checking Shodan API initialization...", "blue"))
            command = "shodan info"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(colored("[-] Shodan API is not initialized. Please provide an API key.", "red"))
                sys.exit(1)
            else:
                print(colored("[+] Shodan API is initialized correctly.", "green"))
    except Exception as e:
        print(colored(f"[-] Error checking Shodan API: {e}", "red"))
        sys.exit(1)

# Function to search Shodan for the Favicon hash
def search_shodan(favicon_hash):
    try:
        print(colored(f"[+] Searching Shodan for Favicon hash {favicon_hash}...", "blue"))
        command = f"shodan search http.favicon.hash:{favicon_hash} --fields ip_str,port,hostnames,org"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print(colored("[+] Shodan Results:\n", "green"))
                print(output)
                save_results(output, "shodan_results.txt")
            else:
                print(colored("[-] No results found in Shodan.", "yellow"))
        else:
            print(colored(f"[-] Shodan search failed: {result.stderr}", "red"))
    except Exception as e:
        print(colored(f"[-] Error searching Shodan: {e}", "red"))

# Function to use Amass for subdomain enumeration
def run_amass(domain):
    try:
        print(colored("[+] Running Amass for subdomain enumeration...", "blue"))
        command = f"amass enum -d {domain} -passive"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print(colored("[+] Amass Results:\n", "green"))
                print(output)
                save_results(output, "amass_results.txt")
            else:
                print(colored("[-] No subdomains found by Amass.", "yellow"))
        else:
            print(colored(f"[-] Amass failed: {result.stderr}", "red"))
    except Exception as e:
        print(colored(f"[-] Error running Amass: {e}", "red"))

# Function to save results to a file
def save_results(data, filename):
    with open(filename, 'w') as f:
        f.write(data)
    print(colored(f"[+] Results saved to {filename}", "green"))

# Main function to run the tool
def main():
    parser = argparse.ArgumentParser(description="Advanced Favicon-based Subdomain Enumeration Tool")
    parser.add_argument("url", help="The URL of the target domain (e.g., https://example.com)")
    parser.add_argument("--shodan-api", help="Shodan API key (optional if already initialized)", required=False)
    parser.add_argument("--ignore-ssl", action="store_true", help="Ignore SSL certificate verification errors")
    parser.add_argument("--run-amass", action="store_true", help="Run Amass for subdomain enumeration")
    args = parser.parse_args()

    # Validate the URL
    domain_url = validate_url(args.url)

    # Check Shodan API initialization (or initialize with provided API key)
    check_shodan_api(args.shodan_api)

    # Download the favicon from the provided URL, optionally ignoring SSL verification
    favicon_path = download_favicon(domain_url + "/favicon.ico", ignore_ssl=args.ignore_ssl)

    if favicon_path:
        # Generate the hash from the downloaded favicon
        favicon_hash = generate_favicon_hash(favicon_path)

        if favicon_hash:
            # Search Shodan using the generated hash
            search_shodan(favicon_hash)

            # Optionally, run Amass for subdomain enumeration
            if args.run_amass:
                run_amass(args.url.split("//")[-1])

if __name__ == "__main__":
    main()
