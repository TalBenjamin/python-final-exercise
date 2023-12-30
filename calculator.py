import math_funcs as funcs

OPERATOR_PRECEDENCE = {"+": [1, funcs.add], "-": [1, funcs.sub], "*": [2, funcs.mul], "/": [2, funcs.div],
                       "~~": [2.5, funcs.neg],  # Unary minus
                       "^": [3, funcs.power], "@": [5, funcs.my_avg], "$": [5, funcs.my_max], "&": [5, funcs.my_min],
                       "%": [4, funcs.modulo], "~": [6, funcs.neg], "!": [6, funcs.factorial]}


def tokenize(expression: str) -> list:
    """
    Breaks expression into it's components (tokens) - operands and operators.
    Also does some basic validity checks on expression(allowed characters, ~, decimal point)
    :param expression: expression to tokenize
    :return: The list of tokens
    :raises: SyntaxError if expression isn't a valid mathematical expression
    """
    tokenized_lst = []
    in_num = False  # Flag used to know if currently in number
    cur_num = ""
    has_tilda = False  # Flag used to check if operand has more than 1 ~
    for char in expression:
        if char == ".":
            if not in_num:
                raise SyntaxError("'.' out of place")
            if "." in cur_num:
                raise SyntaxError("2 '.' in same number")
            cur_num += char

        elif char.isnumeric():
            has_tilda = False
            in_num = True
            cur_num += char

        elif char in OPERATOR_PRECEDENCE or char in ["(", ")"]:
            # unary minus if it doesn't come after operand or ")"
            is_unary = False if in_num or (tokenized_lst and tokenized_lst[-1] == ")") else True

            # if 2 ~ for same operand, or ~ immediately after operand or ")" --> syntax error
            if char == "~" and (has_tilda or in_num or (tokenized_lst and tokenized_lst[-1] == ")")):
                raise SyntaxError("Improper use of operator '~'")

            if char == "~":
                has_tilda = True

            if is_unary and char == '-':
                char = "~~"

            if char == "(":
                has_tilda = False

            # if we were in number, append it to tokenized_lst, and reset cur_num
            if in_num:
                tokenized_lst.append(float(cur_num))
                in_num = False
                cur_num = ""

            tokenized_lst.append(char)
        else:
            raise SyntaxError("Invalid character in input")
    if in_num:
        tokenized_lst.append(float(cur_num))

    return tokenized_lst


def main():
    exp = "23+65.56/234(%11.1"
    exp = "".join(exp.split())
    try:
        lst = tokenize(exp)
        print(lst)
    except SyntaxError as e:
        print(e)


if __name__ == '__main__':
    main()
