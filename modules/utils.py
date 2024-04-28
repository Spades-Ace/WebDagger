# modules/utils.py

def parse_burp_request(file_path):
    headers = {}
    parameters = {}
    body = ''
    with open(file_path, 'r' , encoding='utf-8') as file:
        lines = file.readlines()
        is_body = False
        for line in lines:
            if line.strip() == '':
                is_body = True
                continue
            if is_body:
                body += line
            else:
                parts = line.strip().split(': ')
                if len(parts) >= 2:  # Ensure there are at least two parts
                    headers[parts[0]] = ': '.join(parts[1:])  # Handle values with colons
                else:
                    # Check for URL query parameters
                    if '?' in line:
                        query_string = line.strip().split('?')[1]
                        params = query_string.split('&')
                        for param in params:
                            key, value = param.split('=')
                            parameters[key] = value
                    # Check for POST body parameters
                    else:
                        params = line.strip().split('&')
                        for param in params:
                            key, value = param.split('=')
                            parameters[key] = value

    # Print headers, parameters, and body for logging
    print("Headers:", headers)
    print("Parameters:", parameters)
    print("Body:", body)
    
    return headers, parameters, body

# modules/utils.py

def construct_url(headers, parameters):
    host = headers.get('Host')
    if not host:
        return None  # Host header is required to construct the URL

    # Extract additional path/query parameters from the headers, if any
    path = headers.get('Referer')
    if path:
        # Extract path from the Referer header
        path = path.split('://', 1)[-1]  # Remove scheme
        path = path.split('/', 1)[-1]  # Remove host part
        if '?' in path:
            path, query = path.split('?', 1)
            parameters.update(parse_query_string(query))

    # Construct the URL
    url = f"http://{host}/{path}?{'&'.join([f'{k}={v}' for k, v in parameters.items()])}"
    return url

def parse_query_string(query_string):
    parameters = {}
    for param in query_string.split('&'):
        key, value = param.split('=')
        parameters[key] = value
    return parameters
