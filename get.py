#*-* coding:utf-8 *-*
import socket
socket.setdefaulttimeout(10.0)
import re
import time
import urllib2
import gzip
import thread
import requests
import sys
reload(sys)
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
def getImage(content):
    ret=[]
    index1=0
    index2=0
    for count in range(0,200):
        index1=content.find("<input src=",index2)
        index2=content.find('type=\'image\'',index1)

        res=content[index1+12:index2-2]
        if(len(res)==0):break
        if(len(res)>300):break
        ret.append(res)
    return ret
def thread_function(start,end,directoryBegin):
    page=0
    pageReverse=0
    for page in range(start,end-1,-1):
        try:
            r = requests.get('http://c6.h0j.org/thread0806.php?fid=16&search=&page='+str(page),headers=headers)
            data=r.text.encode(r.encoding)
            r=re.compile(r".+\[\d+\]")
            index=0
            index=data.find("<a href=\"htm_data",index)
            index2=data.find("P]",index)
            length=len(data)
            for x in range(0,100):
                try:
                    index=data.find("<a href=\"htm_data",index2)
                    indexUrlEnd=data.find(".html",index)
                    index2=data.find("P]",index)
                    index3=data[index:index2+1].rfind(">")
                    url=data[index+9:indexUrlEnd+5]
                    titleName=data[index+index3+1:index2+2]
                    titleIndex=data[index+26:index+33]
                    print page,titleIndex,url,titleName
                    if(len(data[index:index2])==0):
                        print "Page none ,break"
                        continue
                    imgReq = requests.get('http://c6.h0j.org/'+url,headers=headers)
                    imgHtml=imgReq.text.encode(imgReq.encoding)
                    info=getImage(imgHtml)
                    print info
                    output=open("cl/"+str(directoryBegin+int(pageReverse))+"/"+str(titleIndex)+","+titleName+".html","w")
                    html='<div align="center">'
                    for imgUrl in info:
                            html=html+"<img src='"+imgUrl+"'/><br><br>"
                    html=html+"</div>"
                    output.write(html)
                    output.close()
                    print ""
                except Exception as e:
                    print e
                    print "Error occurred ,pass"
            pageReverse=pageReverse+1
        except Exception as e:
            print e
def splitTask(tailPage,frontPage,startFolderNum,everyTaskPages):
    count=0
    a=0
    b=0
    c=startFolderNum-everyTaskPages
    for x in range(tailPage,frontPage-1,-1):
        if(count==0):
            a=x
        if(count+1==everyTaskPages or x==frontPage):
            b=x
            if(count+1==everyTaskPages):
                c=c+everyTaskPages
            else:
                c=c+(tailPage-frontPage)%everyTaskPages+1
            count=0
            thread.start_new_thread(thread_function,(a,b,c))
            print a,b,c
            continue
        count=count+1

splitTask(9,1,154,2)#end page,front page,front folder,page num each task
while True:
    time.sleep(5)
