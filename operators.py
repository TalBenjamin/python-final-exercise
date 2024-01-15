class Operator:

    def __init__(self, symbol: str, precedence: float, func: callable, is_unary: bool = False,
                 is_pre: bool = False, is_single: bool = False):
        self.symbol = symbol
        self.precedence = precedence
        self.func = func
        self.is_unary = is_unary
        self.is_pre = is_pre
        self.is_single = is_single   # if 2 cant appear in a row (only relevant for unary)

    def call_func(self, op1: float, op2: float = None) -> float:
        """calls and return the result of function of the operator"""
        return self.func(op1) if self.is_unary else self.func(op1, op2)

    def is_pre_unary(self) -> bool:
        """returns true if this operator is pre unary"""
        return self.is_unary and self.is_pre

    def is_post_unary(self) -> bool:
        """returns true if this operator is post unary"""
        return self.is_unary and not self.is_pre

    def can_come_after(self, prev_element) -> bool:
        """
        returns true if this operator can come after prev_element
        :param prev_element: can be either: operand (float), Operator, or string (parenthesis). (None if nothing)
        :return: True if element can come before operator, false otherwise
        """

        if prev_element is None:
            # can only be pre unary operator
            return self.is_unary and self.is_pre

        if isinstance(prev_element, float):
            # can be post unary or binary operator
            return (self.is_unary and not self.is_pre) or not self.is_unary

        if isinstance(prev_element, Operator):
            # if prev is binary or pre unary, this must be pre unary
            if prev_element.is_pre or not prev_element.is_unary:
                return self.is_unary and self.is_pre
            # if prev is post unary, this must be post unary or binary
            if prev_element.is_unary and not prev_element.is_pre:
                return (self.is_unary and not self.is_pre) or not self.is_unary

            return False

        if prev_element == "(":
            # this must be pre unary
            return self.is_unary and self.is_pre
        if prev_element == ")":
            # this must be binary or post unary
            return (not self.is_unary) or (self.is_unary and not self.is_pre)
        return False

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self)
