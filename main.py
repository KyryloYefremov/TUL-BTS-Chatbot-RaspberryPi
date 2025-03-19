import machine

from wifi_controller import WifiController
from bot_controller import WhatsappBot


if __name__ == "__main__":
    ssid = 'IPhone Kyrylo'
    password = 'Kempel7654'
#    api_key = '2568235'
    api_key = 'EVgBe9DPNRpE'
    phone = '420728372280'
    
    # init controllers
    wifi = WifiController(ssid, password)
    whatsapp_bot = WhatsappBot(api_key, phone)
    
    # try to establish the wifi connection
    if not wifi.connect():
        print("Not connected")
        raise Exception()
    else:
        print(":D\n")
        print("Sending message...")
        msg = 'Hello from the Raspberry Pi Pico'
        whatsapp_bot.send_message(msg)
        
        
    
    
