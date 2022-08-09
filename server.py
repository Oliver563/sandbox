from ast import Dict
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("server"),
    autoescape=select_autoescape())

hostName = "localhost"
serverPort = 8080
save_data = dict( r1c1 = "", r1c2 = "", r1c3 = "" )
template = env.get_template("sandbox-template.html")

def save_data_to_dict(d):
  row = d.split('&')
  for cell in row:
    save_data[cell.split('=')[0]] = cell.split('=')[1]

f = open("./static/wordle.css", "r")

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()
        
    def do_GET(self):
        path = self.path
        print(self.path)
        if path == "/static/wordle.css":
            type = "text/css"
            self._set_response(type)
            self.wfile.write(bytes(f.read(), "utf-8"))
        elif path == "/favicon.ico":
            type = "image/x-icon"
            self._set_response(type)
        else:
            type = "text/html"
            self._set_response(type)
            self.wfile.write(bytes(template.render(data=save_data), "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        self.send_response(303)
        self.send_header('Location', self.path)
        self.end_headers()
        save_data_to_dict(post_data.decode('utf-8'))
        
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")