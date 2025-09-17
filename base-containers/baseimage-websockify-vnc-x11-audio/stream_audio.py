import http.server
import socketserver

class AudioHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'audio/mpeg')
        self.end_headers()
        self.wfile.write(self.rfile.read())

httpd = socketserver.TCPServer(('localhost', 7772), AudioHandler)
httpd.serve_forever()