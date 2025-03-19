import urequests


class WhatsappBot:
    
    def __init__(self, api_key: str, phone_number: str):
        self._api_key = api_key
        self._dest_phone = phone_number
        
    def send_message(self, message: str):
        # send a GET request on whatsapp API endpoint
        prepared_msg = self._prepare_message(message)
        url = f'http://api.textmebot.com/send.php?recipient={self._dest_phone}&apikey={self._api_key}&text={prepared_msg}'
        response = urequests.get(url)
        
        # check if request was successful
        if response.status_code == 200:
            print("Success!")
        else:
            print("Error:")
            print(f"URL: {url}")
            print(response.text)            
            
    def _prepare_message(self, message: str) -> str:
        split_symbol = '%20'
        end_symbol = '%21'
        prepared_msg = message.replace(' ', split_symbol) + end_symbol
        return prepared_msg


if __name__ == "__main__":
    bot = WhatsappBot('2568235', '420728372280')
    bot.send_message('Hello my name is Kyrylo')
#    res = bot.prepare_message('Hello my name is Kyrylo')
#    print(res)

