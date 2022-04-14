import datetime
import string
import sys
sys.path.append('../')
from PBL.Token_Types_Enum import TokenType

#Token value si type
#Cu error
delimeters = {".": ".", ",": ",", ":": ":", "/": "/", "|": "|", "_": "_", "-": "-", "eof": "EOF"}

###Puntuation tokens
singleTokens = {
    ".": "DOT", ",": "COMMA", ";": "SEMICOLON", ":": "COLON", "#": "HASHTAG",
    "{": "LBRACE", "}": "RBRACE", "(": "LPAREN", ")": "RPAREN", "[": "LBRACKET", "]": "RBRACKET",
     "/": "SLASH", "\\": "BACK_SLASH", "\"": "DOUBLE_QUOTE", "\'": "SINGLE_QUOTE"
}

###Operation tokens
operationTokens = {
    "<": "SMALLER", ">": "BIGGER", "=": "EQUAL", "!": "NEGATION", "!=": "NEGATION_EQUAL", "/": "SLASH", "%": "MOD",
    "==": 'EQUAL_EQUAL', ">=": "BIGGER_EQUAL", "<=": "SMALLER_EQUAL", "*": "MULT", "+": "PLUS", "-": "MINUS",
}

###Keyword tokens
keywordTokens = {
    "int": "INT", "double": "DOUBLE", "bool": "BOOLEAN_VAR", "chars": 'CHARS', "text": "TEXT_VAR",
    "words": "WORDS", "date": "DATE", "money": "MONEY", "phonenum": "PHONENUM",
    "template": "TEMPLATE", "actions": "ACTIONS", "open": "OPEN", "params": "PARAMS", "enum": "ENUM",
    "pack": "PACK", "sentences": "SENTENCES", "global": "GLOBAL", "create": "CREATE", "make": "MAKE",
    "contains": "CONTAINS", "print": "PRINT", "error": "ERROR", "input": "INPUT", "return": "RETURN",
    "right": "RIGHT", "left": "LEFT", "merge": "MERGE", "split": "SPLIT", "replace": "REPLACE",
    "for": "FOR", "until": "UNTIL", "do": "DO", "if": "IF", "else": "ELSE",
    "and": "AND", "or": "OR", "true": "TRUE", "false": "FALSE", "not": "NOT",
    "fontsize": "FONTSIZE", "font": "FONT", "length": "LENGTH", "begin": "BEGIN", "end": "END",
    "doc": "DOC", "pdf": "PDF", "docx": "DOCX", "html": "HTML", "csv": "CSV", "num":"NUMBER"
}

dataType = {
    "int": "INT", "double": "DOUBLE", "bool": "BOOLEAN_VAR", "chars": 'CHARS', "text": "TEXT_VAR",
    "words": "WORDS", "date": "DATE", "money": "MONEY", "phonenum": "PHONENUM", "num":"NUMBER"
}

### tokens with slash \u , \i ,\center , \b , \color , \line , \space , \t
textTokens = {
    "u": "UNDERLINE", "i": "ITALIC", "center": "CENTER", "b": "BOLD", "color": "COLOR", "line": "LINE", "space": "SPACE",
    "t": "TAB"
}

### tokens for colors
colorTokens = {
    "red": "RED", "blue": "BLUE", "green": "GREEN", "magenta": "MAGENTA", "white": "WHITE",
    "yellow": "YELLOW", "brown": "BROWN", "grey": "GREY", "black": "BLACK"
}


######################
### Token class
######################
class Token:
    def __init__(self, value, type,lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column
    def __str__(self):
        #String representation of the class instance.
        #Example:
        #     Token(TokenType.INTEGER, 7, position=5:10)
        
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column,
        )

    def __repr__(self):
        return self.__str__()

######################
### Lexer class
######################
class Lexer:
    def __init__(self, inp):
        self.text = inp
        self.tokens = []
        self.current = 0
        self.line = 0
        self.length = 0
        self.column = 0
        self.error = False
        self.literals=string.printable.replace("\\","").replace("{","").replace("}","").replace("#","")

    # Reset values to initial values, will be called for each line
    def initializer(self, input_line):
        self.text = input_line
        self.current = 0
        self.line += 1
        self.column = 0
        self.length = len(input_line)
        self.error = False

    # increases the current counter
    def increaseCurrent(self):
        self.current += 1
        self.column += 1

    # Main function to tokenize a line input into tokens
    def tokenizer(self, input_line):
        self.initializer(input_line)
        # we have 4 main cases when current char is a: single character, operation, digit or alphabetic
        # we loop until end of line
        while self.current < self.length:
            current_char = self.text[self.current]
            # if newline we stop if whitespace then we skip
            if current_char == '\n':
                break
            if current_char == ' ' or current_char == '\t':
                self.increaseCurrent()
            elif current_char.isalpha():
                self.setKeywordTokens()
            elif current_char in singleTokens:
                self.setSingleTokens(current_char)
            elif current_char in operationTokens:
                self.setOperationTokens()
            elif current_char.isdigit():
                self.setDigitTokens()


    # for single characters we simply add them to tokens list
    def setSingleTokens(self, punctuation):
        # create a text token which is stored in quotes
        if punctuation == "\"":  # a = "hello"
            self.increaseCurrent()
            position = self.current
            while position != self.length:
                if self.text[position] != "\"":
                    position += 1
                    self.column+=1
                else:
                    position += 1
                    self.column+=1
                    break
            s = self.text[self.current:position - 1]
            token = Token(s,  TokenType("TEXT_LITERAL"),lineno=self.line, column=self.column)
            self.tokens.append(token)

            # set current to the new position
            self.current = position

        # commented code
        elif punctuation == "/" and self.text[self.current + 1] == "/":
            self.increaseCurrent()
            position = self.current
            while position != self.length:
                position += 1
                self.column+=1


            # set current to the new position
            self.current = position


        # if we find a backslash we get the first word(textToken) after and until we find another backslash we store text in a text var
        elif punctuation == "\\":
            self.tokens.append(Token(punctuation.upper(), TokenType(punctuation.upper()),lineno=self.line, column=self.column))
            self.increaseCurrent()
            position = self.current
            # get the first word after backslash
            while self.text[position].isalnum() and self.text[position] != "*" : #Does not tokenize when line*4 / space *7
                position += 1
                self.column+=1
            str = self.text[self.current:position]
            str.replace(" ","")
            # if it is a token then append otherwise an error
            if str in textTokens:
                token = Token(str.upper(), TokenType(str.upper()),lineno=self.line, column=self.column)
                self.tokens.append(token)
                if self.text[position]=="*":
                    token = Token(self.text[position].upper(), TokenType(self.text[position]),lineno=self.line, column=self.column)
                    self.tokens.append(token)
                    position+=1
                    self.column+=1
                    if self.text[position].isdigit():
                        self.current=position
                        self.setDigitTokens()
                        position=self.current
            else:
                token = Token(str,  TokenType("TEXT_LITERAL"),lineno=self.line, column=self.column)
                self.tokens.append(token)
    
            # set current to new position
            self.current = position

            # loop until we find the other backslash or }
            while self.text[position] in self.literals :
                position += 1
                self.column+=1
                if position==self.length:
                    break
            # store the text in between the slashes
            str = self.text[self.current:position]
            token = Token(str, TokenType("TEXT_LITERAL"),lineno=self.line, column=self.column)
            self.tokens.append(token)

            if  position!=self.length:
                token = Token(self.text[position].upper(),  TokenType(self.text[position].upper()),lineno=self.line, column=self.column)
                self.tokens.append(token)

            # set current to the new position
            self.current = position
            self.increaseCurrent()
        
        else:
            # simple other tokens
            token = Token(punctuation.upper(),  TokenType(punctuation.upper()),lineno=self.line, column=self.column+1)
            self.tokens.append(token)
            self.increaseCurrent()

    # we have a special function for operations like comparison operators since they can be more than 1 char
    def setOperationTokens(self):
        position = self.current
        while position != self.length:
            # if operation is longer than 2 chars like "===" we have an error
            if position - self.current > 2:
                self.error = True
                print("Too many operators error!")
            if self.text[position] in operationTokens:
                position += 1
                self.column+=1
            else:
                break
        operation = self.text[self.current:position]

        if not self.error:
            if operation in operationTokens:
                token = Token(operation.upper(),  TokenType(operation.upper()),lineno=self.line, column=self.column)
                self.tokens.append(token)
            else:
                if(operation=='=-' or operation=='=+'):
                    token = Token(operation[0],  TokenType(operation[0]),lineno=self.line, column=self.column)
                    self.tokens.append(token)
                    token = Token(operation[1],  TokenType(operation[1]),lineno=self.line, column=self.column)
                    self.tokens.append(token)
                else:
                    self.error = True
                    print(operation)
                    print("1Operation Error! Check line here: ", self.line)
        else:
            print("Operation Error! Check line: ", self.line)

        # set current to the new position
        self.current = position

    # we create an alphanumeric word and if it doesn't belong to keywords it'll be an identifier
    def setKeywordTokens(self):
        position = self.current
        while position != self.length:
            if self.text[position].isalnum():
                position += 1
                self.column+=1
            else:
                break
        # create keyword string by cutting text from current to position
        s = self.text[self.current:position]
        # if the string is a keyword
        if s.lower() in keywordTokens:
            token = Token(s.upper(),  TokenType(s.upper()),lineno=self.line, column=self.column)
            self.tokens.append(token)
        elif s.lower() in textTokens:          
            token = Token(s.upper(),  TokenType(s.upper()),lineno=self.line, column=self.column)
            self.tokens.append(token)
        # if the string is not a keyword it's an identifier
        else:
            token = Token(s,  TokenType("IDENTIFIER"),lineno=self.line, column=self.column)
            self.tokens.append(token)

        # set current to the new position
        self.current = position


    # we loop until we have either digits or a '.' char and create a number based off that
    def setDigitTokens(self):
        position = self.current
        dot_counter = 0  # keeping track of dots to avoid syntax error like "1.2.3" is not a number
        
        while position != self.length and (self.text[position].isdigit() or self.text[position]=='.'):
            current_char = self.text[position]
            # check if current char isn't a digit or a dot then break

            if current_char.isalpha():
                self.error = True
                break

            # increment dot counter
            if current_char == '.':
                dot_counter += 1
            position += 1
            self.column+=1

        number = self.text[self.current:position]

        # if we have no dots in the number string then it's an integer
        # if we have 1 dot it'll be a double, if 2 then date
        # otherwise it'll be a syntax error
        if not self.error:
            if dot_counter == 0:
                token = Token(int(number),  TokenType("NUM_LITERAL"),lineno=self.line, column=self.column)
                self.tokens.append(token)
            elif dot_counter == 1:
                # check for money format
                # if self.is_money(number):
                #     token = Token(number, "MONEY")
                #     self.tokens.append(token)
                # else:
                token = Token(float(number), TokenType("NUM_LITERAL"),lineno=self.line, column=self.column)
                self.tokens.append(token)
            elif dot_counter == 2:
                # check for date format
                number=number.replace('.','-')
                date=datetime.date.fromisoformat(number)
                token = Token(date, TokenType("DATE"),lineno=self.line, column=self.column)
                self.tokens.append(token)
            else:
                print("Syntax Error! Wrong format! Check line: ", self.line)
        else:
            print("Syntax Error! Wrong format! Check line: ", self.line)

        # set current to the new position
        self.current = position

    # check if number is a money format 125.50 2 decimal places
    def is_money(self, number):
        if "." in number:
            pos = number.find('.')
            if len(number[pos+1:]) != 2:
                return False
            else:
                return True

    def is_date(self, number):
        #check the date format
        print("Date is checked here")

    # print tokens array
    def print_tokens(self):
        for token in self.tokens:
            print(token)
            
    def get_tokens(self):
        self.tokens.append(Token("eof".upper(), TokenType("EOF")))
        return self.tokens

# lex = Lexer("")

# filename='./Lexer/test.txt'

# with open(filename) as openfileobject:
#     for line in openfileobject:
#         lex.tokenizer(line)
#         # print("linie "+line)
# lex.get_tokens()
# lex.print_tokens()