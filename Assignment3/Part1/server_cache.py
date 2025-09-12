import http.server
import socketserver
import os
import hashlib
from email.utils import formatdate

PORT = 9000
TARGET_FILE = "index.html"

class CacheHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            filepath = TARGET_FILE

            if not os.path.exists(filepath):
                self.send_error(404, f"File Not Found: {self.path}")
                return

            # Load file content and metadata
            stat_info = os.stat(filepath)
            with open(filepath, "rb") as f:
                content = f.read()

            # Prepare headers
            last_mod_time = stat_info.st_mtime
            last_mod_http = formatdate(timeval=last_mod_time, usegmt=True)
            etag_val = '"' + hashlib.md5(content).hexdigest() + '"'

            # --- Client cache validation ---
            client_etag = self.headers.get("If-None-Match")
            client_mod = self.headers.get("If-Modified-Since")

            not_modified = False
            if client_etag and client_etag == etag_val:
                not_modified = True
            elif client_mod and client_mod == last_mod_http:
                not_modified = True

            if not_modified:
                self.send_response(304)   # Not Modified
                self.end_headers()
                return

            # --- Send fresh response ---
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Last-Modified", last_mod_http)
            self.send_header("ETag", etag_val)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, f"File Not Found: {self.path}")

# Run the server
HOST = "127.0.0.1"
with socketserver.TCPServer((HOST, PORT), CacheHandler) as httpd:
    print(f"Server is running at http://{HOST}:{PORT}")
    httpd.serve_forever()
