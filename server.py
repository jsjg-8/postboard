from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from datetime import datetime

LOG_FILE = "log.txt"

class LogHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        line = f"[{datetime.now().isoformat()}] {self.client_address[0]} {body}"
        print(line, flush=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK\n")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        try:
            with open(LOG_FILE) as f:
                self.wfile.write(f.read().encode())
        except FileNotFoundError:
            self.wfile.write(b"(empty)\n")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(("0.0.0.0", port), LogHandler)
    print(f"Listening on 0.0.0.0:{port}")
    server.serve_forever()
