from re import S
from Parser import *

class CodeBuilder:
    def __init__(self,level = 0) -> None:
        self.code = []
        self.level = level
    
    def addLine(self, line):
        self.code.append(" " * self.level + line + "\n")
    
    def indent(self):
        self.level += 4
    
    def dedent(self):
        self.level -= 4
    
    def addSection(self):
        section = CodeBuilder(self.level)
        self.code.append(section)
        return section

    def getCode(self):
        if(self.level != 0):
            return None
        return str(self)
    
    def __str__(self) -> str:
        return "".join(str(line) for line in self.code)

class Compiler:
    def __init__(self) -> None:
        self.code = CodeBuilder()
        self.varList = set()
        self.tempVarList = set()
        self.buffer = []

    def flush(self):
        if(len(self.buffer) == 0): return
        if(len(self.buffer) == 1):
            self.code.addLine("result.append(%s)" % self.buffer[0])
        else:
            self.code.addLine("result.extend([%s])" % ",".join(self.buffer))
        self.buffer = []
    
    def compile(self,ast):
        self.code.addLine("""def render_function(context):""")
        self.code.indent()
        section = self.code.addSection()
        self.code.addLine("result = []")

        self.template(ast)

        for var in self.varList - self.tempVarList:
            section.addLine("c_{name} = context['{n}']".format(name=var,n=var))
        self.code.addLine("""return "".join(result)""")
        result = str(self.code)
        self.code = CodeBuilder()
        self.varList = []
        return result
    
    def expression(self,node: Expression):
        name = "c_{n}".format(n=node.name)
        for subName in node.subNameList:
            name += "['{n}']".format(n=subName)
        for filter in node.filterList: #FIXME:
            name = "{f}({n})".format(f=filter,n=name)
        name = "str({n})".format(n=name)
        return name

    def template(self,ast):
        for node in ast.nodeList:
            if(isinstance(node, Literal)):
                self.buffer.append(repr(node.text))
            if(isinstance(node, Expression)):
                self.buffer.append(self.expression(node))
                self.varList.add(node.name)
            if(isinstance(node,FOR)):
                self.flush()
                self.code.addLine("for c_{var} in c_{iter}:".format(var=node.var.name,iter=node.iter.name))
                self.varList.add(node.var.name)
                self.varList.add(node.iter.name)
                self.tempVarList.add(node.var.name)
                self.code.indent()
                self.template(node.body)
                self.code.dedent()
        self.flush()
