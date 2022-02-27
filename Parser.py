from email.quoprimime import body_check
from Lexer import *
from typing import List

class AST:
    pass

class Template(AST):
    def __init__(self) -> None:
        self.nodeList = []
    
    def __str__(self) -> str:
        ans = ""
        for node in self.nodeList:
            ans += str(node)
        return ans + "\n"

class Literal(AST):
    def __init__(self,text) -> None:
        self.text = text

    def __str__(self) -> str:
        return "Literal: " + self.text + "\n"

class Expression(AST):
    def __init__(self,name) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return "Expression: " + self.name + "\n"

class FOR(AST):
    def __init__(self,var,iter,body) -> None:
        self.var = var
        self.iter = iter
        self.body = body
    
    def __str__(self) -> str:
        return "For: " + str(self.var) + str(self.iter) + str(self.body)  + "END FOR\n"

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

class Parser:
    def __init__(self,tokenList: List[Token]) -> None:
        self.tokenList = tokenList
        self.currentIndex = 0
        self.currentToken = self.tokenList[self.currentIndex]

    def error(self,msg):
        raise Exception(msg)

    def eat(self,tokenType):
        if(self.currentToken.tokenType != tokenType):
            self.error("Parser Error: Unexpected token {}".format(self.currentToken.tokenValue))
        else:
            self.currentIndex += 1
            self.currentToken = self.tokenList[self.currentIndex]

    def parser(self):
        template = self.template()
        if(self.currentToken.tokenType != TokenType.EOF):
            self.error("EEEEEEEERRRRRROOOOORRRRRRRR!!!!!!!!!!!!!!!")
        return template

    def template(self):
        template = Template()
        while(self.currentToken.tokenType != TokenType.EOF):
            if(self.currentToken.tokenType == TokenType.LITERAL):
                template.nodeList.append(Literal(self.currentToken.tokenValue))
                self.eat(TokenType.LITERAL)
                continue
            elif(self.currentToken.tokenType == TokenType.EXPR):
                template.nodeList.append(self.expression())
                continue
            elif(self.currentToken.tokenType == TokenType.FOR):
                template.nodeList.append(self.forLoop())
                continue
            else:
                break
        return template

    def expression(self): # 现在表达式只有变量名
        expression = self.currentToken.tokenValue
        self.eat(TokenType.EXPR)
        return Expression(expression)

    def forLoop(self):
        self.eat(TokenType.FOR)
        var = self.expression()
        self.eat(TokenType.IN)
        iters = self.expression()
        body = self.template()
        self.eat(TokenType.ENDFOR)
        return FOR(var,iters,body)
