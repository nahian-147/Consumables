import os
import mysql.connector
from rich.console import Console
from rich.table import Column,Table

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

def show():
    c = db.cursor()
    book = "select sum(consTime),sum(total_days),avg(rating),count(type) from consumables where type = 'Book';"
    c.execute(book)
    btd = c.fetchone()
    series = "select sum(consTime),sum(total_days),avg(rating),count(type) from consumables where type = 'Series';"
    c.execute(series)
    std = c.fetchone()
    movie = "select sum(consTime),sum(total_days),avg(rating),count(type) from consumables where type = 'Movie';"
    c.execute(movie)
    mtd = c.fetchone()

    rating = "select avg(rating),count(type) from consumables;"
    c.execute(rating)
    r = c.fetchone()

    alltype = "select sum(total_time),sum(total_days) from total;"
    c.execute(alltype)
    at = c.fetchone()

    tt = "\nTotal Time spent in,\tBooks  "+str(btd[0])+"\tSeries  "+str(+std[0])+"\tMovies  "+str(mtd[0])+"\tOverall  "+str(at[0])+"\n"
    td = "\nTotal Days spent in,\tBooks  "+str(btd[1])+"\tSeries  "+str(+std[1])+"\tMovies  "+str(mtd[1])+"\tOverall  "+str(at[1])+"\n"
    av = "\nAverage rating of,\tBooks  "+str(btd[2])+"\tSeries  "+str(+std[2])+"\tMovies  "+str(mtd[2])+"\tOverall  "+str(r[0])+"\n"
    cnt = "\nTotal count of\tBooks  "+str(btd[3])+"\tSeries  "+str(+std[3])+"\tMovies  "+str(mtd[3])+"\tOverall  "+str(at[1])+"\n"
    line = "\n======================================================================================================================\n"

    print(line+tt+line+td+line+av+line+cnt+line)


def showind(typ):
    c = db.cursor()
    query = "select name,total_days,consTime,rating from consumables where type = '"+typ+"';"
    c.execute(query)
    lst = c.fetchall()
    nms = 'NAME'
    TD = 'TOTAL DAYS'
    TT = 'TOTAL TIME'
    R = 'RATING'
    print(f"{nms:50} || {TD:10} || {TT:10} || {R:10} ||")
    line = "======================================================================================================"
    print(line)
    for item in lst:
        print(f"{item[0]:50} || {item[1]:10} || {item[2]:10} || {item[3]:10} ||")


def fulldetail(name):
    c = db.cursor()
    query = "select * from consumables where name = '"+name+"';"
    c.execute(query)
    lst = c.fetchone()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("TYPE")
    table.add_column ("NAME", justify="right")
    table.add_column("START DATE", justify="right")
    table.add_column("END DATE", justify="right")
    table.add_column("RATING", justify="right")
    table.add_column("START DATE", justify="right")
    table.add_column("TOTAL TIME", justify="right")
    table.add_column("TOTAL DAYS", justify="right")

    table.add_row(str(lst[0]),str(lst[1]),str(lst[2]),str(lst[3]),str(lst[4]),str(lst[5]),str(lst[6]),str(lst[7]))

    console.print(table)



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
            typeOptions = 'Select one Consumable from below: \n1.Books\n2.Series\n3.Movie\n4.none'
            os.system('clear')
            typ = input(typeOptions)
            if not typ.lower() in ['5','none']:
                name = int("Type thye name of the Consumable you want to delete\n")
                dlt(name)
            else:
                continue
        elif(choice=='4'):
            typeOptions = 'Select one Consumable from below: \n1.Book\n2.Series\n3.Movie\n4.Pick One\n5.None\n'
            os.system('clear')
            typ = input(typeOptions)
            if not typ.lower() in ['5','none']:
                if(typ=='1'):
                    showind('Book')
                elif(typ=='2'):
                    showind('Series')
                elif(typ == '3'):
                    showind('Movie')
                elif typ == '4':
                    name = input("Enter the name of the conumable : ")
                    fulldetail(name)
                input('\nPress any key to return to the Main Menu')
            else:
                continue
        elif(choice=='5'):
            show()
            response = input("Press Any key to go to the Main menu")
            if response.lower() in ['1','cancel']:
                continue
    else:
        break

db.close()
