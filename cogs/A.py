import requests
import json
import discord
import os
import urllib.request
import pyautogui
import psutil
import sys
import concurrent.futures
import asyncio
import aiohttp
import random
from ast import literal_eval
from bs4 import BeautifulSoup
from datetime import datetime
from difflib import SequenceMatcher
from discord.flags import Intents
from discord.ext import commands, tasks
from discord.errors import ClientException
from discord.utils import get
from dotenv import load_dotenv as dotenv
from itertools import cycle
from multiprocessing import Process
from PIL import Image
from time import time, sleep
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from aiofile import async_open
import ujson

try:
    sys.path.append("..")
    from fakekc import fakekc
    from receipt import photoshop
    from fullreceipt import photoshop2
    from profiledisplay import iImage
    from Account import Account
    from Clan import Clan
    from Devices import Devices
    from Legend import Legend
    from Yopmail import Yopmail
    from Logs import Logging, Sum
    from Rank import Rank
except:
    pass


dotenv()
if os.name == "nt":
    k = os.getenv("homeoffice")
else:
    k = os.getenv("pi")

arrym = ['2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
         '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
         '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
         '2021-01', '2021-02', '2021-03', '2021-04']


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = data[0]['q'] + " -" + data[0]['a']
    return quote


def random_hex():
    return random.randint(0, 16777215)


def is_dead(tag):
    z = Account(tag)
    if z.league == 'Leagueless' and z.donated == 0 and z.donations == 0:
        return True
    return False


def sanitize(url):
    url2 = url.split("/")
    return f"{url2[4]}-{url2[5]}"


def blacklisted(tag):
    with open("jsondata/private.json") as f:
        blacklist = json.load(f)
    if tag[0] != "#":
        tag = "#"+tag
    tag = tag.upper()
    return True if tag in blacklist else False


def nmonth2smonth(m):
    arr = ['January', 'February', 'March', 'April', 'May', 'June',
           'July', 'August', 'September', 'October', 'November', 'December']
    z = int(m)
    return arr[z-1]


def backwardscountrycode(code):
    with open("jsondata/countries.json") as f:
        data = json.load(f)
    for k in data:
        if k == code:
            return data[k]

async def get_seasons(tag, start, end):
    s = time()
    ncs = set()
    sttr = dict()

    async def data4thatseason(season, tag):
        async with aiohttp.ClientSession() as session:
            async with async_open("jsons3/{}.json".format(season), 'r', encoding='utf-8') as f:
                data = ujson.loads(await f.read())
            if tag[0] != "#":
                tag = "#"+tag
            tag = tag.upper()
            tag = tag.replace('\u200b', '')
            if tag in data:
                ncs.add(data[tag]['name'])
                zz = data[tag]
                sttr[f'{nmonth2smonth(season[5:])} {season[:4]}'] = "{}\n".format(
                    zz['name'])
            return 0
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[data4thatseason(u, tag) for u in arrym[start:end]])
    arrym2 = ["{} {}".format(nmonth2smonth(i[5:]), i[:4]) for i in arrym]
    order = [(k, sttr[k]) for k in arrym2 if k in sttr.keys()]
    e = time()
    return dict(order), ncs
