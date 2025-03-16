import requests


class WhatsappBot:
    
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._url = lambda phone, message = f'https://api.callmebot.com/whatsapp.php?phone={phone}&text={message}&apikey={self._api_key}'
        
        
    def send_message(self, dest_phone_number: str, message: str):
        # send a GET request on whatsapp API endpoint
        response = requests.get(self._url(dest_phone_number, message))
        
        # check if request was successful
        if response.status_code == 200:
            print("Success!")
        else:
            print("Error:")
            print(response.text)
