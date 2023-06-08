from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import zpool_extractor

hostName = "localhost"
serverPort = 8242

class ZpoolWatcherServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get the zpool status.
        stream = os.popen('zpool status')
        output = stream.readlines()

        # Convert it to JSON.
        json_string = ExtractJson(output)

        # Return it back to the caller.
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), ZpoolWatcherServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")