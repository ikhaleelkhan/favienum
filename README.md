
# Advanced Favicon-based Subdomain Enumeration Tool

A Python tool to automate downloading a website's favicon, generating its Murmur3 hash, and searching Shodan for subdomains and IP addresses. The tool also provides SSL verification handling and integrates Amass for passive subdomain enumeration.

## Features

- **Favicon Hashing**: Automatically download and hash the favicon of a target domain.
- **Shodan Integration**: Use the favicon hash to search Shodan for related subdomains and IP addresses.
- **SSL Handling**: Option to bypass SSL verification errors when downloading favicons from domains with certificate issues.
- **Amass Integration**: Run Amass for passive subdomain enumeration.
- **Logging**: Automatically save results from Shodan and Amass to log files.

## Requirements

Before using the tool, make sure you have the following:

- **Python 3.x**
- **Required Python Libraries**:
  ```bash
  pip install requests mmh3 termcolor
  ```

- **Shodan CLI**: [Shodan CLI installation](https://cli.shodan.io/)
- **Amass (Optional for subdomain enumeration)**: [OWASP Amass installation](https://github.com/OWASP/Amass#installation)

## Usage

### Basic Command

Run the tool by providing a target URL:

```bash
python3 favienum.py https://example.com
```

### Optional Flags

- `--shodan-api` : Provide a Shodan API key if it's not already initialized.
  
  Example:
  ```bash
  python3 favienum.py https://example.com --shodan-api YOUR_SHODAN_API_KEY
  ```

- `--ignore-ssl` : Ignore SSL certificate verification errors when downloading the favicon.
  
  Example:
  ```bash
  python3 favienum.py https://example.com --ignore-ssl
  ```

- `--run-amass` : Run Amass for passive subdomain enumeration.
  
  Example:
  ```bash
  python3 favienum.py https://example.com --run-amass
  ```

### Example Commands

1. **Download favicon, hash it, and search Shodan**:
   ```bash
   python3 favienum.py https://example.com
   ```

2. **Ignore SSL verification**:
   ```bash
   python3 favienum.py https://example.com --ignore-ssl
   ```

3. **Use a Shodan API key directly**:
   ```bash
   python3 favienum.py https://example.com --shodan-api YOUR_SHODAN_API_KEY
   ```

4. **Run Amass for subdomain enumeration**:
   ```bash
   python3 favienum.py https://example.com --run-amass
   ```

## Output

The tool saves the results to the following files:

- **Shodan Results**: `shodan_results.txt`
- **Amass Results**: `amass_results.txt` (if used)

## Troubleshooting

### SSL Certificate Errors
If you encounter SSL certificate issues, use the `--ignore-ssl` option:

```bash
python3 favienum.py https://example.com --ignore-ssl
```

### Shodan API Issues (403 Forbidden)
Ensure you have a valid Shodan API key with the appropriate permissions. You may need to upgrade to a paid plan to perform favicon searches.

### Shodan API Initialization
If Shodan is not initialized, you can initialize it by providing your API key:

```bash
shodan init YOUR_API_KEY
```

You can also pass the API key directly using the `--shodan-api` argument.

## Prerequisites

1. **Shodan API Key**: A valid Shodan API key is required. You can provide it using the `--shodan-api` argument or initialize it using `shodan init YOUR_API_KEY`.

2. **Amass**: To use Amass for subdomain enumeration, ensure it's installed.

   Install Amass:
   ```bash
   sudo apt install amass
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.
