import itchat, time
from itchat.content import *


# itchat.send('Hello', toUserName='filehelper')
# @4fbb76e9173863914f78bf75b75496a9708480d8263221dbdbae29b3783bdceb camfee
# @746bd0c368618416efcc9e420cf5a63a60caeb859647f32bd449dcf1e5e8ab4e flh

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    msg.user.send('%s: %s' % (msg.type, msg.text))


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print(msg)
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print(msg)
    msg.user.verify()
    msg.user.send('Nice to meet you!')


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(msg)
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))


@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg)
    # itchat.send('Hello %s!' % (msg['User']['NickName']), toUserName=msg.FromUserName)


def after_login():
    print('login success')


def after_logout():
    print('exit')


# 登陆
itchat.auto_login(hotReload=True, loginCallback=after_login, exitCallback=after_logout)
# 运行并保持在线状态
itchat.run()
