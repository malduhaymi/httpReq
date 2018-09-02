import requests
import warnings
import mysql.connector
from time import sleep
warnings.filterwarnings("ignore")



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="govtect"
)

mycursor = mydb.cursor()


tech=""
lang=""
server=""
con="ksa"
def getValue( parameters ):
    x=stringHeaders.split(parameters)
    arraylist=x[1].split(",")[0].split(":")[1]
    #print hello
    arraylist=arraylist.replace("'","")
    return arraylist

with open('url.txt') as urls:
    
    for url in urls:
        tech=""
        lang=""
        server=""
        tech=""
        url=url.strip()
        #sleep(3)
        try:
            r = requests.get(url, verify=False)
            headers=r.headers
            #print headers
            stringHeaders=str(headers)
            #print stringHeaders
                
            #read from HTTP RESP HEADER
            try:
                if "X-MS-InvokeApp" in stringHeaders:
                    x= getValue("X-MS-InvokeApp")
                    tech= "SharePoint"
                    print tech

                    #insert into DataBase

                if  "X-SharePoint" in stringHeaders:
                    #insert into DataBase
                    x= getValue("X-SharePoint")
                    tech= "SharePoint"
                    print tech

                if  "X-Drupal" in stringHeaders:
                    #insert into DataBase
                    x= getValue("X-Drupal")
                    tech= "Drupal"
                    print tech
                    
                if  "Server" in stringHeaders:
                    #insert into DataBase
                    x= getValue("Server")
                    server= x
                    print server

                if  "X-Powered-By" in stringHeaders:
                    #insert into DataBase
                    lang= getValue("X-Powered-By")
                    print lang
            
            except :
                print "error"


            #read from Cookie
            try:
                if headers['Set-Cookie']:
                    cookie=headers['Set-Cookie']
                    x=str(cookie)
                    if x.find("JSESSIONID")!=-1:
                        #Man, it's a JAVA :)
                            print " IT'S JAVA"
                            lang="java"
                    if x.find("PHPSESSIONID")!=-1:
                        #Bro, it's a PHP :(
                        print "IT'S php "
                        lang="PHP"
                    #insert into DataBase
            except KeyError:
                print("No Set-Cookie")

            #read from URL
            #check php
            if con !="ksa":                
                req = requests.get(url+"/index.php", verify=False)
                if req.status_code == 404:
                    print "not PHP"
                else:
                    lang="PHP"

                req = requests.get(url+"/index.aspx", verify=False)
                if req.status_code == 404:
                    print "not aspx"
                else:
                    lang="aspx"
         
                req = requests.get(url+"/index.jsp", verify=False)
                if req.status_code == 404:
                    print "not jsp"
                else:
                    lang="java"



            sql = "INSERT INTO tech (url, server_type,tech_type,lang,country) VALUES (%s, %s,%s, %s,%s)"
            val = (url,server,tech,lang,"ksa")
            mycursor.execute(sql, val)
            mydb.commit()

        except:
            print "ERROR IN HTTPREQ"
