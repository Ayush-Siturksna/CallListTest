import pandas as pd1

df1=pd1.read_csv('panda2.csv')


def funct(string):
    rs=string.find('Please provide SPC/SNOW ticket number')
    n=int(rs)
    
    return string[n+49:n+58]

def funct2(string):
    rs2=string.find('please select the correct service from below list. For non-HEC, pls select N/A')
    n2=int(rs2)
    
    return string[n2+88:n2+107]    

    

df1['ticket']=df1['Description'].apply(funct)
df1['service']=df1['Description'].apply(funct2)


df2=df1[['Start Time','Subject','ticket','service']]


print(df2)

# print(df1['Description'].apply(funct).head())



# print(df1['Description'].head())
