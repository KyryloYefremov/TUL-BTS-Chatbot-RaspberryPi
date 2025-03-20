from time import sleep
import network


class WifiController:
    
    def __init__(self, ssid: str, password: str):
        self._ssid = ssid
        self._password = password
        
    def connect(self, connection_timeout=10) -> bool:
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        # connect to your network
        self._wlan.connect(self._ssid, self._password)
        
        # wait for Wi-Fi connection
        while connection_timeout > 0:
            if self._wlan.status() >= 3:
                break
            connection_timeout -= 1
            print('Waiting for Wi-Fi connection...')
            sleep(1)
            
        # check if connection is successful
        if self._wlan.status() != 3:
            return False
        else:
            print('Connection successful!')
            network_info = self.ipconfig()
            print(network_info)
            return True
        
    def ipconfig(self):
        ip, subnet_mask, gateway, dns = self._wlan.ifconfig()
        info = f"Network ssid: {self._ssid}\nIP: {ip}\nSubnet mask: {subnet_mask}\nGateway: {gateway}\nDns: {dns}\n"
        return info
