import os
import mysql.connector

db = mysql.connector.connect(
        host='localhost',
        user='nahian',
        password='Nahian_8',
        database='CONSUMABLES'
        )


def insrt(t):
    os.system('clear')
    name = input('name of the '+t+'? : ')
    start = input('starting date (YYYY-MM-DD) ? : ')
    end = input('ending date (YYYY-MM-DD) ? : ')
    rating = input('rating (out of 10) ? : ')

    c = db.cursor(buffered=True)
    insert = """insert into consumables (type,name) 
            values ('"""+t+"""','"""+name+"""');"""
    c.execute(insert)
    if not start == "":
        us = "update consumables set consStart = '"+start+"' WHERE name = '"+name+"';"
        c.execute(us)
    if not end == "":
        ue = "update consumables set consEnd = '"+end+"' WHERE name = '"+name+"';"
        c,execute(ue)
    if not rating == "":
        ur = "update consumables set rating = '"+rating+"' WHERE name = '"+name+"';"
        c.execute(ur)
    
    #insert = """insert into consumables (type,name,consStart,consEnd,rating) 
           # values ('"""+t+"""','"""+name+"""','"""+start+"""','"""+end+"""','"""+rating+"""');"""

    db.commit()

def addTime(name,hours):
    c = db.cursor(buffered=True)
    q1 = "UPDATE consumables SET consTime = consTime + "+hours+" WHERE name  = '"+name+"';"
    q2 = "UPDATE total SET total_time = total_time + "+hours+";"
    c.execute(q1)
    c.execute(q2)
    db.commit()

def aday(name):
    c = db.cursor(buffered=True)
    q1 = "UPDATE consumables SET total_days = total_days + 1 WHERE name  = '"+name+"';"
    q2 = "UPDATE total SET total_days = total_days + 1;"
    c.execute(q1)
    c.execute(q2)
    db.commit()

def chngRating(name,rating):
    c = db.cursor(buffered=True)
    q = "UPDATE consumables SET rating = "+rating+" WHERE name  = '"+name+"';"
    c.execute(q)
    db.commit()

def chngEdate(name,date):
    c = db.cursor(buffered=True)
    q1 = "SELECT consEnd from consumables where name = '"+name+"';"
    c.execute(q1)
    if not len(c.fetchall()) :
        q2 = "UPDATE consumables SET consEnd = '"+date+"' where name = '"+name+"';"
        c.execute(q2)
        db.commit()
    else:
        print("Can't update now !")

def dlt(name):
    c = db.cursor()
    fetch = "select name, consTime,total_days from consumables where name = '"+name+"';"
    c.execute(ftch)
    p = c.fetchall()
    d = "delete from consumables where name = '"+name+"';"
    insert = """insert into deleteds (name,consTime,total_days) 
             values ('"""+name+"""','"""+p[0][1]+"""','"""+p[0][2]+"""');"""
    c.execute(d)
    c.execute(insert)

options = "1.Add a Consumable\n2.Edit a Consumable\n3.Delete a Consumable\n4.See the list of consumables and individually\n5.See overall info\n6.Exit\n"

while True:
    os.system('clear')
    choice = input(options)
    if(not choice.lower() in ['6','exit']):
        if(choice=='1'):
            typeOptions = 'Select one Consumable from below: \n1.Books\n2.Series\n3.Movie\n4.None\n'
            os.system('clear')
            typ = input(typeOptions)
            if not typ.lower() in ['4','none']:
                if(typ=='1'):
                    insrt('Book')
                elif(typ=='2'):
                    insrt('Series')
                elif(typ=='3'):
                    insrt('Movie')
            else:
                continue
        elif(choice=='2'):
            actions = 'Select one of the actions below: \n1.Add time in Hours\n2.Add a day\n3.Change the Rating\n4.Change Conumption Ening date\n5.None\n'
            os.system('clear')
            name = input("Enter the name of the Consumable(Book/Series/Movie) : ")
            action = input(actions)
            if not action.lower() in ['5','none']:
                if action == '1':
                    hours = input("How many Hours ? : ")
                    addTime(name,hours)
                elif action == '2':
                    aday(name)
                elif action =='3':
                    rating = input("New Rating ? : ")
                    chngRating(name,rating)
                elif action == '4':
                    date = input("Date ? : ")
                    chngEdate(name,date)
            else:
                continue
        elif(choice=='3'):
            typeOptions = 'Select one Consumable from below: \n1.Books\n2.Series\n3.Movie\n4.Pick One\n5.None'
            os.system('clear')
            typ = input(typeOptions)
            if not typ.lower() in ['5','none']:
                name = int("Type thye name of the Consumable you want to delete\n")
                dlt(name)
            else:
                continue
        elif(choice=='4'):
            typeOptions = 'Select one Consumable from below: \n1.Books\n2.Series\n3.Movie\n4.None\n'
            os.system('clear')
            typ = input(typeOptions)
            if not typ.lower() in ['4','none']:
                print('You have chosen',typ)
                input('Press any key to exit')
            else:
                continue
        elif(choice=='5'):
            
            response = input()
            if response.lower() in ['1','cancel']:
                continue
    else:
        break

db.close()
