import json 
import os 
import random 
import string 

class config:
    hroj_user = "./hroj.db/hroj_user.json"

def getdb():
    return json.loads( open(config.hroj_user,"r").read())

def user_info(username):
    db = getdb()

    for token,info in db.items():
        if(info['username']==username):
            info['submissions'] = info['submissions'][::-1]
            return token,info
        
    return "!","!"
    
def usernames():
    lst = []
    db = getdb()
    for tok,inf in db.items():
        lst.append(inf['username'])
    return lst

def mails():
    lst = []
    db = getdb()
    for tok,inf in db.items():
        lst.append(inf['mail'])
    return lst
    
def username_to_token(username):
    db = getdb()
    for tok,inf in db.items():
        if inf['username'] == username: 
            return tok
    
def token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(31))

def correct(username,password):
    token,info = user_info(username)
    if(token!="!" and info!="!" and info['password']==password):
        return token,info 
    else:
        return "!","!"
    
def new_user(info):
    tok = "HROJ-"+token()
    db= getdb()
    db[tok]=info
    
    if(info['username'] not in usernames()):
        
        with open(config.hroj_user,"w") as f:
            f.write(json.dumps(db,indent=4))
        
    else:
        return "!"
    
def ban_user(tok):    
    db= getdb()

    if(tok in db):
        db.pop(tok,None)
        with open(config.hroj_user,"w") as f:
            f.write(json.dumps(db,indent=4))
        
    else:
        return "!"
    
def update_user(tok,info):
    db=getdb()
    usrlst = usernames()
    maillst = mails()
    if 'username' in info and db[tok]['username']!=info['username'] and info['username'] in usrlst:
        return "Username"
    elif 'mail' in info and db[tok]['mail']!=info['mail'] and info['mail'] in maillst:
        return "Mail"
    
    if( len(info.items())):
        
        for key,value in info.items():
            db[tok][key]=value
            
        
        with open(config.hroj_user,"w") as f:
            f.write(json.dumps(db,indent=4))
        