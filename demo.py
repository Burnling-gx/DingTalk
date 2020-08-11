
#sendMessage

import DingTalk
dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName
dt.send(cid,'text')


#get members of a group

import DingTalk
dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName
members = dt.getUsers(cid)
print(dt.formatMembersInfo(members))

#get messages in a group

import DingTalk
dt = DingTalk.Work()
dt.Login()
cid_dict = dt.getConversation()
cid = cid_dict['ConversationName']#Please replace 'ConversationName' with ConversationName

