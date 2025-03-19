import machine

from wifi_controller import WifiController
from bot_controller import WhatsappBot


if __name__ == "__main__":
    ssid = 'IPhone Kyrylo'
    password = 'Kempel7654'
    api_key = '2568235'
    phone = '420728372280'
    
    # init controllers
    wifi = WifiController(ssid, password)
    whatsapp_bot = WhatsappBot(api_key)
    
    # try to establish the wifi connection
    if not wifi.connect():
        print("Not connected")
        raise Exception()
    else:
        print(":D")
        print("Sending message...")
        msg = 'Hello%20from%20the%20Raspberry%20Pi%20Pico%21'
        whatsapp_bot.send_message(phone, msg)
    
    