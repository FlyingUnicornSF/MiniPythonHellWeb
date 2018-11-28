import http.server

class RequestHandeler(http.server.BaseHTTPRequestHandler):

  Page = '''\
  <html>
  <body>
  <p>Hello Web!</p>
  </body>
  </html> 
  '''

    #handel a GET request
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-Type", "text/html")
    self.send_header("Content-Length", str(len(self.Page)))
    self.end_headers()
    # Had to add .encode() for python 3.7 "TypeError: a bytes-like object is required, not 'str' 
    self.wfile.write(self.Page.encode())

 #---------------------
if __name__ == '__main__':
  serverAddress = ('', 8080)
  #TypeErro: getsockaddrarag: AF_INET address must be tuple, not 'str'
  #server = http.server.HTTPServer(('', 8080), RequestHandeler)
  server = http.server.HTTPServer(serverAddress, RequestHandeler)
  server.serve_forever()