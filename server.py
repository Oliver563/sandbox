from ast import Dict
from asyncore import write
from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.dom.minidom import Document
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("server"),
    autoescape=select_autoescape())

hostName = "localhost"
serverPort = 8080
save_data = [
    #dict( c1 = "", c2 = "", c3 = "", c4 = "", c5 = "" )
    dict( c1 = ("", "tile"), c2 =  ("", "tile"), c3 =  ("", "tile"), c4 =  ("", "tile"), c5 =  ("", "tile") )
]
template = env.get_template("sandbox-template.html")
f = open("./static/wordle.css", "r")

word = "WRITE"

current_row = 0

def save_data_to_dict(d):
  values = d.split('&')
  for value in values:
    row = int(value[1:2])
    col = 'c' + value[3:4]
    value = value.split('=')[1]
    save_data[row - 1][col] = value
  
  evaulate()
  save_data.append(dict( c1 = ("", "tile"), c2 =  ("", "tile"), c3 =  ("", "tile"), c4 =  ("", "tile"), c5 =  ("", "tile") ))
  global current_row 
  current_row += 1

def evaulate():
   position = 0 
   global current_row 
   for letter in save_data[current_row].values():
    if letter[0].upper() == word[position:position+1]:
       print("foundit!") 
       col = 'c' + str(position)
       save_data[current_row][col] = (letter[0].upper(), 'correct')

    elif (word.__contains__(letter[0].upper())):
       print("Found it but not here!")
       col = 'c' + str(position)
       save_data[current_row][col] = (letter[0].upper(), 'present')

    else:
      print("Not found")  
      col = 'c' + str(position)
      save_data[current_row][col] = (letter[0].upper(), 'absent')

    position += 1    


class MyServer(BaseHTTPRequestHandler):
    def _set_response(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()
        
        
    def do_GET(self):
        path = self.path
        f.seek(0)
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