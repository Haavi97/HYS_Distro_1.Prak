import socketserver



class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 6000 # 4000 + random.randrange(4000)

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyRequestHandler)

    print("Server started on port:", PORT)
    server.serve_forever()
    