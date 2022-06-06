from Interpreter.SemanticAnalyzer import SemanticAnalyzer
from PBL.Lexer.Lexer import Lexer
from PBL.Parser.Parser import Parser
from PBL.Interpreter.Interpreter import Interpreter

#Creating the lexer object
lex = Lexer("")
filename='./Parser/version2.txt'
with open(filename) as openfileobject:
    for line in openfileobject:
        lex.gather_lines(line)
#Tokenizing each line
lex.tokenize_lines()
tokens=lex.get_tokens()
lex.print_tokens()

print("\n\n")
#Creating the parser object and generating the AST
parser = Parser(tokens)
AST=parser.parse()

#Analysing semanticaly the AST
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.visit(AST)
print("\n")

#Interpreting the AST
interpreter = Interpreter(AST)
print("#############---PROGRAM OUTPUT---#############")
interpreter.interpret()
interpreter.print_pdf()