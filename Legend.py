import urllib.request, json, os
from dotenv import load_dotenv as dotenv

dotenv()
if os.name == "nt":
    k = os.getenv("windowskey")
else:
    k = os.getenv("linuxkey")

class Legend:
    def __init__(self, season=''):
        key = k.rstrip('\n')
        url = "https://api.clashofclans.com/v1"
        endpoint = '/leagues/29000022/seasons/'+season
        request = urllib.request.Request(
            url+endpoint,
            None,
            {
                "Authorization": "Bearer %s" % key
            }
        )
        response = urllib.request.urlopen(request).read().decode('UTF-8')
        data = json.loads(response)
        self.data = data
        self.players = self.data['items']
        self.rank1 = self.data['items'][0]
        self.ranklast = self.data['items'][-1]

    def __len__(self):
        return len(self.players)
