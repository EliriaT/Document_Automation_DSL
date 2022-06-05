import sys
from enum import Enum
from TypeCheckersClasses import *
from pdfcreator import PDF
from fpdf import FPDF
sys.path.append('../')

from PBL.Interpreter.SemanticAnalyzer import NodeVisitor,SemanticAnalyzer
from PBL.Token_Types_Enum import TokenType
from PBL.Lexer.Lexer import Lexer
from PBL.Parser.Parser import Parser

###############################################################################
#                                                                             #
#                               INTERPRETER                                   #
#                                                                             #
###############################################################################

#Activation records type for the DSL
class ARType(Enum):
    PROGRAM   = 'PROGRAM'
    TEMPLATE = 'TEMPLATE'
    ACTIONS = 'ACTIONS'


class CallStack:
    def __init__(self):
        self._records = []

    def push(self, ar):
        self._records.append(ar)

    def pop(self):
        return self._records.pop()

    def peek(self):
        return self._records[-1]

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self._records))
        s = f'CALL STACK\n{s}\n\n'
        return s

    def __repr__(self):
        return self.__str__()


class ActivationRecord:
    def __init__(self, name, type, nesting_level):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {}

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members[key]

    def get(self, key):
        return self.members.get(key)

    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type.value,
                name=self.name,
            )
        ]
        for name, val in self.members.items():
            lines.append(f'   {name:<20}: {val}')

        s = '\n'.join(lines)
        return s

    def __repr__(self):
        return self.__str__()


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = CallStack()
        self.pdf = PDF('P', 'mm', 'Letter')
        self.pdf.add_page()

    def log(self, msg):
        if _SHOULD_LOG_STACK:
            print(msg)

    def visit_Program(self, node):
        
        program_name = "GLOBAL"
        self.log(f'ENTER: PROGRAM {program_name}')

        ar = ActivationRecord(
            name=program_name,
            type=ARType.PROGRAM,
            nesting_level=1,
        )
        self.call_stack.push(ar)

        self.log(str(self.call_stack))

        # visit subtrees                #In interpreter the templates in ast are not visited, only actions.
        # self.visit(node.templates)    #The body of the template was already referenced in the Templ call node

        self.visit(node.actions)

        self.log(f'LEAVE: PROGRAM {program_name}')
        self.log(str(self.call_stack))

        self.call_stack.pop()

    def visit_Actions(self,node):
        self.visit(node.block_node)

    def visit_Template_Block(self,node):
        self.visit(node.compound_statement)

    def visit_Block(self, node): #The block of the actions
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        # Do nothing
        pass

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_Type_text(self, node):
        # Do nothing
        pass

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op.type == TokenType.PLUS:
            return left.add(right) 
        elif node.op.type == TokenType.MINUS:
            return left.substract(right)
        elif node.op.type == TokenType.MULT:
            return left.multiply(right)
        elif node.op.type == TokenType.INTEGER_DIV:
            return left.int_divide(right)
        elif node.op.type == TokenType.FLOAT_DIV:
            return left.divide(right)
        elif node.op.type == TokenType.POWER:
            return left.power(right)


    def visit_Num(self, node):
        return Numbers(node.value)

    def visit_Literal(self,node):
        if node.type == TokenType.BOOL_LIT:
            return Bools(node.value)
        elif node.type == TokenType.DATE_LIT:
            return Dates(node.value)
        elif node.type == TokenType.PHONENUM:
            return Phonenums(node.value)

    def visit_Text_Literal(self,node):
        text=node.value
        word_list=[ t for t in text.split() if t.startswith('#') ]
        end='.,!?)(*@`></'
        for word in word_list:              #Getting the list of params in the text
            m=word_list.index(word)
            if word[-1] in end:
                word_list[m]=word[0:len(word)-1]
            word_list[m]=word_list[m][1:len(word)]

        ar = self.call_stack.peek()
        

        for word in word_list:
            var_value = ar.get(word)
            text=text.replace("#"+word,str(var_value.value))
        node.value=text
        return Text_Literals(text)

    def visit_FormattingTextLiteral(self,node):
        if node.formatting == None :
            text_literal=self.visit(node.text)
            self.pdf.text("", text_literal.value)
            return text_literal.value
        elif node.formatting != None  and node.text == None:
            return node.formatting.value
        elif node.formatting != None  and node.text != None:
            text_literal=self.visit(node.text)
            self.pdf.text(node.formatting.value, text_literal.value)
            return node.formatting.value + text_literal.value #Visit

    def visit_list(self,node):  #A list of formmatting text literals ... {}
        text=''
        for i in node:
            text+=self.visit(i)

        return text

    def visit_UnaryOp(self, node):
        op = node.op.type
        number=self.visit(node.expr)
        if op == TokenType.PLUS:
            return number.multiply(Numbers(1))
        elif op == TokenType.MINUS:
            return number.multiply(Numbers(-1))

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)

        ar = self.call_stack.peek()
        ar[var_name] = var_value

    def visit_Var(self, node):
        var_name = node.value

        ar = self.call_stack.peek()
        var_value = ar.get(var_name)

        return var_value

    def visit_NoOp(self, node):
        pass

    def visit_TemplateDecl(self, node):
        pass

    def visit_TemplateCall(self, node):
        templ_name = node.templ_name
        templ_symbol = node.templ_symbol

        ar = ActivationRecord(
            name=templ_name,
            type=ARType.TEMPLATE,
            nesting_level=templ_symbol.scope_level + 1,
        )

        formal_params = templ_symbol.formal_params
        actual_params = node.actual_params
        
        for param_symbol, argument_node in zip(formal_params, actual_params):
            ar[param_symbol.name] = self.visit(argument_node)

        if len(formal_params) > len(actual_params):                 #If there are more actual params, the excess is just ignored
            print("You introduced not enough parameters for template %s, please provide info for: \n" %templ_name)
            for i in range(len(actual_params),len(formal_params)):
                print(formal_params[i].name+":  ",end=" ")
                ar[formal_params[i].name] = input()                  #Sa transform in data type necesar

        self.call_stack.push(ar)

        self.log(f'\n\nENTER: TEMPLATE {templ_name}')
        self.log(str(self.call_stack))

        # evaluate procedure body
        self.visit(templ_symbol.block_ast)

        self.log(f'\n\nLEAVE: TEMPLATE {templ_name}')
        self.log(str(self.call_stack))

        self.call_stack.pop()

    def visit_FunctionCall(self,node):
        if node.func_name==TokenType.PRINT.value:
            for arg in node.actual_params:
                elem=self.visit(arg)
                print(elem,end=" ")
            print()

    def visit_IfNode(self,node):
        bool_result=self.visit(node.expression)
        if(bool_result.value):
            for child in node.statements:
                self.visit(child)

    def visit_IfElseNode(self,node):
        bool_result=self.visit(node.expression)
        if(bool_result.value):
            for child in node.statements:
                self.visit(child)
        else:
            for child in node.else_statements:
                self.visit(child)

    def visit_UntilNode(self,node):
        bool_result=self.visit(node.expression)
        while(bool_result.value):
            for child in node.statements:
                self.visit(child)
            bool_result=self.visit(node.expression)

    def visit_DoUntilNode(self,node):
        while(True):
            for child in node.statements:
                self.visit(child)
            bool_result=self.visit(node.expression)
            if not(bool_result.value): break

    def visit_ExprNode(self,node):
        left_side=None
        right_side=None
        if node.left.token.type!=TokenType.NOT:left_side= self.visit(node.left)
        else: 
            bool_result=self.visit(node.expression)
            return bool_result.not_with

        right_side=self.visit(node.right)

        operation_type=node.expression.type

        if operation_type == TokenType.SMALLER:
            return left_side.compare_lt(right_side)
        elif operation_type == TokenType.BIGGER:
            return left_side.compare_gt(right_side)
        elif operation_type == TokenType.NEGATION_EQUAL:
            return left_side.compare_neq(right_side)
        elif operation_type == TokenType.EQUAL_EQUAL:
            return left_side.compare_eq(right_side)
        elif operation_type == TokenType.BIGGER_EQUAL:
            return left_side.compare_gte(right_side)
        elif operation_type == TokenType.SMALLER_EQUAL:
            return left_side.compare_lte(right_side)

        elif operation_type == TokenType.AND:
            return left_side.and_with(right_side)
        elif operation_type == TokenType.OR:
            return left_side.or_with(right_side)


    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)

    def print_pdf(self):
        self.pdf.print("test2")



lex = Lexer("")

filename='./Parser/version2.txt'
with open(filename) as openfileobject:
    for line in openfileobject:
        lex.tokenizer(line)
        # print("linie "+line)/
tokens=lex.get_tokens()
lex.print_tokens()
print("\n\n")
parser = Parser(tokens)
AST=parser.parse()


_SHOULD_LOG_STACK = True

semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.visit(AST)
print("\n")

interpreter = Interpreter(AST)
# interpreter.__init__(AST)
interpreter.interpret()
interpreter.print_pdf()