from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from werkzeug.utils import secure_filename
import os
import threading
from modules.utils import parse_burp_request
from modules.vuln_scanner import scan_for_vulnerabilities
from queue import Queue
import requests
import time

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global queue for sending SSE messages
message_queue = Queue()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def background_scan(file_path):
    try:
        time.sleep(2)  # Simulate scanning process
        headers, parameters, body = parse_burp_request(file_path)
        scan_results = scan_for_vulnerabilities(headers, parameters, body)

        # Example: Send completion message to the SSE queue
        message_queue.put("Scan initiated")

        # Example: Check for XSS vulnerability and send message to SSE
        for parameter, context in scan_results.items():
            if context == "Payload found":
                message = f"XSS vulnerability found in parameter '{parameter}'"
                send_to_sse(message)
    except Exception as e:
        # Handle exceptions during scanning
        print("in exception because of threading")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                time.sleep(5)
                
                # Run scanning process in the background
                threading.Thread(target=background_scan, args=(file_path,)).start()
                
                # Redirect to the report page
                return redirect(url_for('report'))

    return render_template('index.html')

@app.route('/report')
def report():
    # No need for global variable here
    return render_template('report.html', scan_results=None)

@app.route('/events')
def events():
    print("Starting event stream...")
    def generate():
        while True:
            print()
            message = message_queue.get()
            print("Sending message:", message)
            yield f"data: {message}\n\n"

    return Response(generate(), content_type='text/event-stream')

@app.route('/listen', methods=['POST'])
def listen():
    # Get the data from the POST request
    data = request.get_json()
    
    # Forward the data to the /events endpoint
    forward_to_events(data)
    
    # Return a response
    return jsonify({'status': 'success'})
def forward_to_events(data):
    # Add the data to the message queue to trigger SSE update
    message_queue.put(data)
    print("Data received:", data)


@app.route('/test_listen', methods=['GET'])
def test_listen():
    # Sample data to send in the POST request
    sample_data = {"message": "This is a test message"}

    # Send a POST request to the /listen endpoint
    response = requests.post('http://localhost:5000/listen', json=sample_data)

    if response.status_code == 200:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Failed to send POST request to /listen"})

if __name__ == '__main__':
    app.run(debug=True)
