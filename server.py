from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("server"),
    autoescape=select_autoescape())

hostName = "localhost"
serverPort = 8080

template = env.get_template("sandbox-template.html")

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(template.render(name="Oliver"), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")