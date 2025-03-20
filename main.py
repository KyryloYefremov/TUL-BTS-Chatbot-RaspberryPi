import machine

from wifi_controller import WifiController
from pico_controller import PicoController
from webserver import WebServer

from config import *


if __name__ == "__main__":

    # init controllers
    wifi = WifiController(SSID, PASSWORD)
    pico = PicoController()
    
    # show that program was executed - blink the led
    pico.init_blink()
    
    # try to establish the wifi connection
    if not wifi.connect():
        print("Not connected")
        raise Exception()
    else:
        print(":D\n")
        server = WebServer('172.20.10.2', pico=pico, wifi=wifi, weather_api=WEATHER_API)
        
        server.run()
        
    
    
