import math_funcs as funcs
from operators import Operator


class Calculator:
    ALLOWED_PARENTHESIS = ("(", ")")
    OPERATORS = {"+": Operator("+", 1, funcs.add),
                 "-": Operator("-", 1, funcs.sub),
                 "*": Operator("*", 2, funcs.mul),
                 "/": Operator("/", 2, funcs.div),
                 "~~": Operator("~~", 2.5, funcs.neg, is_unary=True, comes_before=True),  # Unary minus
                 "^": Operator("^", 3, funcs.power),
                 "@": Operator("@", 5, funcs.my_avg),
                 "$": Operator("$", 5, funcs.my_max),
                 "&": Operator("&", 5, funcs.my_min),
                 "%": Operator("%", 4, funcs.modulo),
                 "~": Operator("~", 6, funcs.neg, is_unary=True, comes_before=True),
                 "!": Operator("!", 6, funcs.factorial, is_unary=True, comes_before=False)
                 }

    @staticmethod
    def tokenize(expression: str) -> list:
        """
        Breaks expression into it's components (tokens) - operands and operators.
        Also does some basic validity checks on expression(allowed characters, ~, decimal point)
        :param expression: expression to tokenize
        :return: The list of tokens
        :raises: SyntaxError if expression isn't a valid mathematical expression
        """
        tokenized_lst = []
        in_num = False
        cur_num = ""
        has_tilda = False  # Flag used to check if operand has more than 1 ~
        for char in expression:
            if char == ".":
                if not in_num:
                    cur_num = "0."
                    in_num = True
                elif "." in cur_num:
                    raise SyntaxError("2 '.' in same number")
                else:
                    cur_num += "."

            elif char.isnumeric():
                has_tilda = False
                in_num = True
                cur_num += char

            elif char in Calculator.OPERATORS or char in Calculator.ALLOWED_PARENTHESIS:
                # unary minus if it doesn't come after operand or ")"
                is_unary = False if in_num or (tokenized_lst and tokenized_lst[-1] == ")") else True

                # if 2 ~ for same operand, or ~ immediately after operand or ")" --> syntax error
                if char == "~" and (has_tilda or in_num or (tokenized_lst and tokenized_lst[-1] == ")")):
                    raise SyntaxError("Improper use of operator '~'")

                if char == "~":
                    has_tilda = True

                # if it is unary minus, change char
                if is_unary and char == '-':
                    char = "~~"

                # if we were in number, append it to tokenized_lst, and reset cur_num
                if in_num:
                    tokenized_lst.append(float(cur_num))
                    in_num = False
                    cur_num = ""

                # To block expressions like 3(5+2)
                if char == "(":
                    if tokenized_lst and isinstance(tokenized_lst[-1], float):
                        raise SyntaxError("Parenthesis out of place")
                    has_tilda = False

                if char in Calculator.ALLOWED_PARENTHESIS:
                    tokenized_lst.append(char)
                else:
                    tokenized_lst.append(Calculator.OPERATORS[char])  # append Operator object to list
            else:
                raise SyntaxError("Invalid character in input")
        # add last number in string, if there is one
        if in_num:
            tokenized_lst.append(float(cur_num))

        return tokenized_lst


# todo - use operator attributes in tokenize function, calculate expression

def main():
    exp = "13+-3"
    exp = "".join(exp.split())
    try:
        lst = Calculator.tokenize(exp)
        print(lst)
    except SyntaxError as e:
        print(e)


if __name__ == '__main__':
    main()
