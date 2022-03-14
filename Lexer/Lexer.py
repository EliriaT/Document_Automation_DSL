from datetime import datetime

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
    "doc": "DOC", "pdf": "PDF", "docx": "DOCX", "html": "HTML", "csv": "CSV"
}

dataType = {
    "int": "INT", "double": "DOUBLE", "bool": "BOOLEAN_VAR", "chars": 'CHARS', "text": "TEXT_VAR",
    "words": "WORDS", "date": "DATE", "money": "MONEY", "phonenum": "PHONENUM",
}

### tokens with slash \u , \i ,\center , \b , \color , \line , \space , \t
textTokens = {
    "u": "UNDERLINE", "i": "PRINT", "center": "CENTER", "b": "BOLD", "color": "COLOR", "line": "LINE", "space": "SPACE",
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
    def __init__(self, type, value):
        self.type = type
        self.value = value


######################
### Lexer class
######################
class Lexer:
    def __init__(self, inp):
        self.text = inp
        self.tokens = []
        self.current = 0
        self.line = -1
        self.length = 0
        self.error = False

    # Reset values to initial values, will be called for each line
    def initializer(self, input_line):
        self.text = input_line
        self.current = 0
        self.line += 1
        self.length = len(input_line)
        self.error = False

    # increases the current counter
    def increaseCurrent(self):
        self.current += 1

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
                else:
                    position += 1
                    break
            s = self.text[self.current:position - 1]
            token = Token(s, "TEXT")
            self.tokens.append(token)

            # set current to the new position
            self.current = position

        # commented code
        elif punctuation == "/" and self.text[self.current + 1] == "/":
            self.increaseCurrent()
            position = self.current
            while position != self.length:
                position += 1

            # set current to the new position
            self.current = position

        # if we find a backslash we get the first word(textToken) after and until we find another backslash we store text in a text var
        elif punctuation == "\\":
            self.tokens.append(Token(punctuation, "BACK_SLASH"))
            self.increaseCurrent()
            position = self.current
            # get the first word after backslash
            while self.text[position].isalnum() or self.text[position] == "*":
                position += 1
            str = self.text[self.current:position]
            # if it is a token then append otherwise an error
            if str in textTokens:
                token = Token(str, textTokens.get(str))
                self.tokens.append(token)
            else:
                self.error = True
                print("Wrong method call! Check line: ", self.line)
            # set current to new position
            self.current = position

            # loop until we find the other backslash
            while self.text[position] != "\\":
                position += 1
            # store the text in between the slashes
            str = self.text[self.current:position]
            token = Token(str, "TEXT")
            self.tokens.append(token)

            # store the last backslash
            token = Token(self.text[position], "BACK_SLASH")
            self.tokens.append(token)
            # set current to the new position
            self.current = position
            self.increaseCurrent()
        else:
            # simple other tokens
            token = Token(punctuation, singleTokens.get(punctuation))
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
            else:
                break
        operation = self.text[self.current:position]

        if not self.error:
            if operation in operationTokens:
                token = Token(operation, operationTokens.get(operation))
                self.tokens.append(token)
            else:
                print("Operation Error! Check line here: ", self.line)
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
            else:
                break
        # create keyword string by cutting text from current to position
        s = self.text[self.current:position]
        # if the string is a keyword
        if s in keywordTokens:
            token = Token(s, keywordTokens.get(s))
            self.tokens.append(token)
        elif s in textTokens:
            token = Token(s, textTokens.get(s))
            self.tokens.append(token)
        # if the string is not a keyword it's an identifier
        else:
            token = Token(s, "IDENTIFIER")
            self.tokens.append(token)

        # set current to the new position
        self.current = position

    # we loop until we have either digits or a '.' char and create a number based off that
    def setDigitTokens(self):
        position = self.current
        dot_counter = 0  # keeping track of dots to avoid syntax error like "1.2.3" is not a number
        while position != self.length:
            current_char = self.text[position]
            # check if current char isn't a digit or a dot then break
            if not current_char.isdigit() and current_char not in delimeters:
                # if current char is a letter then error like "1a.2" or "1a"
                if current_char.isalpha():
                    self.error = True
                break

            # increment dot counter
            if current_char in delimeters:
                dot_counter += 1
            position += 1

        number = self.text[self.current:position]

        # if we have no dots in the number string then it's an integer
        # if we have 1 dot it'll be a double
        # otherwise it'll be a syntax error
        if not self.error:
            if dot_counter == 0:
                token = Token(number, "INT")
                self.tokens.append(token)
            elif dot_counter == 1:
                # check for money format
                if self.is_money(number):
                    token = Token(number, "MONEY")
                    self.tokens.append(token)
                else:
                    token = Token(number, "DOUBLE")
                    self.tokens.append(token)
            elif dot_counter == 2:
                # check for date format
                self.is_date(number)
            else:
                print("Syntax Error! Wrong number format! Check line: ", self.line)
        else:
            print("Syntax Error! Wrong number format! Check line: ", self.line)

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
        temp = 0;
        for token in self.tokens:
            print("[",token.value, " ", token.type,"]", end=" ")
            temp = temp + 1
            if temp == 4:
                print("")
                temp = 0
            
    def get_tokens(self):
        self.tokens.append(Token("eof", "EOF"))
        return self.tokens