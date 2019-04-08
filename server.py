import http.server
import socketserver
import requests
from urllib import parse
import json as js

#avoiding 'port already in use' warning
socketserver.TCPServer.allow_reuse_address = True

#defining the server's port
PORT = 8000


class TestHandler(http.server.BaseHTTPRequestHandler):
    # function for retrieving the information of the ensembl database (a request):
    def retrieve(self, resource):
        server = "http://rest.ensembl.org"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        r = requests.get(server + resource, headers=headers)
        decoded = r.json()
        return decoded

    # function that organizes the parameters of a path into a dictionary using urllib
    def parameters(self):
        # processing the message from the client with urllib and store it in variables ('chromo','specie'...)
        path=self.path
        parse.urlsplit(path)
        parse.parse_qs(parse.urlsplit(path).query)
        variables = dict(parse.parse_qsl(parse.urlsplit(path).query))
        return variables

    # Function that processes the information either to process it as an html or a json (requested by the user)
    def htmljson(self, variables, info, json):
        # if the json variable does not appear, the user wants the information in html format
        # so the restults are copied in a html file
        if not ('json' in variables):
            f = open('response.html', 'r')
            content = f.read()
            content = content.replace('msg', info)
            content_type = 'text/html'
        # if the json variable appears(that means that the user wants to retrieve a json file)
        # the content sent will be the json dictionary and not the html page with 'info'
        else:
            content = json
            content_type = 'application/json'
            with open('data.json', 'w') as outfile:
                js.dump(content, outfile)
            f = open('data.json', 'r')
            content = f.read()

        return content, content_type

    # Function that retrieves the information of every action on this project and processes it. It stores it either in
    # a list or string (info) or in a dictionary (for converting then to json)
    def operations(self):

        path = self.path
        variables = self.parameters()
        # info will be used if the user asks for html and json if it asks for a json file
        info = []
        json = {}

        # -These are all the possible functions that the user can choose and its operations.
        # -It retrieves the information and processes it depending on the function demanded
        # -The variable decoded it's always the raw information retrieved from the ensembl database.
        try:
            if 'listSpecies' in path:
                resource = "/info/species"
                decoded = self.retrieve(resource)
                species = (decoded['species'])
                for i in species:
                    info.append(i['common_name'])
                try:
                    info = info[0:int(variables['quantity'])]
                except:
                    pass

                json['list_species'] = dict(zip(range(len(info)), info))
                info = '<h3>These are the species requested from the ensembl database:</h3><p></p>' + '<p></p>'.join(
                    info)

            elif 'karyotype' in path:
                resource = "/info/assembly/" + variables['specie'] + '?'
                decoded = self.retrieve(resource)
                info = decoded['karyotype']

                json['karyotype'] = info
                info = '<h3>The karyotype of your specie is:</h3><p></p>' + ','.join(info)

            elif 'chromosomeLength' in path:
                resource = "/info/assembly/" + variables['specie'] + '?'
                decoded = self.retrieve(resource)

                chromosomes = decoded['top_level_region']
                for chrom in chromosomes:
                    if chrom['name'] == variables['chromo']:
                        info = ('The chromosome ' + variables['chromo'] + ' of a ' + variables[
                            'specie'] + ' has a lenght of: ' + str(chrom['length']) + 'nm')
                        json[variables['chromo'] + '_lenght'] = str(chrom['length'])

            elif 'geneSeq' in path:
                # first finding the ID for that non-scientific name
                resource = "/xrefs/symbol/homo_sapiens/" + variables['gene'] + '?'
                decoded = self.retrieve(resource)
                id = decoded[0]['id']
                # then finding the sequence for that id
                resource = "/sequence/id/" + id
                decoded = self.retrieve(resource)
                seq = decoded['seq']

                json['seq_of_' + variables['gene']] = seq
                info = ('<h3>The sequence of the gene is:</h3>' + seq)

            elif 'geneInfo' in path:
                resource = "/xrefs/symbol/homo_sapiens/" + variables['gene'] + '?'
                decoded = self.retrieve(resource)
                id = decoded[0]['id']

                resource = "/sequence/id/" + id
                decoded = self.retrieve(resource)
                seq = decoded['seq']

                resource = "/lookup/id/" + id
                decoded = self.retrieve(resource)
                categories = ['start', 'end', 'length', 'id']
                data = [str(decoded['start']), str(decoded['end']), len(seq), id]

                json[variables['gene']] = dict(zip(categories, data))
                info = 'This gene starts at: ' + str(decoded['start']) + '<p></p>This gene ends at: ' + str(
                    decoded['end']) + '<p></p>This gene has a length of: ' + str(
                    len(seq)) + "<p></p>This gene's ID is: " + id

            elif 'geneCal' in path:
                resource = "/xrefs/symbol/homo_sapiens/" + variables['gene'] + '?'
                decoded = self.retrieve(resource)
                id = decoded[0]['id']

                resource = "/sequence/id/" + id
                decoded = self.retrieve(resource)
                seq = decoded['seq']
                length = len(seq)
                perc = {'T': seq.count('T') / length * 100,
                        'A': seq.count('A') / length * 100,
                        'C': seq.count('C') / length * 100,
                        'G': seq.count('G') / length * 100}

                json[variables['gene'] + '_perc'] = perc
                info = 'The total length of the sequence is: ' + str(length) + '<p></p>The percentage of T is: ' + str(
                    perc['T']) + '%<p></p>The percentage of C is: ' + str(
                    perc['C']) + '%<p></p>The percentage of G is: ' + str(
                    perc['G']) + '%<p></p>The percentage of A is: ' + str(perc['A']) + '%'

            elif 'geneList' in path:
                resource = "/overlap/region/human/" + str(variables['chromo']) + ":" + str(variables['start']) + '-' + str(variables['end']) + '?feature=gene;'
                decoded = self.retrieve(resource)
                info = ''
                json['genes_chrom' + variables['chromo']] = []
                for i in range(len(decoded)):
                    name = decoded[i]['external_name']
                    info += '<p></p>' + str(name)
                    json['genes_chrom' + variables['chromo']].append(name)

            content, content_type = self.htmljson(variables, info, json)

        # If the form is incorrect, an error html page appears, with a link to the main page
        except:
            content_type = 'text/html'
            f = open('error.html', 'r')
            content = f.read()

        return content, content_type

    def do_GET(self):

        # printing the request line
        print(self.requestline, 'green')
        print('Path: ' + self.path)

        #Checking that the path is alright and directing to the main menu.
        content_type='text/html'
        if self.path== '/':
            f = open("main.html", 'r')
            content = f.read()
        else:
            f = open("error.html", 'r')
            content = f.read()

        # defining the path that the user chose
        path = self.path

        # searching for an '=' on the path, just to avoid an error if /favicon.ico appears as the path
        i = path.find('=')
        # Generating the response for the user if '=' is found (that means that the form has been filled)
        if i != -1:
            content, content_type=self.operations()

        # generating the response message
        self.send_response(200)

        # defining the header:
        self.send_header('Content-Type', content_type)
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