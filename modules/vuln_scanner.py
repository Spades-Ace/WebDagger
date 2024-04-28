# modules/vuln_scanner.py

from threading import Thread
from .xss.xss_scanner import xss_scanner
from .utils import construct_url

def scan_for_vulnerabilities(headers, parameters, body):
    print("We are scanning the request for vulnerabilities...")

    url = construct_url(headers, parameters)
    if not url:
        print("Failed to construct URL. Host header is missing.")
        return

    print("Constructed URL:", url)

    # Define a function to run xss_scanner as a thread
    def scan_xss():
        xss_vulnerability_found = xss_scanner(url)
        if xss_vulnerability_found:
            print("XSS vulnerability detected!")
            # Here you can take further action, such as logging, notifying the user, etc.
        else:
            print("No vulnerabilities detected.")
        print("Vulnerability scanning complete.")
    
    def scan_sql_injection():
        # Implement SQL injection scanning here\

        pass

    # Create and start a thread for running scan_xss function
    xss_thread = Thread(target=scan_xss)
    xss_thread.start()
    # sqli_thread = Thread(target=scan_sql_injection)
    # sqli_thread.start()
