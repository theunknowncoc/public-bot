#!/usr/bin/python3
from main import bot, VERSION

def runbot():
    bot.run(VERSION)

if __name__ == "__main__":
    print(f"Version {VERSION}")
    runbot()
