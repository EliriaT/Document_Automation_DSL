import sys
sys.path.append('../')

from PBL.Lexer.Lexer import *



#############-----PARSER-----###################

################################################
#############     NODES     ####################
################################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok.value}:{self.tok.type}'

class VariableNode:
    def __init__(self, tok_name, tok_type):
        self.name = tok_name
        self.type = tok_type

    def __repr__(self):
        return f'({self.name.value} {self.name.type}) : ({self.type.type} {self.type.value})'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
	    self.left_node = left_node
	    self.op_tok = op_tok
	    self.right_node = right_node

    def __repr__(self):
	    return f'({self.left_node}, {self.op_tok.value}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

	def __repr__(self):
		return f'({self.op_tok.value}, {self.node})'



#######################################
# ERRORS
#######################################

errors = { "expectNumber": "Invalid Syntax Error: Expected int or float", "missArithmetic": "Expected '+', '-', '*' or '/'",
"unclosedParen": "Expected ')'", "missId": "Expected Identifier", "missOpenParams": "Expected brackets after keyword params",
"missCloseParams": "Unclosed bracket. Expected ']'", "missColon": "Expected ':' after Identifier", "missType": "Expected datatype in variable declaration",
"noMoreVar":"Params closed succesfully"}



#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.error = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok


    #################----EITHER PARAMS OR ARITHMETIC PARSING--------######################
    def parse(self):
        if self.current_tok.value == "PARAMS":
            res = self.paramsTree()
        else:
            res = self.expr()
            if not self.error and self.current_tok.value != delimeters.get("eof"):
                self.error = "missArithmetic"
        return res, self.error



    #####################-----PARAMS PARSING-----###########################
    def paramsTree(self):
        temp = self.current_tok.value + " " + self.current_tok.type + " "
        self.advance()
        res = temp
        if self.current_tok.value == singleTokens.get("["):
            res = res + str(self.current_tok.type)
            while not (self.error in errors):
                res = res + "\n " + self.paramsLoop().__str__()
            if self.error == "noMoreVar":
                self.error = None
        else:
            self.error = "missOpenParams"
        return res
        
    def paramsLoop(self):
        self.advance()
        newComb = ""
        if self.current_tok.value == "IDENTIFIER":
            newComb = self.current_tok
            self.advance()
            if self.current_tok.type == ":":
                self.advance()
                if self.current_tok.type in dataType:
                    newComb = VariableNode(newComb, self.current_tok)
                else:
                    newComb = "("+newComb.value.__str__()+" "+newComb.type.__str__()+") "+"("+self.current_tok.value.__str__()+" "+self.current_tok.type.__str__()+")"
                    self.error = "missType"
            else:
                newComb = "("+newComb.value.__str__()+" "+newComb.type.__str__()+") "+"("+self.current_tok.value.__str__()+" "+self.current_tok.type.__str__()+")"
                self.error = "missColon"
        elif self.current_tok.value == singleTokens.get("]"):
            newComb = self.current_tok.type
            self.error = "noMoreVar"
        else:
            self.error = "missCloseParams"
        return newComb



    ######################-------ARITHMETIC PARSING--------###########################
    def factor(self):
        tok = self.current_tok

        if tok.value in (operationTokens.get("+"), operationTokens.get("-")):
            self.advance()
            factor = self.factor()
            if self.error in errors: 
                return factor
            return UnaryOpNode(tok, factor)

        elif tok.value in (keywordTokens.get("int"), keywordTokens.get("double")):
            self.advance()
            return NumberNode(tok)
        
        elif tok.value == singleTokens.get("("):
            self.advance()
            expr = self.expr()
            if self.error in errors:
                return expr
            if self.current_tok.value == singleTokens.get(")"):
                self.advance()
                return expr
            else:
                self.error = "unclosedParen"
                return 

        self.error = "expectNumber"
        return tok.value

    def term(self):
        return self.bin_op(self.factor, (operationTokens.get("*"), operationTokens.get("/")))

    def expr(self):
        return self.bin_op(self.term, (operationTokens.get("+"), operationTokens.get("-")))

    def bin_op(self, func, ops):
        left = func()
        if self.error in errors: 
            return left

        while self.current_tok.value in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            if self.error in errors: 
                return left, op_tok.value
            left = BinOpNode(left, op_tok, right)
        
        return left 




################################################
#############     MAIN     #####################
################################################
lex = Lexer("")

filename='./Parser/parsing_example.txt'

with open(
        filename) as openfileobject:
    for line in openfileobject:
        lex.tokenizer(line)
lex.get_tokens()
lex.print_tokens()

parser = Parser(lex.get_tokens())
print("\n")
ast, error = parser.parse()
print(ast)
if error in errors:
    print(errors.get(error))