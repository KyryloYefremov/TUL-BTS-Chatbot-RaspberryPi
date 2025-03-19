import machine

from wifi_controller import WifiController
from pico_controller import PicoController
from webserver import WebServer


if __name__ == "__main__":
    ssid = 'IPhone Kyrylo'
    password = 'Kempel7654'
    
    # init controllers
    wifi = WifiController(ssid, password)
    pico = PicoController()
    
    # try to establish the wifi connection
    if not wifi.connect():
        print("Not connected")
        raise Exception()
    else:
        print(":D\n")
        server = WebServer('172.20.10.2', pico=pico)
        
        server.run()
        
    
    
