from ast import Dict
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("server"),
    autoescape=select_autoescape())

hostName = "localhost"
serverPort = 8080
save_data = dict( name = "" )
template = env.get_template("sandbox-template.html")

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        self._set_response()
        self.wfile.write(bytes(template.render(name=save_data['name']), "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        self.send_response(303)
        self.send_header('Location', self.path)
        self.end_headers()
        save_data['name'] = post_data.decode('utf-8').split('=')[1]

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")