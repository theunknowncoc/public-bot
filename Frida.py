from __future__ import print_function
import frida
import sys

session = frida.attach("notepad.exe")
script = session.create_script("send('Hello World!');")
def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()
