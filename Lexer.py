from enum import Enum

class TokenType(Enum):
    LITERAL =   'LITERAL'
    EXPR    =   'EXPR'
    TAG     =   'TAG'
    IF      =   'if'
    ELIF    =   'elif'
    ELSE    =   'else'
    ENDIF   =   'endif'
    FOR     =   'for'
    IN      =   'in'
    ENDFOR  =   'endfor'
    EOF     =   'EOF'


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

    def expression(self):
        self.next()
        self.next() #eat {{
        expr = ''
        while(self.currentChar != None and (self.currentChar.isalpha() or self.currentChar in ('.', '|',' '))):
            if(self.currentChar == ' '):
                self.skipWhiteSpace()
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
                self.tokenList.append(Token(TokenType.IF,word))
            elif(word == 'endfor'):
                self.tokenList.append(Token(TokenType.ENDFOR,word))
            elif(word == 'in'):
                self.tokenList.append(Token(TokenType.IN,word))
            else:
                self.tokenList.append(Token(TokenType.EXPR,word))

        while(self.currentChar != None and (self.currentChar.isalpha() or self.currentChar == ' ')):
            if(self.currentChar == ' '):
                addToken(temp)
                temp = ''
                self.skipWhiteSpace()
                continue
            temp += self.currentChar
            self.next()
        if(self.currentChar == '%' and  self.peek() == '}'):
            self.next()
            self.next()
        else:
            raise Exception("Unexpected char at index {}\n".format(self.currentIndex))

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