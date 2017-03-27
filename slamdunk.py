import SimpleHTTPServer
import SocketServer

PORT = 81

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT


def do_GET(self):
	self.wfile.write("Hello")

httpd.serve_forever()


