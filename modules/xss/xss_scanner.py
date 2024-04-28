import argparse

import sys
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Add it to the Python path
sys.path.append(script_dir)
from custom_xss.xss import XSS_Scanner as xss_instance
def xss_scanner(url):
    print("Starting XSS scanning using bane...")
    print("Scanning URL:", url)
    #url="http://testphp.vulnweb.com/search.php?test=query"
    try:
        if url:
            # Scan for XSS vulnerabilities
            script_dir = os.path.dirname(os.path.realpath(__file__))
            print(script_dir)
            file_path = os.path.join(script_dir, "xss_payload.txt")
            print(os.path.exists(file_path))
            results = xss_instance.scan(url,payload=file_path)
            #results = bane.XSS_Scanner.scan(url,payload="./xss-payload-list.txt")

            # Process results
            if results:
                for result in results:
                    print("XSS vulnerability detected at:", result['url'])
                    print("Form inputs:", result['form_inputs'])
                    print("Injected payloads:", result['injected_payloads'])
                    # You can further process or log the results as needed
            else:
                print("No XSS vulnerabilities detected.")
        else:
            print("No URL provided for XSS scanning.")

    except Exception as e:
        print("An error occurred during XSS scanning:", e)

    print("XSS scanning complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL for XSS scanning.")
    parser.add_argument("--url", required=True, help="The URL to scan for XSS vulnerabilities.")
    args = parser.parse_args()
    xss_scanner(args.url)
