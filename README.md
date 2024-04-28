## WebDagger

WebDagger is a web vulnerability scanner tool, still under development, designed to help identify security vulnerabilities in web applications. Currently, it supports scanning for XSS vulnerabilities.

### Usage

1. Capture the request using BurpSuite or any similar tool.
2. Copy the captured request to a text file.
3. Upload the text file using the provided interface in WebDagger.

### Important Notes

- **Real-Time Report**: After uploading the request file, the scanner will run in the background. If the Real-Time Report does not show any updates, open the network tab in your browser's developer tools and try again. This issue is being addressed and will be resolved soon.

- **Modules Under Development**: Currently, WebDagger supports XSS vulnerability scanning. Additional modules for scanning SQL injection, SSRF, SSTI, etc., are planned to be added in future releases.

### Installation

If you want to use WebDagger in your local environment, follow these steps:

1. Clone the WebDagger repository using the following command:

   ```
   git clone https://github.com/Spades-Ace/WebDagger.git
   ```

2. Navigate to the cloned directory:

   ```
   cd WebDagger
   ```

3. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```
   python3 app.py
   ```
   A sample request file (req.txt) is provided for testing purposes.

### Contributions

Contributions to WebDagger are welcome! Feel free to submit pull requests, report issues, or suggest improvements to help make this tool more robust and effective.

### Disclaimer

WebDagger is provided for educational and testing purposes only. It is your responsibility to use this tool ethically and only on web applications you have permission to test. The developers of WebDagger are not responsible for any misuse or illegal activities performed using this tool.
