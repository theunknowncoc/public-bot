import json
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

class Cos:
    def __init__(self, porc, name, strict: bool =False, thfilter="", page ="") -> None:
        self.url = "https://api.clashofstats.com/search/"
        self.endpoint = porc+"?"
        self.endpoint += "q="+name
        if page:
            self.endpoint += "&page="+page
        if strict:
            self.endpoint += "&nameEquality=true"
        else:
            self.endpoint += "&nameEquality=false"
        if thfilter:
            self.endpoint += "&th="+thfilter
        self.url += self.endpoint
        self.req = Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
        self.decode = urlopen(self.req).read()
        self.soup = BeautifulSoup(self.decode, 'lxml')
        self.json = json.loads(self.soup.text)
        self.items = self.json['items']
        for i in self.items:
            if 'townHallLevel' not in i:
                i['townHallLevel'] = "Unavailable"
            if 'warStars' not in i:
                i['warStars'] = "Unavailable"
        self.structdata = "\n".join([f"{i['tag']} {i['name']} TH: {i['townHallLevel']} XP: {i['expLevel']} WS: {i['warStars']}" for i in self.items])



