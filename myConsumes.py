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
        c.execute(ue)
    if not rating == "":
        ur = "update consumables set rating = '"+rating+"' WHERE name = '"+name+"';"
        c.execute(ur)

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
    fetch = "select id, name, consTime,total_days from consumables where name = '"+name+"';"
    c.execute(fetch)
    p = c.fetchone()
    d = "delete from consumables where id = '"+str(p[0])+"';"
    insert = """insert into deleteds (name,consTime,total_days) 
             values ('"""+name+"""','"""+str(p[2])+"""','"""+str(p[3])+"""');"""
    c.execute(d)
    c.execute(insert)
    db.commit()

def shownames():
    os.system('clear')
    c = db.cursor()
    q = "select name from consumables;"
    c.execute(q)
    names = c.fetchall()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column ("NAMES", justify="left")

    for name in names:
        table.add_row(str(name[0]))

    console.print(table)


def show():
    os.system('clear')
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

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column ("INFO", justify="left")
    table.add_column("BOOKS", justify="center")
    table.add_column("SERIES", justify="center")
    table.add_column("MOVIES", justify="center")
    table.add_column("OVERALL", justify="center")

    table.add_row("TOTAL CONSUMPTION TIME (IN HOURS)",str(btd[0]),str(std[0]),str(mtd[0]),str(at[0]))
    table.add_row("TOTAL CONSUMPTION DAYS",str(btd[1]),str(std[1]),str(mtd[1]),str(at[1]))
    table.add_row("AVERAGE RATING",str(btd[2])[:4],str(std[2])[:4],str(mtd[2])[:4],str(r[0])[:4])
    table.add_row("TOTAL COUNT",str(btd[3]),str(std[3]),str(mtd[3]),str(r[1]))

    console.print(table)


def showind(typ):
    c = db.cursor()
    query = "select name,total_days,consTime,rating from consumables where type = '"+typ+"';"
    c.execute(query)
    lst = c.fetchall()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column ("NAME", justify="left")
    table.add_column("TOTAL DAYS", justify="center")
    table.add_column("TOTAL TIME (IN HOURS)", justify="center")
    table.add_column("RATING (OUT OF 10)", justify="center")

    for item in lst:
        table.add_row(str(item[0]),str(item[1]),str(item[2]),str(item[3]))

    console.print(table)


def fulldetail(name):
    c = db.cursor()
    query = "select * from consumables where name = '"+name+"';"
    c.execute(query)
    lst = c.fetchone()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("TYPE")
    table.add_column ("NAME", justify="left")
    table.add_column("START DATE", justify="center",no_wrap=False)
    table.add_column("END DATE", justify="center",no_wrap=False)
    table.add_column("RATING (OUT OF 10)", justify="center")
    table.add_column("TOTAL TIME (IN HOURS)", justify="center")
    table.add_column("TOTAL DAYS", justify="center")

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
            shownames()
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
            typeOptions = 'Type the name of the Consumable\nType none or -1 to cancel and return to the main menu\n'
            name = input(typeOptions)
            if not name.lower() in ['none','-1']:
                dlt(name)
                print('Record Has been Dleted !!!')
                input("Press any key to return to the Main Menu")
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
                    shownames()
                    name = input("Enter the name of the consumable : ")
                    fulldetail(name)
                input('\nPress any key to return to the Main Menu')
            else:
                continue
        elif(choice=='5'):
            show()
            response = input("\nPress Any key to go to the Main menu")
            if response.lower() in ['1','cancel']:
                continue
    else:
        break

db.close()
