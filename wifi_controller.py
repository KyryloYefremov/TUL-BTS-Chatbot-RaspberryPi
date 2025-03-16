from time import sleep
import network


class WifiController:
    
    def __init__(self, ssid: str, password: str):
        self._ssid = ssid
        self._password = password
        
    def connect(self, connection_timeout=10) -> bool:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # connect to your network
        wlan.connect(self._ssid, self._password)
        
        # wait for Wi-Fi connection
        while connection_timeout > 0:
            if wlan.status() >= 3:
                break
            connection_timeout -= 1
            print('Waiting for Wi-Fi connection...')
            sleep(1)
            
        # check if connection is successful
        if wlan.status() != 3:
            return False
        else:
            print('Connection successful!')
            network_info = wlan.ifconfig()
            print('IP address:', network_info[0])
            return True
