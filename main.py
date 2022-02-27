from Parser import *
from Lexer import *
from Compiler import *

text = '''
<p>Topics for {{name}}: {% for t in topics %}{{t}}, {% endfor %}</p>{{name}}
'''


lex = Lexer(text)
lis = lex.lexer()
# for token in lis:
#     print(token)

p = Parser(lis)
template = p.parser()
compiler = Compiler()
code = compiler.compile(template)
print(code)
context = {"name":"game","topics":["ttf2","bf1","deadcell","minecraft"]}
func = exec(code)
print(render_function(context))