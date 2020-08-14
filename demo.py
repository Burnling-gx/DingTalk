
#sendMessage 发消息

import DingTalk
dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName
dt.send(cid,'text')


#get members of a group 获取群员信息

import DingTalk
dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName
members = dt.getUsers(cid)
print(dt.formatMembersInfo(members))
# return:
# {[{'FullName': '', 'groupNick': '', 'role': '', 'openId': },{'FullName': '', 'groupNick': '', 'role': '', 'openId': }......]}


#get messages in a group 获取聊天信息

import DingTalk
dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName
print(dt.getMessage(cid))
# return:
# [['messageData', timestamp, openID, 'nick'],['messageData', timestamp, openID, 'nick'],['messageData', timestamp, openID, 'nick']]
