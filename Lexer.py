from cmath import exp
from enum import Enum

class TokenType(Enum):
    LITERAL     =   'LITERAL'
    EXPR        =   'EXPR'
    TAG         =   'TAG'
    IF          =   'if'
    DOT         =   '.'
    FILTER      =   '|'
    LPAREN      =   '('
    RPAREN      =   ')'
    COMMA       =   ','
    ELIF        =   'elif'
    ELSE        =   'else'
    ENDIF       =   'endif'
    FOR         =   'for'
    IN          =   'in'
    ENDFOR      =   'endfor'
    MACRO       =   'macro'
    ENDMACRO    =  'endmacro'
    CALL        =   'call'
    # ENDCALL     =   'endcall'
    EOF         =   'EOF'


class Token:
    def __init__(self, tokenType, tokenValue) -> None:
        self.tokenType = tokenType
        self.tokenValue = tokenValue
    
    def __str__(self):
        return '{type},{value}'.format(type=self.tokenType, value=self.tokenValue)

class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.currentIndex = 0
        self.currentChar = self.text[self.currentIndex]
        self.lenOfText = len(text)
        self.tokenList = []

    def next(self):
        self.currentIndex += 1
        if(self.currentIndex >= self.lenOfText):
            self.currentChar = None
        else:
            self.currentChar = self.text[self.currentIndex]
    
    def peek(self):
        pos = self.currentIndex + 1
        if(pos >= self.lenOfText):
            return None
        return self.text[pos]
    
    def skipWhiteSpace(self):
        while(self.currentChar != None and self.currentChar == ' '):
            self.next()

    def expression(self): #FIXME:
        self.next()
        self.next() #eat {{
        expr = ''
        while(self.currentChar != None and (self.currentChar.isalpha() or self.currentChar in ('.', '|',' '))):
            if(self.currentChar == ' '):
                self.skipWhiteSpace()
                continue
            if(self.currentChar == '.'):
                self.tokenList.append(Token(TokenType.EXPR,expr))
                expr = ''
                self.tokenList.append(Token(TokenType.DOT,'.'))
                self.next()
                continue
            if(self.currentChar == '|'):
                self.tokenList.append(Token(TokenType.EXPR,expr))
                expr = ''
                self.tokenList.append(Token(TokenType.FILTER,'|'))
                self.next()
                continue
            expr += self.currentChar
            self.next()
        if(self.currentChar == '}' and self.peek() == '}'):
            self.next()
            self.next()
        else:
            raise Exception("Unexpected char at index {}\n".format(self.currentIndex))
        self.tokenList.append(Token(TokenType.EXPR,expr))

    def tag(self):
        self.next()
        self.next() #eat {%
        temp = ''

        def addToken(word):
            if(word == ''): return
            if(word == 'for'):
                self.tokenList.append(Token(TokenType.FOR,word))
            elif(word == 'endfor'):
                self.tokenList.append(Token(TokenType.ENDFOR,word))
            elif(word == 'in'):
                self.tokenList.append(Token(TokenType.IN,word))
            elif(word == 'macro'):
                self.tokenList.append(Token(TokenType.MACRO,word))
            elif(word == 'endmacro'):
                self.tokenList.append(Token(TokenType.ENDMACRO,word))
            elif(word == 'call'):
                self.tokenList.append(Token(TokenType.CALL,word))
            # elif(word == 'endcall'):
            #     self.tokenList.append(Token(TokenType.ENDCALL,word))
            else:
                self.tokenList.append(Token(TokenType.EXPR,word))

        while(self.currentChar != None and (self.currentChar.isalpha() or self.currentChar in (' ','(',')',','))):
            if(self.currentChar in (' ','(',')',',')):
                if(temp != ''):
                    addToken(temp)
                    temp = ''
                if(self.currentChar == '('):
                    self.tokenList.append(Token(TokenType.LPAREN,'('))
                elif(self.currentChar == ')'):
                    self.tokenList.append(Token(TokenType.RPAREN,')'))
                elif(self.currentChar == ','):
                    self.tokenList.append(Token(TokenType.COMMA,','))
                if(self.currentChar == ' '):
                    self.skipWhiteSpace()
                else:
                    self.next()
                continue
            temp += self.currentChar
            self.next()
        if(self.currentChar == '%' and  self.peek() == '}'):
            self.next()
            self.next()
        else:
            raise Exception("Unexpected char at index {}\n".format(self.currentIndex))
        if(self.currentChar == '\n'):
            self.next()

    def literal(self):
        literal = ''
        while(self.currentChar != None and self.currentChar != '{'):
            if(self.currentChar == '\\'):
                literal += self.peek()
            else:
                literal += self.currentChar
            self.next()
        self.tokenList.append(Token(TokenType.LITERAL,literal))
    
    def lexer(self):
        while(True):
            if(self.currentChar == None):
                self.tokenList.append(Token(TokenType.EOF,'EOF'))
                break
            if(self.currentChar == '\n'):
                self.next()
                continue
            # if(self.currentChar == ' '):
            #     self.skipWhiteSpace()
            #     continue
            if(self.currentChar == '{'): #LLBRACE OR LTAG
                nextChar = self.peek()
                if(nextChar == '{'): #expression
                    self.expression()
                elif(nextChar == '%'): #tag
                    self.tag()
                else:
                    raise Exception("Unexpected char at index {}".format(self.currentIndex + 1))
            self.literal()
        
        return self.tokenList