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
        # self.tempVarList = set()
        self.buffer = []

    def flush(self):
        if(len(self.buffer) == 0): return
        if(len(self.buffer) == 1):
            self.code.addLine("result.append(%s)" % self.buffer[0])
        else:
            self.code.addLine("result.extend([%s])" % ",".join(self.buffer))
        self.buffer = []
    
    def compile(self,ast):
        self.code.addLine("""def render_function(context,library,do_dots):""")
        self.code.indent()
        section = self.code.addSection()
        self.code.addLine("result = []")

        self.template(ast,[])

        for var in self.varList:
            section.addLine("c_{name} = context['{n}']".format(name=var,n=var))
        self.code.addLine("""return "".join(result)""")
        result = str(self.code)
        self.code = CodeBuilder()
        self.varList = []
        return result
    
    def expression(self,node: Expression,toStr=True):
        name = "c_{n}".format(n=node.name)
        # for subName in node.subNameList:
        #     if(subName.isdigit()):
        #         name += "[{n}]".format(n=subName)
        #     else:
        #         name += "['{n}']".format(n=subName)
        if(node.subNameList != []):
            args = ", ".join([repr(arg) for arg in node.subNameList])
            name = "do_dots({name},{args})".format(name=name,args=args)
        for filter in node.filterList: #FIXME:
            name = "library.filter['{f}']({n})".format(f=filter,n=name)
        if(toStr): name = "str({n})".format(n=name)
        return name

    def template(self,ast,tempVarList):
        for node in ast.nodeList:
            if(isinstance(node, Literal)):
                self.buffer.append(repr(node.text))
            if(isinstance(node, Expression)):
                self.buffer.append(self.expression(node))
                if(node.name not in tempVarList): self.varList.add(node.name)
            if(isinstance(node,FOR)):
                self.flush()
                self.code.addLine("for c_{var} in {iter}:".format(var=node.var.name,iter=self.expression(node.iter,False)))
                # self.varList.add(node.var.name)
                self.varList.add(node.iter.name)
                # self.tempVarList.add(node.var.name)
                tempVarList.append(node.var.name)
                self.code.indent()
                self.template(node.body,tempVarList)
                self.code.dedent()
            if(isinstance(node,MACRO)):
                self.flush()
                name = node.macroName
                valueList = ["c_" + value for value in node.valueList]
                valueStr = ",".join(valueList)
                self.code.addLine("def macro_{name}({lis}):".format(name=name,lis=valueStr))
                self.code.indent()
                self.template(node.macroBody,node.valueList)
                self.code.dedent()
            if(isinstance(node,CALL)):
                self.flush()
                macroName = node.name
                lis = []
                for value in node.valueList:
                    if(value.name not in tempVarList): self.varList.add(value.name)
                    lis.append(self.expression(value,False))
                valueStr = ",".join(lis)
                self.code.addLine("macro_{name}({lis})".format(name=macroName,lis=valueStr))
        self.flush()
