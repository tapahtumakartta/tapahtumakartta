# Import modules
import http.server
import socketserver

# Run an arbitrary port to which the server points
# using an apache2 proxy
PORT = 6000

# Setup a server handler
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    # Start the server
    print("Listening on port", PORT)
    httpd.serve_forever()
