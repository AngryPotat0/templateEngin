from Render import *
import datetime

render = Render("template.html")

productList = [{"name":"book","price":12},{"name":"cup","price":22},{"name":"keyboard","price":530}]
context = {"userName":"angryPotato","age":15,"productList":productList}

# toM = lambda x: "$" + str(x)
@render.registerTag
def currentTime(*args):
    now_time = str(datetime.datetime.now())
    return now_time

# render.library.registerFilter("toM",toM)
@render.registerFilter("toM")
def func(x):
    return "$" + str(x)

# render.library.registerTag("currentTime",currentTime)
render.compile()
html = render.render(context)
print(html)
