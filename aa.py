import os

def DTB(num):
    return "{0:b}".format(num)

def get_binary(tag):
    b256 = os.popen('node decalc.js calc {}'.format(tag)).read()
    b256 =  b256.strip().split(",")
    b256 = [DTB(int((i.strip()))).zfill(8) for i in b256]
    b256 = "".join(b256)
    return b256

if __name__ == "__main__":
    while True:
        tag = input("tag\n")
        b256 = os.popen('node decalc.js calc {}'.format(tag)).read()
        b256 =  b256.strip().split(",")
        b256 = [DTB(int((i.strip()))).zfill(8) for i in b256]
        b256 = "".join(b256)
        print(b256)
        b = b256[:41]
        print(len(b))
        print(b)
