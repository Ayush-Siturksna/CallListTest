from curses.ascii import isalnum
from operator import concat, index
from curses.ascii import *
import pandas as pd1
import time
import datetime as dt

now=dt.datetime.now()

df1=pd1.read_csv('panda3.csv')

df1.columns = [c.replace(' ', '_') for c in df1.columns]


def funct(string):
    rs=string.find('Please provide SPC/SNOW ticket number')
    n=int(rs)
    if string[n+49].isdigit():
        
        return string[n+49:n+58]
    else : 
        return   'Non-booking' 
        
    
    
    
def funct2(string):
    rs2=string.find('please select the correct service from below list. For non-HEC, pls select N/A')
    n2=int(rs2)
    if string[n2+86]=="-":
        
        return string[n2+86:n2+107]
    else : 
        return   'Non-booking' 
    
      

    

df1['ticket']=df1['Description'].apply(funct)
df1['service']=df1['Description'].apply(funct2)

def remove(string):
    return string.replace(" ", "")

def funct3(string):
    strng2=remove(string)
    # newdate2 = time.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")
    newdate2 = dt.datetime.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")    
    return newdate2

df1['datetime']=df1['Start_Time']+' ' +df1['Start_Date']

df1['modfdatetime']=df1['datetime'].apply(funct3)

df2=df1[['Start_Time','Subject','service','ticket','modfdatetime']]
df2.sort_values(by=['modfdatetime'],inplace=True)

a = df2.loc[(df2['modfdatetime'] >now) &(df2['modfdatetime'] < (now+dt.timedelta(hours=24)))]

def remove(string):
    return string.replace(" ", "")

strng1=df1.loc[1].at['datetime']
strng2=remove(strng1)

# newdate2 = time.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")
newdate2 = dt.datetime.strptime(strng2, "%I:%M:%S%p%m/%d/%Y")
newdate3=newdate2+dt.timedelta(hours=20)

a.reset_index(drop=True,inplace=True)
print(a.loc[:, a.columns != 'modfdatetime'])
# print(strng1)
# print(newdate2)
# print(newdate3)
# print(now>newdate2)


# print()