import requests
import re
import json
import qrcode
import base64
import os
import re
import time
import random
import hashlib
import threading
from PIL import Image
from websocket import create_connection

#2020-08-14

class Work():

    def __init__(self):
        self.res = requests.session()
        self.Code = ''
        self.QRurl = ''
        self.threadList = []
        self.appKey = '85A09F60A599F5E1867EAB915A8BB07F'

    def getCode(self):
        r = self.res.get(
            'https://login.dingtalk.com/user/qrcode/generate.jsonp?callback=angular.callbacks._0')
        html = re.findall('\((.*?)\)', r.text, re.S)[0]
        callback = json.loads(html)
        if callback['success'] == True:
            self.Code = callback['result']
            self.QRurl = 'http://qr.dingtalk.com/action/login?code='+self.Code
            return callback['result']
        else:
            print('Error01:返回值为否')

    def makeQRcode(self):
        img = qrcode.make(self.QRurl)
        with open('test.png', 'wb') as f:
            img.save(f)
        im = Image.open('test.png')
        im.show()

    def makedata(self):
        data = {
            'data': '106!woxiangqiaoni',
            'xa': 'dingding',
            'xt': ''
        }
        r = self.res.post('https://ynuf.aliapp.org/service/um.json', data=data)
        _ = r.json()
        self.tn = _['tn']
        self.id = _['id']

    def checkIfLogined(self):
        url = 'https://login.dingtalk.com/user/qrcode/is_logged.jsonp'
        params = {
            'appKey': '85A09F60A599F5E1867EAB915A8BB07F',
            'callback': None,
            'pdmModel': 'Windows Unknown',
            'pdmTitle': 'Windows Unknown Web',
            'pdmToken': self.tn,
            'qrcode': self.Code
        }
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://im.dingtalk.com/',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        while True:
            r = self.res.get(url, params=params, headers=headers)

            _ = json.loads(re.findall('\((.*?)\)', r.text, re.S)[0])

            if _['success'] == True:
                break
            time.sleep(2)

        os.remove('test.png')
        self.accessToken = _['result']['accessToken']
        self.appKey = _['result']['appKey']
        self.tmpCode = _['result']['tmpCode']
        self.openId = str(_['result']['openId'])
        self.nick = _['result']['nick']

    def sendMessage(self, jsondata):
        self.ws.send(json.dumps(jsondata))

        return self.ws.recv()

    def makeMid(self):
        self.mid = ''
        for i in range(8):
            self.mid += random.choice(['a', 'b', 'c', 'd', 'e', 'f',
                                       '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.mid += ' 0'
        return self.mid

    def InitMessage(self):
        self.ws = create_connection('wss://webalfa-cm10.dingtalk.com/long', header={
                                    'Upgrade': 'websocket', 'Connection': 'Upgrade'})
        self.mid = ''

        def makeMid():
            self.mid = ''
            for i in range(8):
                self.mid += random.choice(['a', 'b', 'c', 'd', 'e', 'f',
                                           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            self.mid += ' 0'
            return self.mid

        
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://im.dingtalk.com/',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        did = self.res.get('https://webalfa-cm10.dingtalk.com/setCookie?code={}&appkey=85A09F60A599F5E1867EAB915A8BB07F&isSession=true&callback=__jp0'.format(
            self.tmpCode), headers=headers).headers['set-cookie']
        did = did.split('; ')[0].split('=')[1]
        
        j1 = {"lwp": "/reg", "headers": {"cache-header": "token app-key did ua vhost wv", "vhost": "WK",
                                         "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OS(windows/10.0) Browser(chrome/84.0.4147.89) DingWeb/3.8.10 LANG/zh_CN", "app-key": "85A09F60A599F5E1867EAB915A8BB07F", "wv": "im:3,au:3,sy:4", "mid": "61880001 0"}, "body": None}
        sid = json.loads(self.sendMessage(j1))
        sid = sid['headers']['sid']
        

        sendData = {
            "lwp": "/subscribe",
            "headers":
            {
                "token": self.accessToken,
                "sync": "0,0;0;0;",
                "set-ver": "191175777171",
                "mid": makeMid(),
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OS(windows/10.0) Browser(chrome/84.0.4147.89) DingWeb/3.8.10 LANG/zh_CN",
                "sid": sid,
                "did": did,
                'appkey': self.appKey
            }
        }
        self.sendMessage(sendData)
        self.sendMessage({"lwp": "/r/Sync/getSwitchStatus",
                          "headers": {"mid": makeMid()}, "body": []})
        self.sendMessage({"lwp": "/r/Adaptor/LogI/log", "headers": {"mid": makeMid()}, "body": [{"code": 2, "uid": None, "app": "ddweb", "appVer": "3.8.10", "os": "WINDOWS",
                                                                                                 "osVer": "Unknown", "manufacturer": "", "model": "", "level": 1, "message": "gmkey:stay,gokey:stayName=auth&stayTime="+str(random.randint(100, 10000))}]})
        self.sendMessage({"lwp": "/r/Adaptor/LogI/log", "headers": {"mid": makeMid()}, "body": [{"code": 2, "uid": None, "app": "ddweb", "appVer": "3.8.10", "os": "WINDOWS",
                                                                                                 "osVer": "Unknown", "manufacturer": "", "model": "", "level": 1, "message": "gmkey:stay,gokey:stayName=login&stayTime="+str(random.randint(100, 1000))}]})
        self.sendMessage({"lwp": "/r/Adaptor/IDLDing/getConfirmStatusInfo",
                          "headers": {"mid": makeMid()}, "body": []})
        self.sendMessage({"lwp": "/r/Adaptor/ConferenceI/getPreferBizCallNum",
                          "headers": {"mid": makeMid()}, "body": []})
        self.sendMessage({"lwp": "/r/Adaptor/LoginI/createTempSessionInfo",
                          "headers": {"mid": makeMid()}, "body": []})

        self.sendMessage({"lwp": "/r/Adaptor/CsConfigI/getConf", "headers": {
                         "mid": makeMid()}, "body": [[{"topic": "org_screen", "version": 0}]]})
        self.sendMessage({"lwp": "/r/Adaptor/LogI/log", "headers": {"mid": makeMid()}, "body": [{"code": 2, "uid": self.openId, "app": "ddweb", "appVer": "3.8.10", "os": "WINDOWS",
                                                                                                 "osVer": "Unknown", "manufacturer": "", "model": "", "level": 1, "message": "gmkey:stay,gokey:stayName=login.scanCodeLogin&stayTime="+str(random.randint(100, 10000))}]})
        self.sendMessage({"lwp": "/r/Adaptor/LogI/log", "headers": {"mid": makeMid()}, "body": [{"code": 2, "uid": self.openId, "app": "ddweb", "appVer": "3.8.10", "os": "WINDOWS",
                                                                                                 "osVer": "Unknown", "manufacturer": "", "model": "", "level": 1, "message": "gmkey:stay,gokey:stayName=authorized&stayTime="+str(random.randint(10, 10000))}]})
        self.sendMessage({"lwp": "/r/IDLConversation/getByIdUnlimited",
                          "headers": {"mid": makeMid()}, "body": ["164902:"+self.openId]})
        self.sendMessage({"lwp": "/r/IDLConversation/getByIdUnlimited",
                          "headers": {"mid": makeMid()}, "body": ["21000:"+self.openId]})
        self.sendMessage({"lwp": "/r/Adaptor/CsConfigI/getConf", "headers": {
                         "mid": makeMid()}, "body": [[{"topic": "ch_user", "version": 0}]]})
        self.sendMessage({"lwp": "/r/Adaptor/UserMixI/getUserProfileByUids",
                          "headers": {"mid": makeMid()}, "body": [[self.openId]]})
        self.sendMessage(
            {"headers": {"mid": makeMid()}, "code": 200, "body": {}})
        self.sendMessage({"lwp": "/r/Adaptor/CMailI/queryUserDingMailStatus",
                          "headers": {"mid": makeMid()}, "body": ["zh_CN"]})
        self.sendMessage({"lwp": "/r/IDLConversation/listNewest",
                          "headers": {"mid": makeMid()}, "body": [1000]})
        _ = json.loads(self.sendMessage({"lwp": "/r/Sync/getState", "headers": {"mid": makeMid(
        )}, "body": [{"pts": 0, "highPts": 0, "seq": 0, "timestamp": 0, "tooLong2Tag": ""}]}))

    def getConversation(self):

        a = self.sendMessage(self.sendMessage(
            {"lwp": "/r/IDLConversation/listNewest", "headers": {"mid": self.makeMid()}, "body": [1000]}))
        a = json.loads(a)

        if a['code'] != 200:
            print(a['reason'])
            return False

        a = a['body']
        #print(a)
        

        _ = {}
        for i in a:
            t = i['baseConversation']['title']
            # print('"{}"'.format(t))
            if t.strip() == '':
                t1 = i['baseConversation']['conversationId'].split(':')[1]
                t0 = i['baseConversation']['conversationId'].split(':')[0]

                if t1 == self.openId:
                    t = self.getUserInfo(t0)['body']['userProfileModel']['nick']
                else:
                    t = self.getUserInfo(t1)['body']['userProfileModel']['nick']

            _[t]=i['baseConversation']['conversationId']

        return _

    def send(self, conversationId, text):
        self.sendMessage({"lwp": "/r/IDLSend/send", "headers": {"mid": self.makeMid()}, "body": [{"uuid": str(int(time.time(
        )*1000000)), "conversationId": conversationId, "type": 1, "creatorType": 1, "content": {"contentType": 1, "textContent": {"text": text}, "atOpenIds": {}}, "nickName": self.nick}]})

    def getUserInfo(self, openId):
        a = self.sendMessage({"lwp": "/r/Adaptor/UserMixI/getUserProfileExtensionByUid",
                              "headers": {"mid": self.makeMid()}, "body": [openId, None]})
        return json.loads(a)

    def getUsers(self, conversationId):
        a = self.sendMessage({"lwp": "/r/IDLConversation/listMembers", "headers": {
                             "mid": self.makeMid()}, "body": [conversationId, 0, 2147483647]})
        
        return json.loads(a)['body']

    def formatMembersInfo(self,infolist):
        _=[]
        __={1:'群主',2:'群管理员',3:'群员'}
        for i in infolist:
            d = {}
            try:
                d['FullName'] = self.getUserInfo(i['openIdEx']['openId'])['body']['cardUserModel']['name']
                d['groupNick'] = i['groupNickModel']['groupNick']
                d['role'] = __[i['role']]
                d['openId'] = i['openIdEx']['openId']
            except:
                pass
            _.append(d)
        return _

    def getNewMessage(self, conversationId, wait_time=2):
        
        
        _ = []
        __ = []
        
        a = self.sendMessage({"lwp": "/r/IDLMessage/listMessages", "headers": {
                                 "mid": self.makeMid()}, "body": [conversationId, False, int(time.time()*1000), 14]})
        b = json.loads(a)['body']

        for i in b:
            try:
                i['baseMessage']['content']['textContent']['text']
            except:
                continue
            if [i['baseMessage']['content']['textContent']['text'], i['baseMessage']['createdAt'], i['baseMessage']['openIdEx']['openId']] in _:
                continue
            else:
                __.append([i['baseMessage']['content']['textContent']['text'],
                               i['baseMessage']['createdAt'], i['baseMessage']['openIdEx']['openId']])
        
        if __ != []:
            _ += __

        time.sleep(wait_time)
        return __[::-1]

    def getMessage(self,cid,rule=[],mode='all',wait_time=2):
        
        if mode == 're':
            
            _ = []
            __ = self.getNewMessage(cid,wait_time)
            for i in rule:
                for j in __:
                   
                    h = re.findall(i, j[0],re.S)
                    if h != []:
                        _.append(j)
            if _==[]:
                return _
            time.sleep(wait_time)
            for i in _:
                try:
                    i.append(self.getUserInfo(i[2])['body']['cardUserModel']['name'])
                except BaseException as e:
                    print(e)
                    i.append('')
            return _
        
        elif mode=='all':
            _=self.getNewMessage(cid,wait_time)
            time.sleep(wait_time)
            for i in _:
                try:
                    i.append(self.getUserInfo(i[2])['body']['cardUserModel']['name'])
                except BaseException as e:
                    print(e)
                    i.append('')
            return _


    def Login(self):
        self.getCode()
        self.makeQRcode()
        self.makedata()
        self.checkIfLogined()
        self.InitMessage()


