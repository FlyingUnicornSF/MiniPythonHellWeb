# aosabook.org/en/500L/a-simple-web-server.html
import http.server

class RequestHandeler(http.server.BaseHTTPRequestHandler):
# no space allowed between value and { } like JS
  Page = '''\
  <html>
  <body>
  <tr> <td>Header</td> <td>Value</td> </tr>
  <tr> <td>Date and Time</td> <td>{date_time}</td> </tr>
  <tr> <td>Client Location</td> <td>{client_host}</td> </tr>
  <tr> <td>Client Location</td> <td>{client_port}</td> </tr>
  <tr> <td>Command</td> <td>{command}</td> </tr>
  <tr> <td>Path</td> <td>{path}</td> </tr>
  </body>
  </html> 
  '''
  def do_GET(self):
    page = self.create_page()
    self.send_page(page)

  def create_page(self):
    values = {
      'date_time'   : self.date_time_string(),
      'client_host' : self.client_address[0],
      'client_port' : self.client_address[1],
      'command'     : self.command,
      'path'        : self.path
    }
    page = self.Page.format(**values).encode()
    return page

  def send_page(self, page):
    self.send_response(200)
    self.send_header("Content-Type", "text/html")
    self.send_header("Content-Length", str(len(page)))
    self.end_headers()
    self.wfile.write(page)

 #---------------------
if __name__ == '__main__':
  serverAddress = ('', 8080)
  #TypeErro: getsockaddrarag: AF_INET address must be tuple, not 'str'
  #server = http.server.HTTPServer(('', 8080), RequestHandeler)
  server = http.server.HTTPServer(serverAddress, RequestHandeler)
  server.serve_forever()