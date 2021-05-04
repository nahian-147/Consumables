import os
from datetime import date
import mysql.connector
from rich.console import Console
from rich.table import Column,Table

hs = "bold blue"

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

    if start == "":
        today = date.today().strftime("%Y-%m-%d")
        start = str(today)
    
    insert = """insert into consumables (type,name,consStart) 
            values ('"""+t+"""','"""+name+"""','"""+start+"""');"""
    try:
        c.execute(insert)
        if not end == "":
            ue = "update consumables set consEnd = '"+end+"' WHERE name = '"+name+"';"
            c.execute(ue)
        if not rating == "":
            ur = "update consumables set rating = '"+rating+"' WHERE name = '"+name+"';"
            c.execute(ur)
        input("A new Consumable has been added successfully.\nPress any key to return back to the main menu.")
    except:
        db.rollback()
        input("Sorry, Record couldn't be inserted. Please, try again.")
    db.commit()

def addTime(cid,hours):
    c = db.cursor(buffered=True)
    q1 = "UPDATE consumables SET consTime = consTime + "+hours+" WHERE id  = '"+cid+"';"
    q2 = "UPDATE total SET total_time = total_time + "+hours+";"
    try:
        c.execute(q1)
        c.execute(q2)
        input("Time has been added successfully.\nPress any key to return back to the main menu.")
    except:
        db.rollback()
        input("Time could not be updated.Please try again.")
    db.commit()

def aday(cid):
    c = db.cursor(buffered=True)
    q1 = "UPDATE consumables SET total_days = total_days + 1 WHERE id  = '"+str(cid)+"';"
    q2 = "UPDATE total SET total_days = total_days + 1;"
    try:
        c.execute(q1)
        c.execute(q2)
        input("A day to the Consumable has been added successfully.\nPress any key to return back to the main menu.")
    except:
        db.rollback()
        input("A day could not be added.Please try again.")
    db.commit()

def chngRating(cid,rating):
    c = db.cursor(buffered=True)
    q = "update consumables set rating = "+rating+" where id  = '"+str(cid)+"';"
    try:
        c.execute(q)
        input("Rating has been updated successfully.\nPress any key to return back to the main menu.")
    except:
        db.rollback()
        input("Rating Could not be updated.Please try again.")
    db.commit()

def setEdate(cid):
    date = input("Date ? : ")
    c = db.cursor()
    q1 = "select consEnd from consumables where id = '"+str(cid)+"';"
    c.execute(q1)
    p = c.fetchall()
    print(p,len(p))
    input()
    if len(p)-1 == 0:
        q2 = "update consumables set consEnd = '"+date+"' where id = '"+str(cid)+"';"
        try:
            c.execute(q2)
        except:
            db.rollback()
            input("There was an error Setting the Date !\nPress Enter to return back to the main menu.")
        db.commit()
        input("Ending Date has been Set successfully.\nPress any key to return back to the main menu.")
    else:
        input("Can't Update now !\nPress Enter to return back to the main menu.")

def dlt(cid):
    
    c = db.cursor()
    fetch = "select * from consumables where id = '"+cid+"';"
    c.execute(fetch)
    p = c.fetchone()
    d = "delete from consumables where id = '"+str(cid)+"';"
    
    name = p[2]
    t = p[1]
    start = str(p[3])
    end = str(p[4])
    rating = str(p[5])
    time = str(p[6])
    days = str(p[7])
    
    insert = """insert into deleteds (id,type,name,consStart,rating,consTime,total_days) 
            values ('"""+str(cid)+"""','"""+t+"""','"""+name+"""','"""+start+"""','"""+rating+"""','"""+time+"""','"""+days+"""');"""
    
    try:
        c.execute(insert)
        c.execute(d)
    except:
        db.rollback()
        print("An Error Occurred!!! Please, try again.")
    else:
        db.commit()
        input("Selected Consumable has been Deleted Successfully.\nPress any key to return back to the main menu.")
    

def rstr(cid):
    c = db.cursor()
    fetch = "select * from deleteds where id = '"+str(cid)+"';"
    c.execute(fetch)
    p = c.fetchone()
    d = "delete from deleteds where id = '"+str(cid)+"';"
    
    name = p[2]
    t = p[1]
    start = str(p[3])
    end = str(p[4])
    rating = str(p[5])
    time = str(p[6])
    days = str(p[7])
    
    insert = """insert into consumables (id,type,name,consStart,rating,consTime,total_days) 
            values ('"""+str(cid)+"""','"""+t+"""','"""+name+"""','"""+start+"""','"""+rating+"""','"""+time+"""','"""+days+"""');"""
    try:
        c.execute(insert)
        c.execute(d)
    except:
        db.rollback()
        print("An Error Occurred!!! Please, try again.")
    else:
        db.commit()
        input("Selected Consumable has been Restored Successfully.\nPress any key to return back to the main menu.")

def shownames():
    os.system('clear')
    c = db.cursor()
    q = "select id,name from consumables;"
    c.execute(q)
    names = c.fetchall()

    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("ID", justify="left")
    table.add_column ("NAMES", justify="left")

    for name in names:
        table.add_row(str(name[0]),str(name[1]))

    console.print(table)

def shownames_del():
    os.system('clear')
    c = db.cursor()
    q = "select id,name from deleteds;"
    c.execute(q)
    names = c.fetchall()

    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("ID", justify="left")
    table.add_column ("NAMES", justify="left")

    for name in names:
        table.add_row(str(name[0]),str(name[1]))

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
    table = Table(show_header=True, header_style=hs)
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
    os.system('clear')
    c = db.cursor()
    query = "select name,total_days,consTime,rating from consumables where type = '"+typ+"';"
    c.execute(query)
    lst = c.fetchall()

    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("NAME", justify="left")
    table.add_column("TOTAL DAYS", justify="center")
    table.add_column("TOTAL TIME (IN HOURS)", justify="center")
    table.add_column("RATING (OUT OF 10)", justify="center")

    for item in lst:
        table.add_row(str(item[0]),str(item[1]),str(item[2]),str(item[3]))

    console.print(table)


def fulldetail(cid):
    c = db.cursor()
    query = "select * from consumables where id = '"+cid+"';"
    c.execute(query)
    lst = c.fetchone()

    console = Console()
    table = Table(show_header=True, header_style=hs)
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

def showoptn():
    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("#", justify="left")
    table.add_column ("CHOICE", justify="left")
    table.add_row("1","Add a Consumable")
    table.add_row("2","Edit a Consumable")
    table.add_row("3","Delete a Consumable")
    table.add_row("4","Restore a Consumable")
    table.add_row("5","See the list of consumables and individually")
    table.add_row("6","See overall info")
    table.add_row("7","Exit")
    console.print(table)

def showoptn_1():
    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("#", justify="left")
    table.add_column ("CHOICE", justify="left")
    table.add_row("1","Books")
    table.add_row("2","Series")
    table.add_row("3","Movie")
    table.add_row("4","None")
    console.print("Select one Consumable from below : ")
    console.print(table)

def showoptn_2():
    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("#", justify="left")
    table.add_column ("Actions", justify="left")
    table.add_row("1","Add time in Hours")
    table.add_row("2","Add a day")
    table.add_row("3","Change the Rating of a Specific Consumable")
    table.add_row("4","Change Consumption Ening date")
    table.add_row("5","None")
    console.print("Select one Action from below : ")
    console.print(table)

def showoptn_5():
    console = Console()
    table = Table(show_header=True, header_style=hs)
    table.add_column ("#", justify="left")
    table.add_column ("Actions", justify="left")
    table.add_row("1","Book")
    table.add_row("2","Series")
    table.add_row("3","Movie")
    table.add_row("4","Individual")
    table.add_row("5","None")
    console.print("Select one Option from below : ")
    console.print(table)

while True:
    os.system('clear')
    showoptn()
    choice = input("Please type in your choice number : ")
    if(not choice.lower() in ['7','exit']):
        if(choice=='1'):
            os.system('clear')
            showoptn_1()
            typ = input()
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
            os.system('clear')
            shownames()
            cid = input("Enter the id of the Consumable : ")
            showoptn_2()
            action = input()
            if not action.lower() in ['5','none']:
                if action == '1':
                    hours = input("How many Hours ? : ")
                    addTime(cid,hours)
                elif action == '2':
                    aday(cid)
                elif action =='3':
                    rating = input("New Rating ? : ")
                    chngRating(cid,rating)
                elif action == '4':
                    setEdate(cid)
            else:
                continue
        elif(choice=='3'):
            shownames()
            typeOptions = 'Type the ID of the Consumable You want to Delete !!!\nType none or -1 to cancel and return to the main menu\n'
            cid = input(typeOptions)
            if not cid.lower() in ['none','-1']:
                dlt(cid)
            else:
                continue
        elif(choice=='4'):
            shownames_del()
            typeOptions = 'Type the ID of the Consumable You want to Restore !!!\nType none or -1 to cancel and return to the main menu\n'
            cid = input(typeOptions)
            if not cid.lower() in ['none','-1']:
                rstr(cid)
            else:
                continue
        elif(choice=='5'):
            os.system('clear')
            showoptn_5()
            typ = input()
            if not typ.lower() in ['5','none']:
                if(typ=='1'):
                    showind('Book')
                elif(typ=='2'):
                    showind('Series')
                elif(typ == '3'):
                    showind('Movie')
                elif typ == '4':
                    shownames()
                    cid = input("Enter the id of the consumable : ")
                    fulldetail(cid)
                input('\nPress any key to return back to the main menu.')
            else:
                continue
        elif(choice=='6'):
            show()
            response = input("\nPress any key to return back to the main menu.")
            continue
    else:
        break

db.close()
