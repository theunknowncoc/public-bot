import json, os, coc
from dotenv import load_dotenv as dotenv
from Clan import Clan

dotenv()
if os.name == "nt":
    k = os.getenv("homeoffice")
else:
    k = os.getenv("pi")

client = coc.login(os.getenv("email"), os.getenv("pass"), key_names="deeznuts", key_count=5, throttle_limit=20)

class Account:
    def __init__(self, tag):
        self.key = k.rstrip('\n')
        self.tag = tag
        if self.tag[0] == '#':
            self.tag = self.tag[1:]
        self.url = "https://api.clashofclans.com/v1"
        self.endpoint = '/players/%23'+self.tag
        self.email = os.getenv("email")
        self.passw = os.getenv("pass")
        self.client = client
    
    async def get_data(self):
        #self.client = coc.login(self.email, self.passw, key_names="deeznuts", key_count=5, throttle_limit=20)
        self._playerdata = await self.client.get_player(self.tag)
        self.name = self._playerdata.name
        self.tag = self._playerdata.tag
        self.th = self._playerdata.town_hall
        self.xp = self._playerdata.exp_level
        self.pb = self._playerdata.best_trophies
        self.cups = self._playerdata.trophies
        self.donations = self._playerdata.received
        self.donated = self._playerdata.donations
        self.ws = self._playerdata.war_stars

        self.clanlocalemoji = False
        self.clanlocal = None
        self.hasclan = False
        self.dead = False

        if self._playerdata.clan:
            self._clandata = await self.client.get_clan(self._playerdata.clan.tag)
            self.clanname = self._clandata.name
            self.clanlevel = self._clandata.level
            self.clantag = self._clandata.tag
            self.hasclan = True
            self.clanmembersraw = self._clandata.members
            self.clanmembers = "".join([f"Tag: {i.tag} Name: {i.name}\n" for i in self.clanmembersraw])
            self.clanbadgeurl = self._clandata.badge.url
            self.clanlocal = self._clandata.location if self._clandata.location else "Not set"
            with open("jsondata/countries.json") as f:
                data = json.load(f)
            for k in data:
                if str(data[k]) == str(self.clanlocal):
                    self.clancountrycode = k
        else:
            self.clanlevel = 'Not in a clan'
            self.clantag = 'None'
            self.clanbadgeurl = False
            self.clanname = 'Not in a clan'

        self.bk = 0
        self.aq = 0
        self.gw = 0
        self.rc = 0 
        if (_ := self._playerdata.heroes):
            self.heroes = _
            self.herodict = dict()
            for idx in self.heroes:
                self.herodict[idx.name] = (idx.level, idx.max_level)
            if "Barbarian King" in self.herodict:
                self.bk = self.herodict['Barbarian King'][0]
            if "Archer Queen" in self.herodict:
                self.aq = self.herodict['Archer Queen'][0]
            if "Grand Warden" in self.herodict:
                self.gw = self.herodict['Grand Warden'][0]
            if "Royal Champion" in self.herodict:
                self.rc = self.herodict['Royal Champion'][0]
                
        if not (_ := self._playerdata.builder_hall):
            self.bh = "Boat not built"
        else:
            self.bh = _

        self.league = self._playerdata.league
        self.leagueurl = self._playerdata.league.icon.url if self._playerdata.league.icon.url else "https://api-assets.clashofclans.com/leagues/72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png"
        if str(self.league) == "Unranked" and self.donated == 0 and self.donations == 0:
            self.dead = True

        if (_ := self._playerdata.legend_statistics):
            self.legendinfo = _ 
            self.bestrank = self.legendinfo.best_season
            self.currentrank = self.legendinfo.current_season
            self.previousrank = self.legendinfo.previous_season
            self.legendcups = self.legendinfo.legend_trophies
        self.coslink = "https://www.clashofstats.com/players/{}/summary".format(self.tag[1:])
        self.cclink = "https://www.kuilin.net/cc_n/member.php?tag={}".format(self.tag[1:])
        self.openlink = "https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={}".format(self.tag[1:])
        self.clancoslink = "https://www.clashofstats.com/players/{}/summary".format(self.clantag[1:])
        self.clancclink = "https://www.kuilin.net/cc_n/member.php?tag={}".format(self.clantag[1:])
        self.clanopenlink = "https://link.clashofclans.com/en?action=OpenPlayerProfile&tag={}".format(self.clantag[1:])
    
    async def get_clan_data(self, tag, limit: int):
        self._clandata = await self.client.get_clan(tag)
        self.clanmembersraw = self._clandata.members
        self.clanmembers = "".join([f"Tag: {i.tag} Name: {i.name}\n" for i in self.clanmembersraw if len(i.tag) <=limit+1])

    @staticmethod
    async def get_top(corp, local, start, taglimit: int, before="", after=""):
        with open('jsondata/coscountry.json') as f:
            data = json.load(f)
        dataog = dict()
        counter = 32000006
        for i in data.keys():
            dataog[i] = counter
            counter += 1
        local = dataog[local]
        if corp.lower() in ["clans", "clan"]:
            top = await client.get_location_clans(location_id=local, limit=start)
        else:
            top = await client.get_location_players(location_id=local, limit=start)
        str2rtn = ""
        for rankedplayer in top:
            if len(rankedplayer.tag)-1 <= taglimit:
                str2rtn += "Tag: "+rankedplayer.tag+" Name: "+rankedplayer.name+"\n"
        return str2rtn
    
    @staticmethod
    async def searchclans(name, minLevel, local, minMembers, maxMembers) -> str:
        with open('jsondata/coscountry.json') as f:
            data = json.load(f)
        dataog = dict()
        counter = 32000006
        for i in data.keys():
            dataog[i] = counter
            counter += 1
        error = False
        if minLevel < 2 and minLevel != 0:
            error = True
            return "Error, minLevel must be greater than 1"
        if minMembers < 2 and minMembers != 0:
            return "Error, minMembers must be greater than 1"
        if maxMembers < minMembers:
            return "Error, maxMembers needs to be bigger than or equal to min members"
        if local not in dataog and local != "x":
            return "Error, local needs to be a capitalized two-letter country code, like US"
        if local != "x":
            local = dataog[local]
        
        if True:
            if name != "x":
                if minLevel != 0:
                    if minMembers != 0:
                        if maxMembers != 0 and maxMembers >= minMembers:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local, min_members=minMembers, max_members=maxMembers, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(name=name, min_members=minMembers, max_members=maxMembers, min_clan_level=minLevel)
                        else:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local, min_members=minMembers, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(name=name, min_members=minMembers, min_clan_level=minLevel)
                    else:
                        if maxMembers != 0:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local, max_members=maxMembers, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(name=name, max_members=maxMembers, min_clan_level=minLevel)
                        else:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(name=name, min_clan_level=minLevel)
                else:
                    if minMembers != 0:
                        if maxMembers != 0 and maxMembers >= minMembers:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local, min_members=minMembers, max_members=maxMembers)
                            else:
                                z = await client.search_clans(name=name, min_members=minMembers, max_members=maxMembers)
                        else:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local, min_members=minMembers)
                            else:
                                z = await client.search_clans(name=name, min_members=minMembers)
                    else:
                        if maxMembers != 0:
                            if local != "x":
                                z = await client.search_clans(name=name, max_members=maxMembers, location_id=local)
                            else:
                                z = await client.search_clans(name=name, max_members=maxMembers)
                        else:
                            if local != "x":
                                z = await client.search_clans(name=name, location_id=local)
                            else:
                                z = await client.search_clans(name=name)
            else:
                if minLevel != 0:
                    if minMembers != 0:
                        if maxMembers != 0 and maxMembers >= minMembers:
                            if local != "x":
                                z = await client.search_clans(location_id=local, min_members=minMembers, max_members=maxMembers, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(min_members=minMembers, max_members=maxMembers, min_clan_level=minLevel)
                        else:
                            if local != "x":
                                z = await client.search_clans(location_id=local, min_members=minMembers, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(min_members=minMembers, min_clan_level=minLevel)
                    else:
                        if maxMembers != 0:
                            if local != "x":
                                z = await client.search_clans(location_id=local, max_members=maxMembers, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(max_members=maxMembers, min_clan_level=minLevel)
                        else:
                            if local != "x":
                                z = await client.search_clans(location_id=local, min_clan_level=minLevel)
                            else:
                                z = await client.search_clans(min_clan_level=minLevel)
                else:
                    if minMembers != 0:
                        if maxMembers != 0 and maxMembers >= minMembers:
                            if local != "x":
                                z = await client.search_clans(location_id=local, min_members=minMembers, max_members=maxMembers)
                            else:
                                z = await client.search_clans(min_members=minMembers, max_members=maxMembers)
                        else:
                            if local != "x":
                                z = await client.search_clans(location_id=local, min_members=minMembers)
                            else:
                                z = await client.search_clans(min_members=minMembers)
                    else:
                        if maxMembers != 0:
                            if local != "x":
                                z = await client.search_clans(max_members=maxMembers, location_id=local)
                            else:
                                z = await client.search_clans(max_members=maxMembers)
                        else:
                            if local != "x":
                                z = await client.search_clans(location_id=local)
                            else:
                                z = 0
        returnz = []
        async for clan in client.get_clans([i.tag for i in z]):
            if len(returnz) >= 50:
                break
            for member in clan.members:
                if len(returnz) >= 50:
                    break
                if str(member.role) == "Leader" and str(member.league) == "Unranked" and int(member.received) == 0 and int(member.donations) == 0:
                    returnz.append("Tag: "+clan.tag+" Name: "+clan.name+"\n")
                elif str(member.role) == "Leader":
                    break
        del z
        return "".join(returnz) if "".join(returnz) else "None"
    
    @staticmethod
    async def get_war_log(tag) -> dict:
        ClanLog = await client.get_warlog(tag)
        retval = dict()
        retval['sttr'] = f'**{ClanLog[0].clan}**\n'
        retval['embed'] = f'**{ClanLog[0].clan}**\n'
        total: int = len(ClanLog)
        wins: int = 0
        losses: int = 0
        i = 0
        for clan in ClanLog:
            print(i)
            #print(clan.opponent.name)
            print(clan.clan.destruction)
            print(clan.opponent.destruction)
            i+=1
            if clan.result == "win":
                WL = "✅"
                wins += 1
            else:
                WL = "❌"
                losses += 1
            sttr = f"{clan.team_size}v{clan.team_size} {WL} {clan.opponent} {clan.end_time.time.month}/{clan.end_time.time.day}/{clan.end_time.time.year}\n"
            retval['embed'] += sttr
            retval['sttr'] += sttr
        retval['embed'] += "{}% win rate".format(wins/total*100)
        retval['sttr'] += "{}% win rate".format(wins/total*100)

        return retval

    def __str__(self) -> str:
        return self.tag
