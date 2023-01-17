import requests
import time

class Colab_Alert:
    def __init__(self):
        self.TOKEN = "5812319562:AAF7H7EYLF0VK2p7HAdBbIVUlIbheAxcmeA"
        self.ID_URL = f"https://api.telegram.org/bot{self.TOKEN}/getUpdates"

    def sendMessage(self,chat_id, txt):
        token = self.TOKEN
        data = {"chat_id": int(chat_id), "text": txt}
        url = f"https://api.telegram.org/bot{token}/sendMessage?"
        res = requests.post(url, json=data)

    def getID(self, pw):
        pw = str(pw)
        ck = 0;
        t = 1
        while (1):
            url = self.ID_URL
            res = requests.get(url)

            respond = res.json()["result"][-1]["message"]["text"]
            id = res.json()["result"][-1]["message"]["from"]["id"]
            if respond == "/getID" and ck == 0:
                ck = 1

            elif ck == 1:
                self.sendMessage(id, "Send your password to check your chat_ID")
                while(1):
                  url = self.ID_URL
                  res = requests.get(url)
                  print("Send your PassWord")
                  respond = res.json()["result"][-1]["message"]["text"]
                  if respond == pw:
                    self.sendMessage(id, id)
                    ck=2
                    break
                  time.sleep(2)

            if ck==2: 
              print(f"Your chat_ID is [{id}]")
              break

            time.sleep(t)
