import http.server
import socketserver
import termcolor
import requests


#avoiding 'port already in use' warning
socketserver.TCPServer.allow_reuse_address = True


#defining the server's port
PORT = 8000


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # printing the request line
        termcolor.cprint(self.requestline, 'green')
        print('Path: ' + self.path)

        #checking that the url is right
        if self.path== '/':
            f = open("main.html", 'r')
            content = f.read()
        else:
            f = open("error.html", 'r')
            content = f.read()

        path = self.path

        i = path.find('=')

        if i != -1:
            #processing the message from the client with urllib
            from urllib import parse
            url = path
            parse.urlsplit(url)
            parse.parse_qs(parse.urlsplit(url).query)
            variables=dict(parse.parse_qsl(parse.urlsplit(url).query))
            print(variables)

            #retrieving the information

            server = "http://rest.ensembl.org"
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

            if variables['oper']== 'listspecies':
                resource = "/info/species"
                r = requests.get(server + resource, headers=headers)
                decoded = r.json()
                species = (decoded['species'])
                info=[]
                for i in species:
                    info.append(i['name'])
                try:
                    info=info[0:int(variables['quantity'])]
                except:
                    pass

                info='<p></p>'.join(info)



            elif variables['oper']== 'karyotype':
                resource="/info/assembly/"+variables['specie']+'?'
                r = requests.get(server + resource, headers=headers)
                decoded = r.json()
                info = decoded['karyotype']

            elif variables['oper']== 'chromlength':
                print('cacaaa')







            f = open('response.html', 'r')
            content = f.read()
            content = content.replace('msg', info)


        # generating the response message
        self.send_response(200)

        # defining the header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(content)))
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(content))

        return


















# - Server MAIN program

with socketserver.TCPServer(("", PORT), TestHandler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")