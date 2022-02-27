from Lexer import *
from Parser import *
from Compiler import *

text = '''
<p>{{ viewsDict }}</p>
<p>{{ viewsDict.name }}</p>
'''

lex = Lexer(text)
lis = lex.lexer()
for token in lis:
    print(token)

p = Parser(lis)
template = p.parser()
print(template)

compiler = Compiler()
code = compiler.compile(template)
print(code)

views_dict = {"name":"AAC"}
context = {"viewsDict":views_dict}
func = exec(code)
print(render_function(context))