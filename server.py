import http.server
import socketserver

import requests
from urllib import parse



#avoiding 'port already in use' warning
socketserver.TCPServer.allow_reuse_address = True

#defining the server's port
PORT = 8000


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        # printing the request line
        print(self.requestline, 'green')
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
            parse.urlsplit(path)
            parse.parse_qs(parse.urlsplit(path).query)
            variables=dict(parse.parse_qsl(parse.urlsplit(path).query))

            #function for retrieving the information of the ensembl database:
            def request(source):
                server = "http://rest.ensembl.org"
                headers = {"Content-Type": "application/json", "Accept": "application/json"}
                r = requests.get(server + resource, headers=headers)
                decoded = r.json()
                return decoded

            #Processing the information and getting results

            info=[]
            try:
                if 'listSpecies' in path:
                    resource = "/info/species"
                    decoded=request(resource)
                    species = (decoded['species'])
                    for i in species:
                        info.append(i['name'])
                    try:
                        info=info[0:int(variables['quantity'])]
                    except:
                        pass

                    info='<p></p>'.join(info)

                elif 'karyotype' in path:
                    resource="/info/assembly/"+variables['specie']+'?'
                    decoded=request(resource)
                    info = decoded['karyotype']
                    info=','.join(info)

                elif 'chromosomeLength' in path:
                    resource = "/info/assembly/" + variables['specie']+'?'
                    decoded=request(resource)
                    karyo = decoded['karyotype']

                    chromosomes = decoded['top_level_region']
                    for chrom in chromosomes:
                        if chrom['name']==variables['chromo']:
                            info=('The chromosome '+chrom['name']+ ' of a '+variables['specie']+' has a lenght of: '+str(chrom['length'])+'nm')

                elif 'geneSeq' in path:
                    resource = "/xrefs/symbol/homo_sapiens/" + variables['gene'] + '?'
                    decoded=request(resource)
                    id = decoded[0]['id']

                    resource = "/sequence/id/" + id
                    decoded=request(resource)
                    seq = decoded['seq']

                    info = ('The sequence of the gene is: '+ seq)
                elif 'geneInfo' in path:
                    resource = "/xrefs/symbol/homo_sapiens/" + variables['gene'] + '?'
                    decoded=request(resource)
                    id = decoded[0]['id']

                    resource = "/sequence/id/" + id
                    decoded=request(resource)
                    seq = decoded['seq']

                    resource = "/lookup/id/" + id
                    decoded=request(resource)

                    info= 'This gene starts at: '+ str(decoded['start'])+ '<p></p>This gene ends at: '+ str(decoded['end'])+'<p></p>This gene has a length of: '+str(len(seq))+"<p></p>This gene's ID is: " + id

                elif 'geneCal' in path:
                    resource = "/xrefs/symbol/homo_sapiens/" + variables['gene'] + '?'
                    decoded=request(resource)
                    id = decoded[0]['id']

                    resource = "/sequence/id/" + id
                    decoded=request(resource)
                    seq = decoded['seq']
                    length= len(seq)
                    perc= {'T': seq.count('T')/length*100,
                             'A': seq.count('A')/length*100,
                             'C': seq.count('C')/length*100,
                             'G': seq.count('G')/length*100}

                    info= 'The total length of the sequence is: '+str(length)+ '<p></p>The percentage of T is: '+ str(perc['T'])+ '%<p></p>The percentage of C is: '+ str(perc['C'])+ '%<p></p>The percentage of G is: '+ str(perc['G'])+ '%<p></p>The percentage of A is: '+ str(perc['A'])+'%'

                elif 'geneList' in path:
                    resource= resource = "/overlap/region/human/"+str(variables['chromo'])+":"+str(variables['start'])+'-'+str(variables['end'])+'?feature=gene;'
                    decoded=request(resource)
                    print(resource)

                    for i in decoded:
                        name = i['assembly_name']
                        gene_id = i['gene_id']
                        info1 = ('Gene name: ' + str(name) + '     Gene id: ' + str(gene_id))
                        print(info1)
                        try:
                            info = info.append(info1)
                        except:
                            pass
                    info = '<p></p>'.join(info)


                f = open('response.html', 'r')
                content = f.read()
                content = content.replace('msg', info)

            except:

                f=open('error.html', 'r')
                content=f.read()


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