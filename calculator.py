import math_funcs as funcs
from operators import Operator


class Calculator:
    ALLOWED_PARENTHESIS = ("(", ")")
    OPERATORS = {"+": Operator("+", 1, funcs.add),
                 "-": Operator("-", 1, funcs.sub),
                 "*": Operator("*", 2, funcs.mul),
                 "/": Operator("/", 2, funcs.div),
                 "~~": Operator("~~", 2.5, funcs.neg, is_unary=True, is_pre=True),  # Unary minus
                 "^": Operator("^", 3, funcs.power),
                 "@": Operator("@", 5, funcs.my_avg),
                 "$": Operator("$", 5, funcs.my_max),
                 "&": Operator("&", 5, funcs.my_min),
                 "%": Operator("%", 4, funcs.modulo),
                 "~": Operator("~", 6, funcs.neg, is_unary=True, is_pre=True),
                 "!": Operator("!", 6, funcs.factorial, is_unary=True, is_pre=False),
                 "#": Operator("#", 6, funcs.hashtag, is_unary=True, is_pre=False)
                 }

    @staticmethod
    def tokenize(expression: str) -> list:
        """
        Breaks expression into it's components (tokens) - operands and operators.
        Also does some basic validity checks on expression(allowed characters, ~, decimal point,
        if operator position makes sense).
        :param expression: expression to tokenize
        :return: The list of tokens
        :raises SyntaxError if expression isn't a valid mathematical expression
        """
        tokenized_lst = []
        in_num = False
        cur_num = ""
        last_single = ""  # used to check operators that cant appear more than once
        for char in expression:

            if char == ".":  # take care of decimal point
                last_single = ""  # nullify this flag
                if not in_num:
                    cur_num = "0."
                    in_num = True
                elif "." in cur_num:
                    raise SyntaxError("2 '.' in same number")
                else:
                    cur_num += "."

            # append digit to cur_num
            elif char.isnumeric():
                last_single = ""  # nullify this flag
                in_num = True
                cur_num += char

            elif char in Calculator.OPERATORS or char in Calculator.ALLOWED_PARENTHESIS:  # operator or parenthesis
                # if opening parenthesis, disable tilda flag and check if it comes after operand
                if char == "(":
                    if in_num:
                        raise SyntaxError("Invalid use of parenthesis")
                    last_single = ""  # nullify this flag

                # if was in number, append to list before continuing
                if in_num:
                    # check if operand is in ok position
                    if not Calculator.check_position(tokenized_lst, float(cur_num)):
                        raise SyntaxError("Operand out of place")
                    tokenized_lst.append(float(cur_num))
                    last_single = ""  # nullify this flag
                    cur_num = ""
                    in_num = False

                # if parenthesis, append to list and move to next char
                if char in Calculator.ALLOWED_PARENTHESIS:
                    if char == ")" and tokenized_lst and tokenized_lst[-1] == "(":
                        raise SyntaxError("Improper use of parenthesis")
                    tokenized_lst.append(char)
                    continue

                if Calculator.OPERATORS[char].is_single:
                    last_single = char

                # check that 2 single operators don't appear in a row (like ~)
                if Calculator.OPERATORS[char].is_single and last_single == char:
                    raise SyntaxError(f"Improper use of operator {char}")

                Calculator.handle_operator_tokenization(tokenized_lst, char)

            else:  # invalid character
                raise SyntaxError("Invalid character in input")

        # if in number, append to list
        if in_num:
            tokenized_lst.append(float(cur_num))

        return tokenized_lst

    @staticmethod
    def handle_operator_tokenization(token_list: list, operator: str):
        """
        handles everything related to adding operator to token list.
        :param token_list: token list
        :param operator: operator to check
        :raises SyntaxError if operator isn't in valid place
        """
        if operator == "~":
            if (token_list and isinstance(token_list[-1], Operator) and
                    (token_list[-1].symbol == "~~" or token_list[-1].symbol == "~")):
                raise SyntaxError("Improper use of operator ~")

            # catch unary minus and minus that is part of number (replace with ~)
        if operator == "-":
            if token_list and isinstance(token_list[-1], Operator):
                operator = "~"  # minus that is part of operand. max precedence
            elif not Calculator.is_binary_minus(token_list):
                operator = "~~"  # unary minus

            # get Operator object of char
        operator = Calculator.OPERATORS[operator]

        # check if operator is in ok place
        if not operator.can_come_after(token_list[-1] if token_list else None):
            raise SyntaxError(f"Operator out of place: {operator.symbol}")

        token_list.append(operator)  # append Operator object to list

    @staticmethod
    def calculate_tokens(expression: list) -> float:
        """
        calculate expression that list of tokens represents
        :param expression: expression to be calculated. (token list)
        :return: result of calculation
        :raises SyntaxError, ZeroDivisionError, OverFlowError, ValueError
        """
        operands_stk = []
        operators_stk = []

        for element in expression:
            # if number add to operands stack
            if isinstance(element, float):
                operands_stk.append(element)
            elif element == "(":
                operators_stk.append(element)
            elif element == ")":
                # check that ")" doesn't come straight after (
                # if operators_stk and operators_stk[-1] == "(":
                #  raise SyntaxError("Invalid use of parenthesis")

                # calculate everything until opening parenthesis
                while operators_stk and operators_stk[-1] != "(":
                    Calculator.calc_single(operands_stk, operators_stk)

                # if operators stack is empty, it means that there is a missing (
                if not operators_stk:
                    raise SyntaxError("Invalid use of parenthesis")
                # pop (
                operators_stk.pop()
            else:  # element is operator
                # while current operator isn't pre unary, operators stack isn't empty, haven't reached "("
                # and current operator is weaker than top of stack
                while not element.is_pre_unary() and operators_stk and operators_stk[-1] != "(" and \
                        element.precedence <= operators_stk[-1].precedence:
                    Calculator.calc_single(operands_stk, operators_stk)

                # append current operator
                operators_stk.append(element)

        # Perform all remaining operations
        while operators_stk:
            Calculator.calc_single(operands_stk, operators_stk)

        if len(operands_stk) != 1:
            raise SyntaxError("Invalid expression")

        return operands_stk[0]

    @staticmethod
    def calc_single(operands_stk: list, operators_stk: list):
        """
        performs single operation according to stack statuses
        :return operation result
        :raises SyntaxError, ZeroDivisionError, OverFlowError, ValueError
        """

        operator = operators_stk.pop()
        # Catch ( out of place
        if not isinstance(operator, Operator):
            raise SyntaxError(f"Operator or parenthesis out of place: {operator}")

        try:
            if operator.is_unary:
                op1 = operands_stk.pop()
                result = operator.call_func(op1)
            else:
                op2 = operands_stk.pop()
                op1 = operands_stk.pop()
                result = operator.call_func(op1, op2)
            operands_stk.append(result)
        except IndexError:
            raise SyntaxError(f"Operator or parenthesis out of place: {operator.symbol}")

    @staticmethod
    def evaluate(expression: str) -> float | int:
        """
        functions that connects it all. receives a string expression and tries to calculate it
        :return: result of calculation
        :raises SyntaxError, ValueError, ZeroDivisionError, OverflowError
        """
        expression = "".join(expression.split())  # remove all whitespaces
        token_lst = Calculator.tokenize(expression)
        # print(token_lst)
        result = Calculator.calculate_tokens(token_lst)
        result = int(result) if result.is_integer() else round(result, 10)
        return result

    @staticmethod
    def is_binary_minus(token_list: list) -> bool:
        # returns true if minus that comes when list is at this state is binary
        if not token_list:
            return False
        prev = token_list[-1]
        if prev == ")" or isinstance(prev, float):
            return True
        if isinstance(prev, Operator):
            return prev.is_unary and not prev.is_pre
        return False

    @staticmethod
    def testing(expression: str) -> float | int | str:
        """
       function used for testing calculator. does exactly what evaluate does, except it returns "ERROR" if there was
       error
       :return: result of calculation
       """
        expression = "".join(expression.split())  # remove all whitespaces
        try:
            token_lst = Calculator.tokenize(expression)
            result = Calculator.calculate_tokens(token_lst)
            result = int(result) if result.is_integer() else round(result, 10)
            return result

        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
            return "ERROR"

    @staticmethod
    def check_position(token_list: list, element: str | float) -> bool:
        """
        checks if element can come in the end of token_list
        :param token_list: token list
        :param element: element to check. can be str (parenthesis) or float
        :return: true if yes, false otherwise
        """
        if isinstance(element, str):
            if element == "(":
                if not token_list:
                    return True
                return isinstance(token_list[-1], Operator) and (not token_list[-1].is_unary or token_list[-1].is_pre)

        if isinstance(element, float):
            if not token_list:
                return True
            return token_list[-1] == "(" or (
                    isinstance(token_list[-1], Operator) and not token_list[-1].is_post_unary())

        return False


def main():
    try:
        exp = input("Enter math expression: ")

        result = Calculator.evaluate(exp)
        print(f"Result is:  {result}")
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as e:
        print(e)
    except EOFError:
        print("Invalid input")


if __name__ == '__main__':
    main()
