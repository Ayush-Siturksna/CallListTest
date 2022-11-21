from curses.ascii import isalnum
from operator import concat, index
from curses.ascii import *
import pandas as pd1
import time
import datetime as dt
import requests
import json


weburl1='https://capgemini.webhook.office.com/webhookb2/f1156788-1da9-4e23-ba66-cfd50ddc7bf9@76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/IncomingWebhook/4b4730d6b2d2428ea3311160c7ba63ee/bdbfb26b-c48e-474e-b21a-8270adb44df2'
weburl2='https://capgemini.webhook.office.com/webhookb2/afbd8b6c-c9dc-4f74-94ee-e47f649345b6@76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/IncomingWebhook/e7946416405d4050a5caa15122d7affa/bdbfb26b-c48e-474e-b21a-8270adb44df2'


now=dt.datetime.now()

df1=pd1.read_csv('mail.csv')

df1.columns = [c.replace(' ', '_') for c in df1.columns]


def funct(string):
    rs=string.find('Please provide SPC/SNOW ticket number')
    n=int(rs)
    if string[n+49].isdigit():
        
        return string[n+49:n+59]
    else : 
        return   'NoTicket' 

def funct6(string):
    rs=string.find('Please provide complete meeting link here:')
    n=int(rs)
    stringnew=string[n+51:-1]
    rs2=stringnew.find('\r')
    n2=int(rs2)
        
    return stringnew[0:n2]
            
    
    
    
def funct2(string):
    rs2=string.find('please select the correct service from below list. For non-HEC, pls select N/A')
    n2=int(rs2)
    if string[n2+86]=="-":
        if string[n2+88]=="V":
            return string[n2+86:n2+91]
        else :
            return string[n2+86:n2+107]
    else : 
        return   'Non-booking' 
    
      

    

df1['ticket']=df1['Description'].apply(funct)
df1['service']=df1['Description'].apply(funct2)
df1['Link']=df1['Description'].apply(funct6)

def remove(string):
    return string.replace(" ", "")

def funct3(string):
    strng2=remove(string)
    # newdate2 = time.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")
    newdate2 = dt.datetime.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")    
    return newdate2

df1['datetime']=df1['Start_Time']+' ' +df1['Start_Date']

df1['modfdatetime']=df1['datetime'].apply(funct3)


df2=df1[['Start_Time','Subject','service','ticket','modfdatetime','Link']]
df2.sort_values(by=['modfdatetime'],inplace=True)

a = df2.loc[(df2['modfdatetime'] >(now-dt.timedelta(hours=0))) &(df2['modfdatetime'] < (now+dt.timedelta(hours=10)))]

def remove(string):
    return string.replace(" ", "")

strng1=df1.loc[1].at['datetime']
strng2=remove(strng1)

# newdate2 = time.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")
newdate2 = dt.datetime.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")
newdate3=newdate2+dt.timedelta(hours=20)

def funct4(string):
    d = dt.datetime.strptime(string, '%I:%M:%S %p')
    d2= dt.datetime.strftime(d, "%I:%M %p")
    return d2


def funct5(string):
    if string[0]=='-' :
        return 1 
    else :
        return 0


a['Time']=a['Start_Time'].apply(funct4)

a['boolean']=a['service'].apply(funct5)

a.reset_index(drop=True,inplace=True)

df3=a[['Time','Subject','service','ticket','boolean','Link']]



b=df3.loc[(df3['boolean']==1)]

b.to_csv('pandaoutput.csv',index=False)


print(b)
# print(a.loc[:, a.columns != 'modfdatetime'])
# print(strng1)
# print(newdate2)
# print(newdate3)
# print(now>newdate2)


# print()

string10=""

count = 0
while (count < len(b.index)):   
    string10= string10+"\r- ["+b['Time'].iloc[count]+"]"+"("+b['Link'].iloc[count]+") " + b['Subject'].iloc[count] + b['service'].iloc[count] +"-  ["+b['ticket'].iloc[count]+"]("+"https://spc.ondemand.com/open?ticket="+b['ticket'].iloc[count]+") "
    count = count + 1
    

# for i in range(0, len(b.index)-1):
#     string10= string10+"["+b['Time'][i]+"]"+"("+b['Link'][i]+") \r- "



# string9= b['ticket'][1]

data= {  
    "type":"message",
    "attachments":[
       {
          "contentType":"application/vnd.microsoft.card.adaptive",
          "contentUrl":weburl1,
          "content":{
             "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
             "type":"AdaptiveCard",
             "version":"1.2",
             "msTeams": { "width": "full" },
             "body":[
                {
                    "type": "TextBlock",
                    # "text":  string10+ " here is \r- [7:30 AM](https://teams.microsoft.com/l/meetup-join/19%3ameeting_MTNhMmU5YjMtOWZhZC00NzJmLWFmNGYtNzBkM2RlMzUwMTFj%40thread.v2/0?context=%7b%22Tid%22%3a%2242f7676c-f455-423c-82f6-dc2d99791af7%22%2c%22Oid%22%3a%220c98add1-e9b2-415c-b1ef-dd68a614dd27%22%7d) \r- link3"
                    "text":   " here  " + string10
                }
               
               
           
             ]
          }
       }
    ]
 }

r=requests.post(weburl1,data=json.dumps(data),headers={'Content-type': 'applications/json'})