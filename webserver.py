import socket
import random


class WebServer:
    
    def __init__(self, ip, pico):
        self.pico = pico
        # set up socket and start listening
        addr = socket.getaddrinfo(ip, 80)[0][-1]
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(addr)
        self.s.listen()
        print('Listening on', addr)
        
    def run(self):
        # Initialize variables
        state = "OFF"
        random_value = 0
        
        # Main loop to listen for connections
        while True:
            try:
                conn, addr = self.s.accept()
                print('Got a connection from', addr)
                
                # Receive and parse the request
                request = conn.recv(1024)
                request = str(request)
                print('Request content = %s' % request)

                try:
                    request = request.split()[1]
                    print('Request:', request)
                except IndexError:
                    pass
                
                # Process the request and update variables
                if request == '/toggle':
                    print("Toggle LED")
                    self.pico.toggle_led()
                    response_code = '200 OK'
                    response_body = 'LED toggled'
                elif request == '/temp':
                    print("Read temperature from Pico")
                    tempC = self.pico.read_internal_temperature()
                    response_code = '200 OK'
                    response_body = f"Temperature: {tempC}"
                    print(response_body)
                elif request == '/value':
                    random_value = random.randint(0, 20)
                    response_code = '200 OK'
                    response_body = f"Random value: {random_value}"
                    print(response_body)
                else:
                    response_body = "Not Found"
                    response_code = "404 Not Found"
                    
    
                # Send the HTTP response and close the connection
                response = f'HTTP/1.1 {response_code}\r\nContent-type: text/plain\r\n\r\n{response_body}'
                conn.send(response)
                conn.close()

            except OSError as e:
                conn.close()
                print('Connection closed')






