import http.server  # paramétrage : localisation handler
import socketserver # faire une écoute en temps réel

# on va commencer à travailler avec des classes car c'est orienté objet
# partie handler

class APIHandler(http.server.SimpleHTTPRequestHandler): 
    def do_GET(self) :
        print ("salut poto")
        self.send_response(200)
        self.send_header('content-type','text/json')
        self.end_headers()
        self.wfile.write("Bingo".encode('utf-8'))

MyAPIHandler = APIHandler  #notre commande ** le handler est là pour créeer des famille en gros

#partie server


try:
    with socketserver.TCPServer(("",8080), MyAPIHandler) as httpd: # création d'une instance
        print("Server working")
        httpd.allow_reuse_address = True
        httpd.serve_forever() # fonction définit par défaut
except KeyboardInterrupt:
    print("Stopping server")
    httpd.server_close()