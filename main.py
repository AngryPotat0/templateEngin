from Lexer import *
from Parser import *
from Compiler import *


class Library:
    def __init__(self) -> None:
        self.filter = dict()
        self.filter['len'] = len
    
    def registerFilter(self,name,func):
        self.filter[name] = func

class Render:
    def __init__(self,template,library=None) -> None:
        self.template = template
        self.render_functon = ""
        self.library = library

    def compile(self):
        lex = Lexer(self.template)
        for token in lex.lexer():
            print(str(token))
        p = Parser(lex.lexer())
        ast = p.parser()
        print(str(ast))
        compiler = Compiler()
        self.render_functon = compiler.compile(ast)
        print(self.render_functon)

    def render(self,context):
        def do_dots(value,*args):
            for dot in args:
                try:
                    value = getattr(value,dot)
                except AttributeError:
                    value = value[int(dot)] if dot.isdigit() else value[dot]
                if(callable(value)):
                    value = value()
            return value
        
        if(self.render_functon == ''):
            return None
        functions = {}
        exec(self.render_functon,functions)
        return functions["render_function"](context,self.library,do_dots)


template = '''
{% macro showProduct(product) %}
<li>{{ product.name }}: {{ product.price | doubleMe }}</li>
{% endmacro %}
<p>Welcome, {{userName}}!</p>
<p>Products:</p>
{% if age gte 20 %}
<p>Age={{age}}</p>
{% elif age gte 10 %}
<p>ok,{{age}}</p>
{% else %}
<P>Age less 20</p>
{% endif %}
<ul>
{% for product in productList %}
    {% call showProduct(product) %}
{% endfor %}
{% call showProduct(productList.0)%}
</ul>
'''

productList = [{"name":"book","price":12},{"name":"cup","price":22},{"name":"keyboard","price":530}]
context = {"userName":"angryPotato","age":15,"productList":productList}

# template = '''
# {% macro showProduct(a) %}
# <li>{{ a }}</li>
# {% endmacro %}
# <p>Welcome, {{userName}}!</p>
# <p>Products:</p>
# <ul>
# {% for productKey in productList.keys %}
#     {% call showProduct(productKey) %}
# {% endfor %}
# </ul>
# '''


# productList = {"name":"book","price":12,"palce":"home","tag":"useless"}
# context = {"userName":"angryPotato","productList":productList}

addN = lambda x: x + "NNN"
doubleMe = lambda x: x * 2

library = Library()
library.registerFilter('addN',addN)
library.registerFilter("doubleMe",doubleMe)

render = Render(template,library)
render.compile()
html = render.render(context)
print(html)
