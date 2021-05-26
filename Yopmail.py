from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


class Yopmail:
    def __init__(self, email):
        self.email = email
        self.url = "http://www.yopmail.com/en/inbox.php?login={}&p=1&d=&ctrl=&scrl=&spam=true&yf=005&yp=RAQD2AQtlBGR5ZGV1AQx5ZGx&yj=ZZwR4ZGplBQLlBGD1AwxmBGV&v=3.1&r_c=&id=".format(
            self.email)
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
            'referer':'https://www.google.com/'
        }
        self.req = Request(self.url)
        self.open = urlopen(self.req).read()
        self.soup = BeautifulSoup(self.open, 'lxml')
        self.a = self.soup.find_all("a")
        self.emails = [str(i).replace("span", "").replace(">", "").replace("<", "").replace("class=", "").replace("lms", "").replace(
            "lmf", "").replace("lmh", "").replace('"', "").replace("'", "").split() for i in self.a if self.email.lower() in str(i)]
        self.emails = [" ".join(
            i[-7:])[:-1] for i in self.emails if "Supercell" in i and "Complete" not in i][:4]
