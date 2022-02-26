import imp
from Lexer import *

text = '''
<p>Topics for {{name}}: {% for t in topics %}lis:{{t}}, {% endfor %}</p>
'''


lex = Lexer(text)
lis = lex.lexer()
for token in lis:
    print(token)
