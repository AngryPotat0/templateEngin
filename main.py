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
        self.extendsTemplate = None
        self.render_functon = None
        self.base_function = None
        self.library = library

    def extends(self,line):
        fileName = line[2:len(line) - 2].split()[1]
        with open(fileName,'r') as f:
            self.extendsTemplate = f.read()

    def compile(self):
        line = ""
        for c in self.template:
            if(c == '\n'): break
            line += c
        if(len(line) > 2 and line[0] == '{' and line[1] == '@'): self.extends(line)

        lex = Lexer(self.template)
        # for token in lex.lexer():
        #     print(str(token))
        p = Parser(lex.lexer())
        ast = p.parser()
        # print(str(ast))
        compiler = Compiler()
        self.render_functon = compiler.compile(ast)
        # print(self.render_functon)

        if(self.extendsTemplate != None):
            lex = Lexer(self.extendsTemplate)
            p = Parser(lex.lexer())
            ast = p.parser()
            self.base_function = compiler.compile(ast)
            # print("#################")
            # print(self.base_function)
        

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
        base_functions = {}
        exec(self.render_functon,functions)
        if(self.base_function != None):
            exec(self.base_function,base_functions)
            for functionName in functions.keys():
                if(functionName == 'render'): continue
                if(functionName in base_functions): base_functions[functionName] = functions[functionName]
            return base_functions["render"](context,self.library,do_dots)
        else:
            return functions["render"](context,self.library,do_dots)

blockTemp = '''{@extends base.html@}
{% block tes %}
    Relpace
{% endblock %}

'''
#{@extends base.html@}
template = '''{% macro showProduct(product) %}
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

render = Render(blockTemp,library)
render.compile()
html = render.render(context)
print(html)
