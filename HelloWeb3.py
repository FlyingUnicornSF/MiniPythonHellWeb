# aosabook.org/en/500L/a-simple-web-server.html
import http.server
import os


class ServerException(Exception):
  pass


class RequestHandeler(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
    try: 
      full_path = os.getcwd() + self.path

      if not os.path.exists(full_path):
        raise ServerException("'{0}' not found".format(self.path))
      elif os.path.isfile(full_path):
        self.handle_file(full_path)
      else:
        raise ServerException("Unknown object '{0}'".format(self.path))
    
    except Exception as msg:
      self.handle_error(msg)

  def handle_file(self, full_path):
    try: 
      with open(full_path, 'rb') as reader:
        content = reader.read()
      self.send_content(content)
      
    except IOError as msg:
      msg = "'{0}' canoot be read: {1}".format(full_path, msg)
      self.handle_error(msg)

  Error_page = """\
  <html>
  <body>
  <h1> Error accesssing {path} </h1>
  <p>{msg}</p>
  <html>
  <body>
  """
  def handle_error(self, msg):
    content = self.Error_page.format(path=self.path, msg=msg)
    self.send_content(content.encode(), 404)

  def send_content(self, content, status=200):
    self.send_response(status)
    self.send_header("Content-Type", "text/html")
    self.send_header("Content-Length", str(len(content)))
    self.end_headers()
    self.wfile.write(content)

 #---------------------
if __name__ == '__main__':
  serverAddress = ('', 8080)
  #TypeErro: getsockaddrarag: AF_INET address must be tuple, not 'str'
  #server = http.server.HTTPServer(('', 8080), RequestHandeler)
  server = http.server.HTTPServer(serverAddress, RequestHandeler)
  server.serve_forever()