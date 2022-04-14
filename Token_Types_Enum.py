from enum import Enum
class TokenType(Enum):
    # single-character token types
    DOT         =           "."
    COMMA       =          ","
    SEMICOLON   =    ";"       
    COLON       =         ":"       
    HASHTAG     =     "#"       
    LBRACE      =         "{"           
    RBRACE      =      "}"      
    LPAREN      =      "("     
    RPAREN      =      ")"     
    LBRACKET    =      "["     
    RBRACKET    =       "]"    
    FLOAT_DIV       =          "/"      
    BACK_SLASH  =     "\\"     
    DOUBLE_QUOTE=      "\""    
    SINGLE_QUOTE=      "\'"  
    #Delimiters
    VERTICAL_BAR    = "|"
    UNDERSCORE      = "_"
    #Operational Tokens
    SMALLER         =   "<"
    BIGGER          =   ">"
    EQUAL          =    "="
    NEGATION        =    "!"
    NEGATION_EQUAL  =     "!="
    MOD             =     "%"
    EQUAL_EQUAL     =      "=="
    BIGGER_EQUAL    =      ">="
    SMALLER_EQUAL   =      "<="
    MULT            =       "*"
    PLUS            =      "+"
    MINUS           =      "-"

    # block of reserved words
    INT 	=	"INT"       # marks the beginning of the block
    DOUBLE 	=	"DOUBLE"
    NUM     =   "NUM"
    NUM_LITERAL = "NUM_LITERAL"
    INTEGER_DIV   = 'DIV'
    BOOLEAN_VAR 	=	"BOOL"
    CHARS 	=	"CHARS"
    TEXT_VAR 	=	"TEXT"
    TEXT_LITERALS = "TEXT_LITERAL"
    WORDS 	=	"WORDS"
    DATE 	=	"DATE"
    MONEY 	=	"MONEY"
    PHONENUM 	=	"PHONENUM"
    TEMPLATE 	=	"TEMPLATE"
    ACTIONS 	=	"ACTIONS"
    OPEN 	=	"OPEN"
    PARAMS 	=	"PARAMS"
    ENUM 	=	"ENUM"
    PACK 	=	"PACK"
    SENTENCES 	=	"SENTENCES"
    GLOBAL 	=	"GLOBAL"
    CREATE 	=	"CREATE"
    MAKE 	=	"MAKE"
    CONTAINS 	=	"CONTAINS"
    PRINT 	=	"PRINT"
    ERROR 	=	"ERROR"
    INPUT 	=	"INPUT"
    RETURN 	=	"RETURN"
    RIGHT 	=	"RIGHT"
    LEFT 	=	"LEFT"
    MERGE 	=	"MERGE"
    SPLIT 	=	"SPLIT"
    REPLACE 	=	"REPLACE"
    FOR 	=	"FOR"
    UNTIL 	=	"UNTIL"
    DO 	=	"DO"
    IF 	=	"IF"
    ELSE 	=	"ELSE"
    AND 	=	"AND"
    OR 	=	"OR"
    TRUE 	=	"TRUE"
    FALSE 	=	"FALSE"
    NOT 	=	"NOT"
    FONTSIZE 	=	"FONTSIZE"
    FONT 	=	"FONT"
    LENGTH 	=	"LENGTH"
    BEGIN 	=	"BEGIN"
    END 	=	"END"
    DOC 	=	"DOC"
    PDF 	=	"PDF"
    DOCX 	=	"DOCX"
    HTML 	=	"HTML"
    CSV 	=	"CSV"       # marks the end of the block
    #Text tokens
    UNDERLINE 	=	"U"
    ITALIC 	=	"I"
    CENTER 	=	"CENTER"
    BOLD 	=	"B"
    COLOR 	=	"COLOR"
    LINE 	=	"LINE"
    SPACE 	=	"SPACE"
    TAB 	=	"T"
    RED 	=	"RED"
    BLUE 	=	"BLUE"
    GREEN 	=	"GREEN"
    MAGENTA 	=	"MAGENTA"
    WHITE 	=	"WHITE"
    YELLOW 	=	"YELLOW"
    BROWN 	=	"BROWN"
    GREY 	=	"GREY"
    BLACK 	=	"BLACK"
    IDENTIFIER    = 'IDENTIFIER'
    EOF           = 'EOF'

def _build_reserved_keywords():
    """The function relies on the fact that in the TokenType
    enumeration the beginning of the block of reserved keywords is
    marked with INT and the end of the block is marked with
    the CSV keyword.
    Result Format:
        {'INT': <TokenType.INT: 'INT'>}
    """
    # enumerations support iteration, in definition order
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.INT)
    end_index = tt_list.index(TokenType.CSV)
    reserved_keywords = {
        token_type.value: token_type
        for token_type in tt_list[start_index:end_index + 1]
    }
    return reserved_keywords


RESERVED_KEYWORDS = _build_reserved_keywords()
