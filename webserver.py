import socket
import random
import urequests
import utime
import gc


class WebServer:
    
    def __init__(self, ip, pico, wifi, weather_api):
        self.pico = pico        # instance of Pico
        self.wifi = wifi        # instance of wifi controller
        self.wapi = weather_api # apikey for weather API
        self.start_time = None  # to save the time of starting the server, activate in self.run()
        self.clients = []       # list to store connected clients
        
        # set up socket and start listening
        addr = socket.getaddrinfo(ip, 80)[0][-1]
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(addr)
        self.s.listen()
        print('Listening on', addr)
        
    def run(self):
        # init starting time
        self.start_time = utime.time()
        
        # Main loop to listen for connections
        while True:
            try:
                conn, addr = self.s.accept()
                print('Got a connection from', addr)
                
                self.clients.append(addr)  # store connected client
                
                # Receive and parse the request
                request = conn.recv(1024)
                request = str(request)
                print('Request content = %s' % request)

                try:
                    request = request.split()[1]
                    print('Request:', request)
                except IndexError:
                    pass
                
                ### Process the request and update variables ###
                if request == '/ipconfig':
                    response_body = self.wifi.ipconfig()
                    response_code = '200 OK'
                # request to toggle the pico led
                elif request == '/toggle':  
                    print("Toggle LED")
                    self.pico.toggle_led()
                    response_code = '200 OK'
                    response_body = 'LED toggled'
                # request to get temperature from pico sensors
                elif request == '/temp':  
                    print("Read temperature from Pico")
                    tempC = self.pico.read_internal_temperature()
                    response_code = '200 OK'
                    response_body = f"Temperature: {tempC}"
                    print(response_body)
                # get server status: uptime, memory usage, active connections
                elif request == '/status':  
                    response_code, response_body = self._get_status_info()
                # get server connected clients
                elif request == '/clients':  
                    response_code, response_body = self._get_connected_clients()
                # generate random value
                elif request == '/value': 
                    random_value = random.randint(0, 20)
                    response_code = '200 OK'
                    response_body = f"Random value: {random_value}"
                    print(response_body)
                # get weather for specific city
                elif request.startswith('/weather'):  
                
                    parts = request.split('/')
                    city = "Liberec"  # Default city
                    if len(parts) > 2 and parts[2]:  # if a city is provided in the URL
                        city = str(parts[2])
                        
                    print(f"City parameter: {city}")
                    response_code, response_body = self._get_weather_from_api(city)
                elif request == '/joke':
                    response_code, response_body = self._get_random_joke()
                    print(response_body)
                # if ther request didn't match anything - return as not found route
                else:  
                    response_body = "Not Found"
                    response_code = "404 Not Found"
                    
    
                # Send the HTTP response and close the connection
                response = f'HTTP/1.1 {response_code}\r\nContent-type: text/plain\r\n\r\n{response_body}'
                conn.send(response)
                conn.close()
                
                print('\n' + '-'*40)

            except OSError as e:
                conn.close()
                print('Connection closed')
                
    def _get_weather_from_api(self, city="Liberec") -> tuple:
        # Latitude and longitude for Liberec
        if city == "Liberec":
            lat, lon = 50.76, 15.06
        else:
            lat, lon = self._get_city_lat_lon_from_api(city)

            
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.wapi}&units=metric'
        response = urequests.get(url)
        # check if request was successful => process data
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            temp_max, temp_min = data['main']['temp_max'], data['main']['temp_min']
            wind_speed = data['wind']['speed']
            
            response_code = '200 OK'
            response_body = f"Weather for {city}:\n Temperature now: {temp}C, feels like: {feels_like}C, \nMin|Max temperature at the moments: {temp_min}C|{temp_max}C, wind speed: {wind_speed} m/s"
        # if not, return "400 Bad Request"
        else:
            response_body = "Bad Request"
            response_code = "400 Bad Request"
        
        return response_code, response_body
    
    def _get_city_lat_lon_from_api(self, city: str) -> tuple:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.wapi}'
        response = urequests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            lat = data['coord']['lat']
            lon = data['coord']['lon']
        else:
            lat, lon = None, None
        
        return lat, lon
    
    def _get_status_info(self) -> tuple:
        uptime = utime.time() - self.start_time  # calculate uptime
        free_mem = gc.mem_free()  # get free memory
        active_conns = len(self.clients)  # get active client count
        
        response_code = "200 OK"
        response_body = f"Server Uptime: {uptime} sec\nFree Memory: {free_mem} bytes\nActive Connections: {active_conns}"
        
        return response_code, response_body

    def _get_connected_clients(self) -> tuple:
        response_code = "200 OK"
        response_body = "Connected Clients:\n" + "\n".join([str(client) for client in self.clients])
        return response_code, response_body
    
    def _get_random_joke(self) -> tuple:
        url = 'https://official-joke-api.appspot.com/random_joke'
        response = urequests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            setup = data['setup']
            punchline = data['punchline']
            response_code = '200 OK'
            response_body = f'Joke of the day: \n{setup} \n- {punchline} :D'
        # if not, return "400 Bad Request"
        else:
            response_body = "Bad Request"
            response_code = "400 Bad Request"
        
        return response_code, response_body
        

        






