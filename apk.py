from ppadb.client import Client as adb
import concurrent.futures, random, imaplib, email
from time import sleep, time

'''with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(getdata, a) for a in arr]'''



class BurnerMaker:
    def __init__(self):
        self.client = adb(host="127.0.0.1", port=5037) 
        self.devices = self.client.devices()
        self.apk = "cock.apk"
        self.res = [960, 540]
        self.clicks = (514, 249)
        self.chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '"', '#', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '@', '[', ']', '^', '_', '{', '}']

    def mp(self, cmd):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(cmd, dev) for dev in self.devices]
        
    def refresh(self):
        self.client = adb(host="127.0.0.1", port=5037)
        self.devices = self.client.devices() 

    def install(self, dev):
        dev.install(self.apk)
    
    def calctuple(self, dev, x, y):
        return (x, y)
    
    def click(self, dev):
        dev.shell("input touchscreen tap {} {}".format(self.clicks[0], self.clicks[1]))
    
    def clickat(self, dev, x, y):
        #a, b = self.calctuple(dev, x, y)
        dev.shell("input touchscreen tap {} {}".format(x, y))
    
    def hold(self, dev, x, y, time):
        #a, b = self.calctuple(dev, x, y)
        dev.shell("input touchscreen swipe {} {} {} {} {}".format(x, y, x, y, time))
    
    def makename(self, dev):
        i = random.randint(4, 14)
        s = ''
        for j in range(i):
            s+=random.choice(self.chars)
        print(s)
        dev.shell("input keyboard text {}".format(s))
    
    def write(self, dev, st):
        dev.shell("input keyboard text {}".format(st))
    
    def home(self, dev):
        dev.shell("input keyevent KEYCODE_HOME")

    def back(self, dev):
        dev.shell("input keyevent KEYCODE_BACK")
    
    def appmenu(self, dev):
        dev.shell("input keyevent KEYCODE_APP_SWITCH")
    
    def open(self, dev):
        #.723, .313
        x, y = 960*.723, 540*.313
        dev.shell("input touchscreen tap {} {}".format(x, y))

    def popup(self, dev):
        x, y = 960*.640, 540*.200
        dev.shell("input touchscreen tap {} {}".format(x, y))

    def clearapps(self, dev):
        x, y = 960*.723, 540*.100
        dev.shell("input touchscreen tap {} {}".format(x, y))
    
    def make_email(self):
        emaill = "projectgui/old.txt"
        with open(emaill) as f:
            z = f.read()
            first = z[0:13]
            last = z[-11:]
            zz = z.split(first)
            zzz = zz[1].split(last)
            num = zzz[0]
            letter = num[0]
            nums = num[1:]
        alpha = [chr(i) for i in range(97, 123)]
        if int(nums) < 99:
            i_num = int(nums)+1
            nums = str(i_num)
        else:
            al = alpha.index(letter)
            al += 1
            letter = alpha[al]
            nums = '1'
        newmail = first+letter+nums+last
        with open(emaill, 'w') as f:
            f.write(newmail)
        return newmail

    def connect2scid(self, devall):
        if devall == ("all"):
            for dev in self.devices:
                emaill = self.make_email()
                self.clickat(dev, 469, 179)
                self.write(dev, emaill)
                self.clickat(dev, 469, 230)
                self.write(dev, emaill)
                self.clickat(dev, 808, 334)
                recent = "projectgui/recent.txt"
                with open(recent) as f:
                    recentcode = f.read()
                code1 = recentcode
                code2 = recentcode
                s = time()
                e = time()
                while (code1 == recentcode or code2 == recentcode) and e-s <= 6:
                    host = 'imap.gmail.com'
                    username = ''
                    password = ''
                    mail = imaplib.IMAP4_SSL(host)
                    mail.login(username, password)
                    mail.select('inbox')
                    _, search_data = mail.search(None, 'ALL')
                    num1 = search_data[0].split()[-1]
                    num2 = search_data[0].split()[-2]
                    _, data1 = mail.fetch(num1, '(BODY.PEEK[HEADER])')
                    _, data2 = mail.fetch(num2, '(BODY.PEEK[HEADER])')
                    _, b1 = data1[0]
                    _, b2 = data2[0]
                    e_m1 = email.message_from_bytes(b1)
                    e_m2 = email.message_from_bytes(b2)
                    it1 = e_m1.items()
                    it2 = e_m2.items()
                    subject1 = it1[16][1]
                    subject2 = it2[16][1]
                    code1 = subject1[-8:-1]
                    code2 = subject2[-8:-1]
                    code1 = code1.replace(' ', '')
                    code2 = code2.replace(' ', '')
                    try:
                        int(code1)
                        with open(recent, 'w') as f:
                            f.write(code1)
                        code = code1
                    except:
                        int(code2)
                        with open(recent, 'w') as f:
                            f.write(code2)
                        code = code2
                    e=time()
                self.clickat(dev, 530, 291)
                self.write(dev, code)
                self.clickat(dev, 800, 358)
        else:
            emaill = self.make_email()
            self.clickat(devall, 469, 179)
            self.write(devall, emaill)
            self.clickat(devall, 469, 230)
            self.write(devall, emaill)
            self.clickat(devall, 808, 334)
            recent = "projectgui/recent.txt"
            with open(recent) as f:
                recentcode = f.read()
            code1 = recentcode
            code2 = recentcode
            s = time()
            e = time()
            while (code1 == recentcode or code2 == recentcode) and e-s <= 6:
                host = 'imap.gmail.com'
                username = ''
                password = ''
                mail = imaplib.IMAP4_SSL(host)
                mail.login(username, password)
                mail.select('inbox')
                _, search_data = mail.search(None, 'ALL')
                num1 = search_data[0].split()[-1]
                num2 = search_data[0].split()[-2]
                _, data1 = mail.fetch(num1, '(BODY.PEEK[HEADER])')
                _, data2 = mail.fetch(num2, '(BODY.PEEK[HEADER])')
                _, b1 = data1[0]
                _, b2 = data2[0]
                e_m1 = email.message_from_bytes(b1)
                e_m2 = email.message_from_bytes(b2)
                it1 = e_m1.items()
                it2 = e_m2.items()
                subject1 = it1[16][1]
                subject2 = it2[16][1]
                code1 = subject1[-8:-1]
                code2 = subject2[-8:-1]
                code1 = code1.replace(' ', '')
                code2 = code2.replace(' ', '')
                try:
                    int(code1)
                    with open(recent, 'w') as f:
                        f.write(code1)
                    z = 1
                except:
                    int(code2)
                    with open(recent, 'w') as f:
                        f.write(code2)
                    z = 0
                e=time()
            code = code1 if z else code2
            self.clickat(devall, 530, 291)
            self.write(devall, code)
            self.clickat(devall, 800, 358)


    def do_tutorial(self, dev):
        self.click(dev)
        self.click(dev)
        self.click(dev)
        self.click(dev)
        self.clickat(dev, 894, 464)
        sleep(1)
        self.clickat(dev, 478, 328) #initial cannon
        self.clickat(dev, 426, 171)
        self.clickat(dev, 480, 436)
        sleep(1.5)
        self.clickat(dev, 534, 434)
        sleep(15)
        self.click(dev)
        self.click(dev)
        self.click(dev)
        sleep(1)
        self.clickat(dev, 353, 339)
        sleep(3)
        self.clickat(dev, 138, 483) #wizard battle
        self.hold(dev, 444, 225, 2000) #hold wiz
        sleep(12)
        self.clickat(dev, 484, 476) #go home
        sleep(1)
        self.click(dev) 
        self.clickat(dev, 894, 464) #bhut
        sleep(1)
        self.clickat(dev, 478, 328)
        self.clickat(dev, 518, 98)
        self.click(dev) 
        self.clickat(dev, 894, 464) #elix collector
        sleep(1)
        self.clickat(dev, 478, 328) 
        self.clickat(dev, 446, 256)
        self.clickat(dev, 480, 436)
        self.click(dev) 
        self.click(dev) 
        self.clickat(dev, 894, 464) #elix storage
        sleep(1)
        self.clickat(dev, 478, 328)
        self.clickat(dev, 658, 173)
        self.clickat(dev, 480, 436)
        self.click(dev) 
        self.clickat(dev, 894, 464) #gold storage
        sleep(1)
        self.clickat(dev, 478, 328)
        self.clickat(dev, 423, 65)
        self.clickat(dev, 480, 436)
        self.click(dev) 
        self.clickat(dev, 894, 464)
        sleep(2)
        self.clickat(dev, 98, 319) #barracks
        self.clickat(dev, 346, 229)
        self.clickat(dev, 480, 436)
        self.clickat(dev, 530, 440)
        self.hold(dev, 94, 324, 2000) #train barbs
        self.clickat(dev, 714, 233) #gem barbs
        self.click(dev) #exit training menu
        sleep(.5)
        self.clickat(dev, 60, 466) #click battle
        sleep(.5)
        self.clickat(dev, 648, 349) #click attack
        self.clickat(dev, 138, 483) #click barbs
        self.hold(dev, 300, 255, 4500) #hold barbs
        sleep(15) 
        self.clickat(dev, 484, 476) #go home
        sleep(1)
        self.click(dev) 
        self.makename(dev)
        self.clickat(dev, 479, 171)
        self.click(dev) 
        self.clickat(dev, 600, 366) #age thingy
        self.clickat(dev, 600, 366)
        self.clickat(dev, 600, 446)
        self.clickat(dev, 505, 300)
        self.clickat(dev, 531, 441)
        self.clickat(dev, 484, 475)
        self.clickat(dev, 584, 434)
        self.click(dev) 
        self.clickat(dev, 36, 31)
        self.clickat(dev, 914, 380)
        self.click(dev) 
        self.clickat(dev, 921, 390)
        self.clickat(dev, 740, 95)
        self.clickat(dev, 921, 38)
        self.clickat(dev, 768, 425)
        self.clickat(dev, 815, 300)
        self.clickat(dev, 469, 179)
        self.clickat(dev, 469, 230)
        self.clickat(dev, 808, 334)

if __name__ == "__main__":
    z = BurnerMaker()
