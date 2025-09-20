from http.server import HTTPServer, BaseHTTPRequestHandler
import pathlib
import urllib.parse
import mimetypes
import json
import datetime
from jinja2 import Environment, FileSystemLoader

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('message.html')
        elif pr_url.path == '/read':
            self.send_read_page()
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)
                
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)
        
        # Save data to storage/data.json with timestamp
        self.save_message_to_storage(data_dict)
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def is_static_file(self, path):
        """Check if the requested path is a static file (CSS, JS, images, fonts, etc.)"""
        static_extensions = [
            '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
            '.woff', '.woff2', '.ttf', '.eot', '.pdf', '.txt', '.xml'
        ]
        return any(path.lower().endswith(ext) for ext in static_extensions)
    
    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
    
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())
    
    def save_message_to_storage(self, data_dict):
        """Save form data to storage/data.json with timestamp as key"""
        storage_path = pathlib.Path('storage/data.json')
        
        # Create storage directory if it doesn't exist
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing data or create empty dict
        try:
            with open(storage_path, 'r', encoding='utf-8') as f:
                storage_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            storage_data = {}
        
        # Create timestamp as key
        timestamp = datetime.datetime.now().isoformat()
        
        # Add new message with timestamp as key
        storage_data[timestamp] = data_dict
        
        # Save back to file
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, indent=2, ensure_ascii=False)
    
    def send_read_page(self):
        """Render and send the read page with all messages using Jinja2"""
        try:
            # Load data from storage
            storage_path = pathlib.Path('storage/data.json')
            try:
                with open(storage_path, 'r', encoding='utf-8') as f:
                    messages_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                messages_data = {}
            
            # Set up Jinja2 environment
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('read.html')
            
            # Render template with data
            html_content = template.render(messages=messages_data)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            # If template not found or other error, send error page
            print(f"Error rendering read page: {e}")
            self.send_html_file('error.html', 500)

def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    run()
