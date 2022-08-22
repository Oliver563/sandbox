import os
from ast import Dict
from asyncore import write
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, PackageLoader, select_autoescape
import random

save_data = [{ "c1": ("", "tile"), "c2": ("", "tile"), "c3" : (
        "", "tile"), "c4": ("", "tile"),"c5": ("", "tile") }
]

current_path = os.path.dirname(__file__)
f = open(current_path + "\static\wordle.css", "r")
static_content = bytes(f.read(), "utf-8")
f.close()

words = ['WRITE','FOUND','COUNT','TIGER','FIGHT','DREAD','SOUND','AUDIO','INPUT','DOUBT','TROOP']
word = (random.choice(words))
print(word)

current_row = 0
answer = ''

def save_data_to_dict(d):
    global current_row
    values = d.split('&')
    for value in values:
        row = int(value[1:2])
        col = 'c' + value[3:4]
        value = value.split('=')[1]
        if (row == current_row + 1):
            save_data[row - 1][col] = value

    evaulate()

    if (current_row == 5):
        global answer
        answer = 'Bad luck, the word was ' + word

    if (answer == ''):
        save_data.append({ "c1": ("", "tile"), "c2": ("", "tile"), "c3" : (
        "", "tile"), "c4": ("", "tile"),"c5": ("", "tile") })
        current_row += 1

def evaulate():
    position = 0
    global current_row
    found = 0
    for letter in save_data[current_row].values():
        if letter[0].upper() == word[position:position+1]:
            print("foundit!")
            found += 1
            col = 'c' + str(position + 1)
            save_data[current_row][col] = (letter[0].upper(), 'correct')

        elif (word.__contains__(letter[0].upper())):
            print("Found it but not here!")
            col = 'c' + str(position + 1)
            save_data[current_row][col] = (letter[0].upper(), 'present')

        else:
            print("Not found")
            col = 'c' + str(position + 1)
            save_data[current_row][col] = (letter[0].upper(), 'absent')

        position += 1

    if(found == 5):
        global answer
        answer = 'Congratulations!'

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()

    def do_GET(self):
        global static_content
        path = self.path
        if path == "/static/wordle.css":
            type = "text/css"
            self._set_response(type)
            self.wfile.write(static_content)
        elif path == "/favicon.ico":
            type = "image/x-icon"
            self._set_response(type)
        else:
            type = "text/html"
            self._set_response(type)
            self.wfile.write(bytes(template.render(data=save_data, answer=answer), "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(303)
        self.send_header('Location', self.path)
        self.end_headers()
        global answer 
        if (answer == ''):
            save_data_to_dict(post_data.decode('utf-8'))

if __name__ == "__main__":

    env = Environment(loader=PackageLoader("server"),autoescape=select_autoescape())

    hostName = "localhost"
    serverPort = 8080
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    template = env.get_template("sandbox-template.html")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
