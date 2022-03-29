from Render import *
import datetime


productList = [{"name":"book","price":12},{"name":"cup","price":22},{"name":"keyboard","price":530}]
context = {"userName":"angryPotato","age":15,"productList":productList}

toM = lambda x: "$" + str(x)

def currentTime(*args):
    now_time = str(datetime.datetime.now())
    return now_time

library = Library()
library.registerFilter("toM",toM)
library.registerTag("currentTime",currentTime)
render = Render("template.html",library)
render.compile()
html = render.render(context)
print(html)
