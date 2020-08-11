# DingTalk
自己写的钉钉接口，基于网页版钉钉实现。可以捕获钉钉聊天消息、发送消息


SendMessage:

import DingTalk

dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName
dt.send(cid,'text')


