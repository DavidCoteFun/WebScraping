#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 18:31:35 2022

@author: dcote
"""

from requests_html import HTMLSession
from time import sleep,localtime,strftime
import subprocess
import random
import pickle


phoneNumber="+18191234567"
#textMsg="Ceci est un test: nouveau chat Roger"
#fullArg='tell application "Messages" to send "%s" to buddy "%s"'%(textMsg,phoneNumber)
#print("osascript -e %s"%fullArg)
#subprocess.run(["osascript", "-e", fullArg])
#osascript -e 'tell application "Messages" to send "Python says there three ti minous" to buddy "+18191234567"'



def get_list_of_SPCA_cats(test=False):
    myURL="https://spca-outaouais.org/adoption/chats-en-adoption"
    session = HTMLSession()
    r2 = session.get(myURL)
    rh=str(r2.html.raw_html)
    
    l1=rh.split('aria-label="Lire la suite&nbsp;:  ')
    l2=l1[1:]
    lCats=[]
    for tmp in l2:
        lCats.append(tmp.split('"')[0])

    if test:
        if random.random()>0.5:
            lCats.append("TestCat1")
        if random.random()>0.5:
            lCats.append("TestCat2")
        print("Test: %s"%lCats)
    return set(lCats)


def load_historical_list(verbose=True):
    persistent_file=open('knowncats.pickle', 'rb')
    historical_list=pickle.load(persistent_file)
    latest_update_time=pickle.load(persistent_file)
    persistent_file.close()
    if verbose:
        print(latest_update_time)
        print("Liste historique: %i chats  --  %s"%(len(historical_list),historical_list))
    return historical_list


def dump_historical_list(lNew,theTime):
    persistent_file=open('knowncats.pickle', 'wb')
    pickle.dump(lNew,persistent_file)
    pickle.dump(theTime,persistent_file)
    persistent_file.close()
    return



lAll=load_historical_list()
lNow=get_list_of_SPCA_cats()
print("Liste live: %i chats -- %s \n"%(len(lNow),lNow))
lOld=lNow
print(" ")

nTry=0
while nTry<1000000:
    sleep(120)
    lNow=get_list_of_SPCA_cats(test=False)
    theTime=strftime("%a, %d %b %Y %H:%M:%S", localtime())
    ajout=lNow-lAll
    enleve=lOld-lNow
   
    if len(ajout)>0:
        print("****  Nouveaux Chats!!!  ****  %s"%theTime)
        print(ajout)
        if len(ajout)>1:
            textMsg="Nouveaux chats à la SPCA: %s !!!"%ajout
        else:
            textMsg="Nouveau chat à la SPCA: %s !!!"%ajout
            pass
        #iMessage alert
        fullArg='tell application "Messages" to send "%s" to buddy "%s"'%(textMsg,phoneNumber)
        print("osascript -e %s"%fullArg)
        subprocess.run(["osascript", "-e", fullArg])
        #Update historical list
        lNew=lAll.union(ajout)
        dump_historical_list(lNew,theTime)
        print("nouvelle liste historique: %i chats -- %s"%(len(lNew),lNew))
        lAll=lNew
        
    if len(enleve)>0:
        print("****  Chat Enelevé  ****  %s"%theTime)
        print(enleve)

    if len(enleve)>0 or len(ajout)>0:
        print("nouvelle liste live: %i chats -- %s \n"%(len(lNow),lNow))
    else:
        print("Pas de nouveaux chats  --  %s"%theTime)
        pass
    lOld=lNow
    nTry+=1
    pass

