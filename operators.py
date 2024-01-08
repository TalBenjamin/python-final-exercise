class Operator:

    def __init__(self, symbol: str, precedence: float, func: callable, is_unary: bool = False,
                 comes_before: bool = False):
        self.symbol = symbol
        self.precedence = precedence
        self.func = func
        self.is_unary = is_unary
        self.comes_before = comes_before

    def call_func(self, op1: float, op2: float = None) -> float:
        return self.func(op1) if self.is_unary else self.func(op1, op2)

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self)
