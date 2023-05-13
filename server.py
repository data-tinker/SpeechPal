from http.server import HTTPServer, BaseHTTPRequestHandler


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes('OK', 'utf-8'))


def run_server():
    web_server = HTTPServer(('0.0.0.0', 8080), MyServer)
    web_server.serve_forever()


if __name__ == '__main__':
    run_server()
