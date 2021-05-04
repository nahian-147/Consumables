from rich.console import Console
from rich.table import Column,Table
import mysql.connector

db = mysql.connector.connect(
        host='localhost',
        user='nahian',
        password='Nahian_8',
        database='CONSUMABLES')

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
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column ("INFO", justify="left")
    table.add_column("BOOKS", justify="center")
    table.add_column("SERIES", justify="center")
    table.add_column("MOVIES", justify="center")
    table.add_column("OVERALL", justify="center")

    table.add_row("Total Consumption Time",str(btd[0]),str(std[0]),str(mtd[0]),str(at[0]))
    table.add_row("Total Consumption Days",str(btd[1]),str(std[1]),str(mtd[1]),str(at[1]))
    table.add_row("Average Rating",str(btd[2])[:4],str(std[2])[:4],str(mtd[2])[:4],str(r[0])[:4])
    table.add_row("Total Count",str(btd[3]),str(std[3]),str(mtd[3]),str(r[1]))

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
    table.add_column("TOTAL TIME", justify="center")
    table.add_column("RATING", justify="center")

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

show()
