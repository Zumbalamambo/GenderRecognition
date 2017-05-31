import SocketServer
import urllib2
import predict
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        f = open("index.html", 'r')
        self.wfile.write(f.read())
    def do_POST(self):
        content_length= int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_length)
        print post_body
        matricula = post_body.split("=")[1] 
        image_adress ="http://micampus.mxl.cetys.mx/fotos/0{}.jpg".format(matricula)
        try:
            image = urllib2.urlopen(image_adress).read()
        except urllib2.HTTPError:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            response = """
            <html> 
            <body>
                <h1> No encontre este estudiante</h1>
                <form>
                    <input type="submit" value="Regresar">
                </form>
            </body>
            </html>
            """
            self.wfile.write(response)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            f = open("images/webapp/unlabeled/image.jpg", "w")
            f.write(image)
            f.close()
            prediction = predict.predict()
            print prediction
            response = """
            <html> 
            <body>
                <h1> creo que eres un{}! </h1>
                <img src={} width=328px height=400px>
                <form>
                    <input type="submit" value="Regresar">
                </form>
            </body>
            </html>
            """.format(" hombre" if prediction[0] == 1.0 else "a mujer", image_adress)
            self.wfile.write(response)


if __name__ == "__main__":
    httpserver = HTTPServer(("192.168.1.66",8000), myHandler)
    httpserver.serve_forever()
