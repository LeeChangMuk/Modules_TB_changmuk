import requests
import time

class Colab_Alert:
    def __init__(self):
        self.TOKEN = "5812319562:AAF7H7EYLF0VK2p7HAdBbIVUlIbheAxcmeA"
        self.ID_URL = f"https://api.telegram.org/bot{self.TOKEN}/getUpdates"

    def sendMessage(chat_id, txt):
        token = self.TOKEN
        data = {"chat_id": int(chat_id), "text": txt}
        url = f"https://api.telegram.org/bot{token}/sendMessage?"
        res = requests.post(url, json=data)

    def getID(self):
        ck = 0;
        t = 1
        while (1):
            url = self.ID_URL
            res = requests.get(url)

            respond = res.json()["result"][-1]["message"]["text"]
            if respond == "/getID" and ck == 0:
                id = res.json()["result"][-1]["message"]["from"]["id"]
                sendMessage(id, id)
                sendMessage(id, "If you checked, please send \"OK\"")
                ck = 1
            if (
                    respond == "OK" or respond == "ok" or respond == "Ok" or respond == "oK" or respond == "ㅇㅋ") and ck != 0:
                id = res.json()["result"][-1]["message"]["from"]["id"]
                sendMessage(id, "\"OK\" Sign Checked.")
                break

            elif ck == 1:
                sendMessage(id, "Please send \"OK\"")
                t = 3
            time.sleep(t)