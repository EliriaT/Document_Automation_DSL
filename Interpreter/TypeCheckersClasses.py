import sys
sys.path.append('../')
from Document_Automation_DSL.Errors import OperationTypeError,ErrorCode
from datetime import timedelta

class Literals:

    def add(self, literal):
        return self.illegal_operation(literal)

    def substract(self, literal):
        return self.illegal_operation(literal)

    def multiply(self, literal):
        return  self.illegal_operation(literal)

    def divide(self, literal):
        return self.illegal_operation(literal)

    def int_divide(self, literal):
        return self.illegal_operation(literal)

    def power(self, literal):
        return self.illegal_operation(literal)

    def compare_lt(self, literal):
        return self.illegal_operation(literal)

    def compare_gt(self, literal):
        return self.illegal_operation(literal)

    def compare_lte(self, literal):
        return self.illegal_operation(literal)

    def compare_gte(self, literal):
        return self.illegal_operation(literal)

    def and_with(self, literal):
        return self.illegal_operation(literal)

    def or_with(self, literal):
        return self.illegal_operation(literal)

    def not_with(self, literal):
        return self.illegal_operation(literal)

    def illegal_operation(self, literal=None):
        if not literal: literal = self
        raise OperationTypeError(
                error_code=ErrorCode.WRONG_TYPE,
                token=literal,
                message=f'{ErrorCode.WRONG_TYPE.value} -> {self.__class__.__name__} && {literal.__class__.__name__}',
            )


class Numbers(Literals):
    def __init__(self, value):
        self.value = value

    def add(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value + literal.value)
        else:
            return self.illegal_operation(literal)

    def substract(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value - literal.value)
        else:
            return self.illegal_operation(literal)

    def multiply(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value * literal.value)
        else:
            return self.illegal_operation(literal)

    def divide(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value / literal.value)
        else:
            return self.illegal_operation(literal)

    def int_divide(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value // literal.value)
        else:
            return self.illegal_operation(literal)

    def power(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value ** literal.value)
        else:
            return self.illegal_operation(literal)

    def compare_lt(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value < literal.value)
        else:
            return self.illegal_operation(literal)

    def compare_gt(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value > literal.value)
        else:
            return self.illegal_operation(literal)

    def compare_lte(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value <= literal.value)
        else:
            return self.illegal_operation(literal)

    def compare_gte(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value >= literal.value)
        else:
            return self.illegal_operation(literal)

    def compare_eq(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value == literal.value)
        else:
            return self.illegal_operation(literal)

    def compare_neq(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value != literal.value)
        else:
            return self.illegal_operation(literal)

    def and_with(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value and literal.value)
        else:
            return self.illegal_operation(literal)

    def or_with(self, literal):
        if isinstance(literal, Numbers):
            return Numbers(self.value or literal.value)
        else:
            return self.illegal_operation(literal)

    def not_with(self):
        return Numbers(not(self.value))

    def __str__(self):
        return str(self.value)
  
    def __repr__(self):
        return str(self.value)


class Text_Literals(Literals):
    def __init__(self, value):
        self.value = value

    def add(self, literal):
        if isinstance(literal, Text_Literals):
            return Text_Literals(self.value + literal.value)
        elif isinstance(literal, Numbers):
            return Text_Literals(self.value + str(literal.value))
        else:
            return self.illegal_operation(literal)


    def multiply(self, literal):
        if isinstance(literal, Numbers):
            return Text_Literals(self.value * literal.value)
        else:
            return self.illegal_operation(literal)


    def compare_lt(self, literal):
        if isinstance(literal, Text_Literals):
            return Numbers(len(self.value) < len(literal.value))
        else:
            return self.illegal_operation(literal)

    def compare_gt(self, literal):
        if isinstance(literal, Text_Literals):
            return Numbers(len(self.value) > len(literal.value))
        else:
            return self.illegal_operation(literal)

    def compare_lte(self, literal):
        if isinstance(literal, Text_Literals):
            return Numbers(len(self.value) <= len(literal.value))
        else:
            return self.illegal_operation(literal)

    def compare_gte(self, literal):
        if isinstance(literal, Text_Literals):
            return Numbers(len(self.value) >= len(literal.value))
        else:
            return self.illegal_operation(literal)

    def not_with(self):
        return Numbers(not(self.value))

    def __str__(self):
        return str(self.value)
  
    def __repr__(self):
        return str(self.value)

    
class Bools(Numbers):
    def __init__(self, value):
        super().__init__()

class Dates(Literals):   #test
    def add(self, literal):
        if isinstance(literal, Numbers):
            return Dates(self.value  + timedelta(days=literal.value))

        else:
            return self.illegal_operation(literal)

    def substract(self, literal):
        if isinstance(literal, Numbers):
            return Dates(self.value  - timedelta(days=literal.value))

        else:
            return self.illegal_operation(literal)

class Phonenums(Literals):
    def __init__(self, value):
        super().__init__()

class Money_Val(Literals):
    def __init__(self, value):
        super().__init__()



    
    

    

    