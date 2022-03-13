###Puntuation tokens
singleTokens = {
    ".": "DOT", ",": "COMMA", ";": "SEMICOLON", ":": "COLON", "#": "HASHTAG",
    "{": "LBRACE", "}": "RBRACE", "(": "LPAREN", ")": "RPAREN", "[": "LBRACKET", "]": "RBRACKET",
    "+": "PLUS", "-": "MINUS", "/": "SLASH", "%": "MOD", "*": "MULT",
    "\"": "DOUBLE_QUOTE", "\'": "SINGLE_QUOTE"
}

###Operation tokens
operationTokens = {
    "<": "SMALLER", ">": "BIGGER", "=": "EQUAL", "!": "NEGATION", "!=": "NEGATION_EQUAL",
    "==": 'EQUAL_EQUAL', ">=": "BIGGER_EQUAL", "<=": "SMALLER_EQUAL",
}

###Keyword tokens
keywordTokens = {
    "int": "INT_VAR", "double": "DOUBLE_VAR", "bool": "BOOLEAN_VAR", "chars": 'CHARS', "text": "TEXT_VAR",
    "words": "WORDS", "date": "DATE", "money": "MONEY", "phonenum": "PHONENUM",
    "template": "TEMPLATE", "actions": "ACTIONS", "open": "OPEN", "params": "PARAMS", "enum": "ENUM",
    "pack": "PACK", "sentences": "SENTENCES", "global": "GLOBAL", "create": "CREATE", "make": "MAKE",
    "contains": "CONTAINS", "print": "PRINT", "error": "ERROR", "input": "INPUT", "return": "RETURN",
    "right": "RIGHT", "left": "LEFT", "merge": "MERGE", "split": "SPLIT", "replace": "REPLACE",
    "for": "FOR", "until": "UNTIL", "do": "DO", "if": "IF", "else": "ELSE",
    "and": "AND", "or": "OR", "true": "TRUE", "false": "FALSE", "not": "NOT",
    "fontsize": "FONTSIZE", "font": "FONT", "begin": "BEGIN", "end": "END",
    "doc": "DOC", "pdf": "PDF", "docx": "DOCX", "html": "HTML", "csv": "CSV"
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
        else:
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
        # if the string is not a keyword it's an identifier
        else:
            token = Token(s, "IDENTIFIER")
            self.tokens.append(token)

        # set current to the new position
        self.current = position

    # we loop until we have either digits or a '.' char and create a number based off that
    def setDigitTokens(self):
        position = self.current
        # keeping track of dots to avoid syntax error like "1.2.3" is not a number
        dot_counter = 0
        while position != self.length:
            current_char = self.text[position]
            if not current_char.isdigit() and current_char != '.':
                # if current char is a letter then error like "1a.2" or "1a"
                if current_char.isalpha():
                    self.error = True
                break

            if current_char == '.':
                dot_counter += 1
            position += 1

        number = self.text[self.current:position]

        # if we have no dots in the number string then it's an integer
        # if we have 1 dot it'll be a double
        # otherwise it'll be a syntax error
        if not self.error:
            if dot_counter == 0:
                token = Token(number, "INT_VAL")
                self.tokens.append(token)
            elif dot_counter == 1:
                token = Token(number, "DOUBLE_VAL")
                self.tokens.append(token)
            else:
                print("Syntax Error! Wrong number format! Check line: ", self.line)
        else:
            print("Syntax Error! Wrong number format! Check line: ", self.line)

        # set current to the new position
        self.current = position

    # print tokens array
    def print_tokens(self):
        for token in self.tokens:
            print(token.value, " ", token.type)


################################################
#############     MAIN     ####################
################################################

lex = Lexer("")
with open(
        "C:\\Users\\vraga\\OneDrive\\Desktop\\UNI\\PBL\\DSL\\Document-Automation-DSL\\program_example.txt") as openfileobject:
    for line in openfileobject:
        print(line)
        lex.tokenizer(line)

lex.print_tokens()
