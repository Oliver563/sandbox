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
f = open(current_path + "\static\wordle.css", "r") # opens the css style sheet on read
static_content = bytes(f.read(), "utf-8") #sets static_content as the css style sheet
f.close()

word = (random.choice(open("words.txt").read().split())) # gets a random word out of the word list
word = word.upper() # sets the random word to uppercase
print(word)

current_row = 0
answer = ''

def save_data_to_dict(d):
    global current_row
    values = d.split('&') # removes the & from the data
    for value in values:
        row = int(value[1:2]) # sets the row and the col to the appropriate values within the data
        col = 'c' + value[3:4]
        value = value.split('=')[1] # removes the = from the data
        if (row == current_row + 1):
            save_data[row - 1][col] = value # saves the data to the dict at the end of the row

    evaulate()

    if (current_row == 5): # the lose condition
        global answer
        answer = 'Bad luck, the word was ' + word 

    if (answer == ''): 
        save_data.append({ "c1": ("", "tile"), "c2": ("", "tile"), "c3" : (
        "", "tile"), "c4": ("", "tile"),"c5": ("", "tile") })
        current_row += 1 # moves the current row down and sets the data of the row to nothing

def evaulate(): # checks the letter to the word and updates the letters status
    position = 0
    global current_row
    found = 0
    for letter in save_data[current_row].values():
        if letter[0].upper() == word[position:position+1]: # is the letter in the correct place in the word?
            print("foundit!")
            found += 1
            col = 'c' + str(position + 1)
            save_data[current_row][col] = (letter[0].upper(), 'correct') # sets the status of the letter

        elif (word.__contains__(letter[0].upper())): # if the word contains the letter but not in the right place
            print("Found it but not here!")
            col = 'c' + str(position + 1)
            save_data[current_row][col] = (letter[0].upper(), 'present')

        else: # if the letter is not found within the word
            print("Not found")
            col = 'c' + str(position + 1)
            save_data[current_row][col] = (letter[0].upper(), 'absent')

        position += 1

    if(found == 5): # the win condition
        global answer
        answer = 'Congratulations!'

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()

    def do_GET(self): #gets information from server
        global static_content
        path = self.path
        if path == "/static/wordle.css":
            type = "text/css" # sets the appropriate content type to each of the files
            self._set_response(type)
            self.wfile.write(static_content) 
        elif path == "/favicon.ico":
            type = "image/x-icon"
            self._set_response(type)
        else:
            type = "text/html"
            self._set_response(type)
            self.wfile.write(bytes(template.render(data=save_data, answer=answer), "utf-8"))

    def do_POST(self): #sends information to server
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
