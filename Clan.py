import urllib.request, json, os, dotenv


dotenv.load_dotenv()
if os.name == "nt":
    k = os.getenv("homeoffice")
else:
    k = os.getenv("pi")

class Clan:
    def __init__(self, tag):
        from Account import client
        self.key = k.rstrip('\n')
        self.tag = tag
        if self.tag[0] == '#':
            self.tag = self.tag[1:]
        self.url = "https://api.clashofclans.com/v1"
        self.endpoint = '/clans/%23'+self.tag
        self.email = os.getenv("email")
        self.passw = os.getenv("pass")
        self.client = client


    async def get_data(self):
        self._clandata = await self.client.get_clan(self.tag)
        self.name = self._clandata.name
        self.tag = self._clandata.tag
        self.access = self._clandata.type
        self.local = self._clandata.location
        if not self.local:
            self.local = "Not set"
        else:
            self.local = self.local.name
        self.level = self._clandata.level
        self.cuplimit = self._clandata.required_trophies
        self.points = self._clandata.points
        self.streak = self._clandata.war_win_streak
        self.wins = self._clandata.war_wins
        self.ispublic = self._clandata.public_war_log
        self.league = self._clandata.war_league
        self.nummems = self._clandata.member_count
        self.memlist = self._clandata.members
        self.clanmembers = ''
        self.memtags = ''
        self.description = self._clandata.description
        if self.ispublic:
            self.ties = self._clandata.war_ties
            self.losses = self._clandata.war_losses
        for i in self.memlist:
            self.clanmembers += 'Tag: ' + \
                i.tag + ' Name: ' + i.name + '\n'
            if i.role == "leader":
                self.leader = i
        for i in self.memlist:
            self.memtags += '{}\n'.format(i.tag)
        self.dead = False
        self.coslink = "https://www.clashofstats.com/clans/{}/summary".format(self.tag[1:])
        self.cclink = "https://www.kuilin.net/cc_n/clan.php?tag={}".format(self.tag[1:])
        self.openlink = "https://link.clashofclans.com/en?action=OpenClanProfile&tag={}".format(self.tag[1:])

    async def limitedtag(self, length):
        self.limitedtaglist = ''
        self.puretaglist = ''
        if length >= 3:
            for i in self.memlist:
                if len(i.tag[1:]) > length:
                    continue
                else:
                    self.limitedtaglist += "Tag: {} Name {}\n".format(
                        i.tag, i.name)
                    self.puretaglist += "{}\n".format(i['tag'])
            return (self.limitedtaglist, self.puretaglist)
        else:
            raise ValueError("Length is too short.")
