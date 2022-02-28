from Lexer import *
from Parser import *
from Compiler import *

class Render:
    def __init__(self,template) -> None:
        self.template = template
        self.render_functon = ""

    def compile(self):
        lex = Lexer(self.template)
        p = Parser(lex.lexer())
        ast = p.parser()
        compiler = Compiler()
        self.render_functon = compiler.compile(ast)

    def render(self,context):
        if(self.render_functon == ''):
            return None
        functions = {}
        exec(self.render_functon,functions)
        return functions["render_function"](context)


template = '''
<p>{{ viewsDict }}</p>
<p>{{ viewsDict.name | abs}}</p>
'''
views_dict = {"name":-123}
context = {"viewsDict":views_dict}

render = Render(template)
render.compile()
html = render.render(context)
print(html)