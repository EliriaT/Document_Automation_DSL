import sys

sys.path.append('../')

from PBL.Errors import SemanticError,ErrorCode
from PBL.Lexer.Lexer import Lexer
from PBL.Parser.Parser import Parser

###############################################################################
#                                                                             #
#                               AST visitors                                  #
#                                                                             #
###############################################################################
# implements the Visitor pattern:
class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


# ##############################################################################
#                                                                              #
#                SYMBOLS and SYMBOL TABLE and SEMANTIC ANALYSIS                #
#                                                                              #
# ##############################################################################

class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
        self.scope_level = 0


class Var_Symbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )

    __repr__ = __str__


class Built_in_Type_Symbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )


class Template_Symbol(Symbol):
    def __init__(self, name, formal_params=None):
        super().__init__(name)
        # a list of VarSymbol objects
        self.formal_params = [] if formal_params is None else formal_params
        # a reference to procedure's body (AST sub-tree) used by the interpreter
        self.block_ast = None

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.formal_params,
        )

    __repr__ = __str__


class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def _init_builtins(self):
        self.insert(Built_in_Type_Symbol('NUM'))
        self.insert(Built_in_Type_Symbol('TEXT'))
        self.insert(Built_in_Type_Symbol('DATE'))
        self.insert(Built_in_Type_Symbol('MONEY'))
        self.insert(Built_in_Type_Symbol('BOOL'))
        self.insert(Built_in_Type_Symbol('PHONENUM'))

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
            self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            lines.append(f'{header_name:<15}: {header_value}')
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            f'{key:>7}: {value}'
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(msg)

    def insert(self, symbol):
        self.log(f'Insert: {symbol.name}')
        symbol.scope_level = self.scope_level
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        self.log(f'Lookup: {name}. (Scope name: {self.scope_name})')
        # 'symbol' is either an instance of the Symbol class or None
        symbol = self._symbols.get(name)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(msg)

    def error(self, error_code, token):
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        
        self.log('ENTER scope: global')
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope,  # None
        )
        global_scope._init_builtins()
        self.current_scope = global_scope

        # visit subtrees
        self.visit(node.templates)

        self.visit(node.actions)

        self.log(global_scope)

        self.current_scope = self.current_scope.enclosing_scope
        self.log('LEAVE scope: global')



    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_TemplateDecl(self, node):
        templ_name = node.templ_name
        template_symbol = Template_Symbol(templ_name)
        self.current_scope.insert(template_symbol)

        self.log(f'ENTER scope: {templ_name}')
        # Scope for parameters and local variables
        template_scope = ScopedSymbolTable(
            scope_name=templ_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = template_scope

        # Insert parameters into the procedure scope
        for param in node.formal_params:
            param_type = self.current_scope.lookup(param.type_node.value)
            # print("Este ",param_type)
            param_name = param.var_node.value
            var_symbol = Var_Symbol(param_name, param_type)

            if self.current_scope.lookup(param_name, current_scope_only=True):
                self.error(
                    error_code=ErrorCode.DUPLICATE_ID,
                    token=param.var_node.token,
                )

            self.current_scope.insert(var_symbol)
            template_symbol.formal_params.append(var_symbol)

        self.visit(node.template_block)

        self.log(template_scope)

        self.current_scope = self.current_scope.enclosing_scope
        self.log(f'LEAVE scope: {templ_name}\n')

        # accessed by the interpreter when executing procedure call
        template_symbol.block_ast = node.template_block

    def visit_Template_Block(self,node):
        self.visit(node.compound_statement)

    def visit_Actions(self,node):
        self.visit(node.block_node)


    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)
        # print("Este ",type_symbol)

        # Create the symbol and insert it into the symbol table.
        var_name = node.var_node.value
        var_symbol = Var_Symbol(var_name, type_symbol)

        # It is an error if the table(current scope) already has a symbol with the same name
        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(
                error_code=ErrorCode.DUPLICATE_ID,
                token=node.var_node.token,
            )

        self.current_scope.insert(var_symbol)

    def visit_Assign(self, node):
        # right-hand side
        self.visit(node.right)
        # left-hand side
        self.visit(node.left)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.token)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        pass

    def visit_TemplateCall(self, node):
        for param_node in node.actual_params:
            self.visit(param_node)

        template_symbol = self.current_scope.lookup(node.templ_name)
        # accessed by the interpreter when executing template call
        node.templ_symbol = template_symbol

    


lex = Lexer("")

filename='./Parser/parsing_example.txt'

with open(filename) as openfileobject:
    for line in openfileobject:
        lex.tokenizer(line)
        # print("linie "+line)
tokens=lex.get_tokens()
lex.print_tokens()
print("\n\n")
parser = Parser(tokens)
AST=parser.parse()

_SHOULD_LOG_SCOPE = True

semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.visit(AST)