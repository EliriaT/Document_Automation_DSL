
import sys
from tokenize import Token

sys.path.append('../')

from PBL.Lexer.Lexer import *
from PBL.Token_Types_Enum import TokenType
from PBL.Errors import ParserError,ErrorCode


#############-----PARSER-----###################

################################################
#############     NODES     ####################
################################################

class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Literal(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Text_Literal(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST): 
    """Represents a list of statements"""
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self, templates, actions):
        self.templates = templates
        self.actions = actions


class Actions(AST):
    def __init__(self, block_node):
        # self.formal_params = formal_params  # a list of Param nodes
        self.block_node = block_node   #simple block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations                    #declaration inside actions:
        self.compound_statement = compound_statement        #statements inside actions:


class Template_Block(AST):
    def __init__(self,  compound_statement):
        self.compound_statement = compound_statement        #statements inside template:


class VarDecl(AST):         #Has a var node and a type node
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):        #Has the token and token value- num/date
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Type_text(AST):        #Has the token and token value- num/date
    def __init__(self, token, num,type):
        self.token = token
        self.value = token.value    
        self.num = num
        self.type=type    


#Params declared at template declaration
class Param(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class TemplateDecl(AST):
    def __init__(self, templ_name, formal_params, block_node):
        self.templ_name = templ_name
        self.formal_params = formal_params  # a list of Param nodes
        self.template_block = block_node   #simple block


class TemplateCall(AST):
    def __init__(self, templ_name, actual_params, token):
        self.templ_name = templ_name
        self.actual_params = actual_params  # a list of AST nodes, used by the interpreter
        self.token = token
        # a reference to template declaration symbol
        self.templ_symbol = None


class IfNode(AST):
    def __init__(self, boolean_expression, statements):
        self.expression = boolean_expression
        self.statements = statements


class IfElseNode(AST):
    def __init__(self, boolean_expression, statements, else_statements):
        self.expression = boolean_expression
        self.statements = statements
        self.else_statements = else_statements


class UntilNode(AST):
    def __init__(self, boolean_expression, statements):
        self.expression = boolean_expression
        self.statements = statements


class DoUntilNode(AST):
    def __init__(self, statements, boolean_expression):
        self.statements = statements
        self.expression = boolean_expression


class ExprNode(AST):
    def __init__(self, left, expression, right):
        self.left = left
        self.expression = expression   #In the case of not it is an expression, otherwise and operation :and not >
        self.right = right

class FormattingTextLiteral(AST):
    def __init__(self, formatting=None, text=None):
        self.formatting = formatting  #Just a token with its value or it can be a number token
        self.text = text   #Text is a text literal token

class FunctionCall(AST):  #For built in functions
    def __init__(self, func_name, actual_params):
        self.func_name = func_name
        self.actual_params = actual_params  # a list of AST nodes, used by the interpreter



################################################
#########    Construct the AST     #############
################################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

    def get_next_token(self):
        return self.tokens.pop(0)

    #Function to see the next token in the stream
    def peek(self):
        if(len(self.tokens)>0): return self.tokens[0] 
        else: return None

    def error(self, error_code, token,expected_token):
        raise ParserError( error_code=error_code,token=token, message=f'{error_code.value} -> {token}; Expected:{expected_token}')

    def eat(self, token_type):
        # It compares the current token type with the passed token
        # type and if they match the current token is "eaten" 
        # and assigned the next token to the self.current_token,
        # otherwise  an exception is raised.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token=token_type)

    def main_program(self):
        templates=self.template_decl()
        actions=self.actions_decl()
        program_node=Program(templates,actions)
        return program_node

    def template_decl(self):
        self.eat(TokenType.CREATE)
        self.eat(TokenType.TEMPLATE)
        var_node = self.variable()
        template_name=var_node.value
        self.eat(TokenType.COLON)
        declaration_nodes = self.declarations()  #The formal parameters of a template
        block_node = self.template_block()
        self.eat(TokenType.END)
        self.eat(TokenType.TEMPLATE)
        template_node=TemplateDecl(template_name,declaration_nodes,block_node)

        return template_node

    def actions_decl(self):
        self.eat(TokenType.ACTIONS)
        self.eat(TokenType.COLON)
        block_node = self.action_block()
        action_node=Actions(block_node)
        return action_node

    def template_block(self):
        compound_statement_node = self.compound_statement()
        node = Template_Block( compound_statement_node)
        return node

    def action_block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        """
        declarations : (PARAMS [(variable_declaration SEMI)+) ]
        """
        declarations = []

        if self.current_token.type == TokenType.PARAMS:
            self.eat(TokenType.PARAMS)
            self.eat(TokenType.LBRACKET)
            while self.current_token.type == TokenType.IDENTIFIER:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                # self.eat(TokenType.SEMI)
            self.eat(TokenType.RBRACKET)

        return declarations

    def variable_declaration(self):
        """variable_declaration : IDENTIFIER (COMMA IDENTIFIER)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]  # first Identifier
        self.eat(TokenType.IDENTIFIER)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):
        # type_spec : NUM| MONEY|DATE ETC

        token = self.current_token
        if self.current_token.type == TokenType.NUM:
            self.eat(TokenType.NUM)
        elif self.current_token.type == TokenType.TEXT_VAR:
            self.eat(TokenType.TEXT_VAR)
            if self.current_token.type == TokenType.LBRACKET:
                self.eat(TokenType.LBRACKET)
                num=self.factor()
                type=None
                if(self.current_token.type == TokenType.WORDS):
                    self.eat(TokenType.WORDS)
                    self.eat(TokenType.RBRACKET)
                    type= TokenType.WORDS
                elif(self.current_token.type == TokenType.SENTENCES):
                    self.eat(TokenType.SENTENCES)
                    self.eat(TokenType.RBRACKET)
                    type= TokenType.SENTENCES
                elif(self.current_token.type == TokenType.CHARS):
                    self.eat(TokenType.CHARS)
                    self.eat(TokenType.RBRACKET)
                    type= TokenType.CHARS
                else: self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token=TokenType.CHARS)
                node = Type_text(token,num,type)
                return node

        elif self.current_token.type == TokenType.DATE:
            self.eat(TokenType.DATE)
        elif self.current_token.type == TokenType.MONEY:
            self.eat(TokenType.MONEY)
        elif self.current_token.type == TokenType.BOOLEAN_VAR:
            self.eat(TokenType.BOOLEAN_VAR)
        elif self.current_token.type == TokenType.PHONENUM:
            self.eat(TokenType.PHONENUM)
        else: self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token="Type Token")
        node = Type(token)  #can be a text type only without num and type
        return node

    def compound_statement(self):
        """
        compound_statement:  statement_list 
        """
 
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement
                        | statement SEMICOLON statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
            results.append(self.statement())

        return results

    def statement(self):
        """
        statement :| template_call
                  | assignment_statement
                  |if else
                  |until
                  |do until
                  | print();
                  | pdf()
                  | input()
                  | empty
        """
   
        next_token=self.peek()
        if self.current_token.type == TokenType.IDENTIFIER and next_token.type ==TokenType.LPAREN:
            node = self.template_call_statement()
        elif self.current_token.type == TokenType.IDENTIFIER:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        elif (self.current_token.type == TokenType.UNTIL) or (self.current_token.type == TokenType.DO):
            node = self.until_statement()
        elif self.current_token.type == TokenType.PRINT:
            node = self.print_statement()
        else:
            node = self.empty()
        return node

    def print_statement(self):
        self.eat(TokenType.PRINT)
        actual_params = []
        self.eat(TokenType.LPAREN)

        if self.current_token.type != TokenType.RPAREN:
            node = self.boolean_expressions()
            actual_params.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.boolean_expressions()
            actual_params.append(node)

        self.eat(TokenType.RPAREN)

        node = FunctionCall(
            func_name=TokenType.PRINT.value,
            actual_params=actual_params,
        )
        return node

    def template_call_statement(self):
        token = self.current_token

        template_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        actual_params = []
        if self.current_token.type != TokenType.RPAREN:
            node = self.boolean_expressions()
            actual_params.append(node)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node = self.boolean_expressions()
            actual_params.append(node)

        self.eat(TokenType.RPAREN)

        node = TemplateCall(
            templ_name=template_name,
            actual_params=actual_params,
            token=token,
        )
        return node

    def if_statement(self):
        self.eat(TokenType.IF)

        boolean_expression = self.boolean_expressions()

        statements = self.function_statements()

        
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            else_statements = self.function_statements()
            return IfElseNode(boolean_expression, statements, else_statements)
        else:
            return IfNode(boolean_expression, statements)

    def until_statement(self):
        if self.current_token.type == TokenType.UNTIL:
            self.eat(TokenType.UNTIL)
            boolean_expression = self.boolean_expressions()

            statements = self.function_statements()
            return UntilNode(boolean_expression, statements)
        else:
            self.eat(TokenType.DO)
            statements = self.function_statements()
            self.eat(TokenType.UNTIL)
            boolean_expression = self.boolean_expressions()
            return DoUntilNode(statements, boolean_expression)

    def boolean_expressions(self):
        """
        boolean_expressions : comp_expression ((AND|OR) comp_expression)*
        """
        node = self.comp_expression()
        while (self.current_token.type == TokenType.AND) or (self.current_token.type == TokenType.OR):
            sign = self.current_token
            self.eat(sign.type)
            second_expr=self.comp_expression()
            node = ExprNode(node, sign, second_expr)

        return node
        
    def comp_expression(self):
        #comp_expression: NOT comp_expression
        #                 expr com expr
        if self.current_token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            expression_one=self.comp_expression()
            return ExprNode(TokenType.NOT, expression_one, None)

        expression_one=self.expr()

        while self.current_token.type in [TokenType.SMALLER,TokenType.BIGGER,TokenType.NEGATION_EQUAL,TokenType.EQUAL_EQUAL,TokenType.BIGGER_EQUAL,TokenType.SMALLER_EQUAL]:
            op=(self.current_token)
            self.eat(self.current_token.type)
            expression_Two=self.expr()
            return ExprNode(expression_one, op, expression_Two)
        return expression_one

    def function_statements(self):
        # function_statements: { statement_list } | statement
        if self.current_token.type == TokenType.LBRACE:
            self.eat(TokenType.LBRACE)
            statements = self.statement_list()
            self.eat(TokenType.RBRACE)
        else:
            statements=self.statement()
            if self.current_token.type != TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
            if self.peek().type == TokenType.ELSE or self.peek().type == TokenType.UNTIL:
                self.eat(TokenType.SEMICOLON)

        return statements

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.EQUAL)
        

        if self.current_token.type == TokenType.LBRACE:
            self.eat(TokenType.LBRACE)
            right = self.string_parsing()
            self.eat(TokenType.RBRACE)

        else: 
            right = self.boolean_expressions()

        node = Assign(left, token, right)
        return node

    def string_parsing(self):
        textList = []

        while self.current_token.type == TokenType.BACK_SLASH or  self.current_token.type == TokenType.TEXT_LITERALS:
            
            if self.current_token.type == TokenType.TEXT_LITERALS:
                    text = self.pop_text_literals()
                    right = FormattingTextLiteral(None, text)
                    textList.append(right)
            
            else :
                self.eat(TokenType.BACK_SLASH)

                if self.current_token.type == TokenType.TEXT_LITERALS:
                    text = self.pop_text_literals()
                    right = FormattingTextLiteral(None, text)

          
                elif self.current_token.type ==  TokenType.NUM_LITERAL or self.current_token.value.lower() in textTokens or self.current_token.value.lower() in colorTokens:  #trebuie eat italic underline? nu numaidecat
                    formatting = self.current_token
                    self.current_token = self.get_next_token()

                    if formatting.type in [TokenType.SPACE , TokenType.LINE , TokenType.TAB, TokenType.PAGE,TokenType.COURIER,TokenType.ARIAL,TokenType.HELVETICA,TokenType.TIMES,TokenType.RESETFONT,TokenType.RESETSIZE]:
                        right= FormattingTextLiteral(formatting, None)
                        textList.append(right) 
                        continue

                    if formatting.type == TokenType.NUM_LITERAL:
                        right= FormattingTextLiteral(formatting, None)
                        textList.append(right) 
                        continue
                    
                    text = self.pop_text_literals()
                    right = FormattingTextLiteral(formatting, text)
                else:
                    self.error( error_code=ErrorCode.UNEXPECTED_TOKEN,   token=self.current_token, expected_token="textToken")
                
                self.eat(TokenType.BACK_SLASH)
                textList.append(right)   

        return textList

    def pop_text_literals(self):
        right = self.current_token
        self.eat(TokenType.TEXT_LITERALS)

        while self.current_token.type == TokenType.TEXT_LITERALS:
            right.value += self.current_token.value
            self.eat(TokenType.TEXT_LITERALS)

        return Text_Literal(right)

    def variable(self):
        """
        variable : Identifier
        """
        node = Var(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                # if node.type == TokenType.TEXT_LITERALS:
                #     self.eat(TokenType.PLUS)
                # else:
                #     self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MULT | DIV | INT_DIV) factor)*"""
        node = self.factor()

        # if node.token.type == TokenType.TEXT_LITERALS:
        #     return node

        while self.current_token.type in (
                TokenType.MULT,
                TokenType.INTEGER_DIV,
                TokenType.FLOAT_DIV,
        ):
            token = self.current_token
            if token.type == TokenType.MULT:
                self.eat(TokenType.MULT)
            elif token.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif token.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | power
        
        """
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        else:
            node = self.power()
            return node
        

    def power(self):
        #Power : atom (POW factor)*
        node = self.atom()
        token = self.current_token
        if token.type == TokenType.POWER:
            self.eat(TokenType.POWER)
            node = BinOp(left = node, op=token, right = self.factor())
        return node


    def atom(self):
        #atom: | LPAREN boolean_expressions RPAREN
        #      | variable
        #      |date literal | bool literal | string literal | num literal
        token = self.current_token
        if token.type == TokenType.NUM_LITERAL:
            self.eat(TokenType.NUM_LITERAL)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.boolean_expressions()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.DATE_LIT:
            self.eat(TokenType.DATE_LIT)
            return Literal(token)
        elif token.type == TokenType.BOOL_LIT:
            self.eat(TokenType.BOOL_LIT)
            return Literal(token)
        elif token.type == TokenType.TEXT_LITERALS:
            self.eat(TokenType.TEXT_LITERALS)
            return Text_Literal(token)
        else:
            node = self.variable()
            return node

    def parse(self):
    
        node = self.main_program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
                expected_token=TokenType.EOF
            )

        return node