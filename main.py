import machine

from wifi_controller import WifiController
from bot_controller import WhatsappBot


if __name__ == "__main__":
    ssid = "IPhone Kyrylo"
    password = "Kempel7654"
    api_key = "2568235"
    phone = "420728372280"
    
    wifi = WifiController(ssid, password)
    whatsapp_bot = WhatsappBot(api_key)
    
    # TODO: fix the wifi connection part
    if not wifi.connect():
        print("Not connected")
        raise Exception()
    else:
        print(":D")
    
    