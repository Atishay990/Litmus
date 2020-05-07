from collections import defaultdict
import pickle

class friendGraph:

    global members
    global filename
    filename = 'D:/mysite/network'
    #members = defaultdict(list)

    def __init__(self):
        self.members=defaultdict(list)
        #outfile = open(filename,'wb')
        #pickle.dump(self.members,outfile)
        #outfile.close()

    def nodeDoesNotExist(self,id,node):
        infile = open(filename,'rb')
        members = pickle.load(infile)
        infile.close()
        for member in members[id]:
            if member == node:
                return 0
        return 1

    def sendFriendRequest(self,sender,receiver):
        infile = open(filename,'rb')
        members = pickle.load(infile)
        infile.close()
        members[sender].append(receiver)
        outfile = open(filename,'wb')
        pickle.dump(members,outfile)
        outfile.close()


    def acceptFriendRequest(self,sender,receiver):
        infile = open(filename,'rb')
        members = pickle.load(infile)
        infile.close()
        members[receiver].append(sender)
        outfile = open(filename,'wb')
        pickle.dump(members,outfile)
        outfile.close()

    def pendingFriendRequest(self,id):
        infile = open(filename,'rb')
        members = pickle.load(infile)
        infile.close()
        friend_list=[]
        for member in list(members):
            for friend in members[member]:
                if friend==id and self.nodeDoesNotExist(id,member)==1:
                    friend_list.append(member)

        return friend_list

    def friend_list(self,id):
        infile = open(filename,'rb')
        members = pickle.load(infile)
        #print(members)
        infile.close()
        list=[]
        for friend in members[id]:
            if self.nodeDoesNotExist(friend,id)==0:
                list.append(friend)

        return list


#o = friendGraph()
#o.sendFriendRequest("atishay990@gmail.com","atishayjain79@gmail.com")
#o.sendFriendRequest("atishay990@gmail.com","201951035@iiitvadodara.ac.in")
#o.acceptFriendRequest("atishay990@gmail.com","201951035@iiitvadodara.ac.in")
# o.acceptFriendRequest("atishay","subhangi")
# o.sendFriendRequest("aviral","shreya")
# o.sendFriendRequest("lakshya","shreya")
# o.acceptFriendRequest("aviral","shreya")
#print(o.friend_list("201951035@iiitvadodara.ac.in"))
#print(o.pendingFriendRequest("atishayjain79@gmail.com"))
