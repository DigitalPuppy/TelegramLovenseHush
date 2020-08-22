#! /usr/bin/env python3

import requests
import os
import sys
import time
import random


class lovense:
    def __init__(self, hostport):
        self.hostport = hostport
        # Toy scan
        res = requests.get("http://{}/GetToys".format(self.hostport))
        if res.status_code != 200:
            raise Exception("Bad status: {} : {}".format(res.status_code, res.text()))
        j = res.json()
        print(j)
        if len(j['data']) == 0:
            raise Exception('Connect OK but no toy found')
        self.toy = list(j['data'].keys())[0]
    def stop(self):
        res = requests.get("http://{}/Vibrate?v={}&t={}".format(self.hostport, 0, self.toy))
    def vibrate(self, speed, duration):
        res = requests.get("http://{}/Vibrate?v={}&t={}".format(self.hostport, speed, self.toy))
        if duration == '-':
            return
        time.sleep(int(duration))
        self.stop()
    def pattern(self, pattern, duration):
        res = requests.get("http://{}/Preset?v={}&t={}".format(self.hostport, pattern, self.toy))
        if duration == '-':
            return
        time.sleep(int(duration))
        self.stop()

class telegram:
    def __init__(self, botkey = None):
        if botkey is None:
            with open('.botkey', 'r') as f:
                botkey = f.read()
        self.botkey = 'bot' + botkey
        self.url = 'https://api.telegram.org'
        self.s = requests.session()
        print('hitting {}/{}/getMe'.format(self.url, self.botkey))
        res = self.s.get('{}/{}/getMe'.format(self.url, self.botkey))
        print(res.json())
        self.offset = 0
    def run(self):
        while True:
            res = self.s.get('{}/{}/getUpdates?offset={}&timeout=60'.format(self.url, self.botkey, self.offset))
            j = res.json()
            print(j)
            for u in j['result']:
                self.on_update(u)
                if self.offset < u['update_id'] + 1:
                    self.offset = u['update_id'] + 1
            time.sleep(1) # safety in case of error loop
    def send(self, channel, message):
        res = self.s.post('{}/{}/sendMessage'.format(self.url, self.botkey), json={'chat_id': channel, 'text': message})
        print(res.json())
    def on_update(self, u):
        pass

class hlt(telegram):
    def __init__(self, lovense_hostport, botkey=None):
        super().__init__(botkey)
        self.l = None
        if len(lovense_hostport):
            self.l = lovense(lovense_hostport)
    def on_update(self, u):
        if 'message' in u and u['message'] is not None:
            self.msg(u['message'])
        if 'channel_post' in u and u['channel_post'] is not None:
            self.msg(u['channel_post'])
    def msg(self, m):
        if 'text' in m:
            print(m['text'])
            t = m['text']
            ts = t.split(' ')
            if len(ts) > 0 and ts[0] == '!ping':
                self.send(m['chat']['id'], 'online and ready to serve!')
            if len(ts) > 0 and ts[0] == '!help':
                self.send(m['chat']['id'],
"""commands:
   !ping
   !vibrate intensity duration
   !pattern patternNubmer duration
   !random
   !stop
duration is in seconds and capped to 10 (or use '-' to leave on)
intensity is between 1 and 20
patternNumber is between 1 and 4
""")
            if len(ts) > 0 and ts[0] == '!random':
                if random.randint(0, 1):
                    p = random.randint(1, 4)
                    d = random.randint(3, 10)
                    self.send(m['chat']['id'], 'Go for pattern {} for {} seconds'.format(p, d))
                    self.l.pattern(p, d)
                    self.send(m['chat']['id'], 'bzzzt!')
                else:
                    s = random.randint(5, 20)
                    d = random.randint(3, 10)
                    self.send(m['chat']['id'], 'Go for vibrate at {} for {} seconds'.format(s, d))
                    self.l.vibrate(s, d)
                    self.send(m['chat']['id'], 'bzzzt!')
            if len(ts) > 0 and ts[0] == '!stop':
                self.l.stop()
                self.send(m['chat']['id'], 'stopped')
            if len(ts) > 2 and ts[0] == '!vibrate':
                try:
                    speed = int(ts[1])
                    duration = ts[2]
                    if duration != '-':
                        duration = int(ts[2])
                        if duration > 10:
                            duration = 10
                    self.l.vibrate(speed, duration)
                    self.send(m['chat']['id'], 'bzzzt!')
                except Exception as e:
                    pass
            if len(ts) > 2 and ts[0] == '!pattern':
                try:
                    speed = int(ts[1])
                    duration = ts[2]
                    if duration != '-':
                        duration = int(ts[2])
                        if duration > 10:
                            duration = 10
                    self.l.pattern(speed, duration)
                    self.send(m['chat']['id'], 'bzzzt!')
                except Exception as e:
                    pass

def randomfun(l, mininterval, maxinterval, minduration, maxduration):
    try:
        while True:
            time.sleep(random.randint(mininterval, maxinterval))
            if random.randint(0, 1):
                p = random.randint(1, 4)
                d = random.randint(minduration, maxduration)
                self.l.pattern(p, d)
            else:
                s = random.randint(5, 20)
                d = random.randint(minduration, maxduration)
                self.l.vibrate(s, d)
    except Exception:
        l.stop()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'locate':
        res = requests.get('https://api.lovense.com/api/lan/getToys')
        j = res.json()
        print(j)
        if len(j) != 0:
            k = list(j.keys())[0]
            print(j[k]['domain'] + ':' + str(j[k]['httpPort']))
    elif len(sys.argv) > 1 and sys.argv[1] == 'lovense':
        l = lovense(sys.argv[2])
        print("Lovense connected")
        if len(sys.argv) > 3:
            cmd = sys.argv[3]
            if cmd == 'stop':
                l.stop()
            elif cmd == 'vibrate':
                l.vibrate(sys.argv[4], sys.argv[5])
            elif cmd == 'pattern':
                l.pattern(sys.argv[4], sys.argv[5])
            elif cmd == 'randomfun':
                randomfun(l, int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
            else:
                raise Exception("Unknown command (stop, vibrate, pattern)")
    elif len(sys.argv) > 2 and sys.argv[1] == 'run':
        o = hlt(sys.argv[2])
        o.run()
    else:
        o = hlt('')
        o.run()