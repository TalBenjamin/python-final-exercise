from math import pow


def add(operand1: float, operand2: float) -> float:
    return float(operand1 + operand2)


def sub(operand1: float, operand2: float) -> float:
    return float(operand1 - operand2)


def mul(operand1: float, operand2: float) -> float:
    return float(operand1 * operand2)


def div(operand1: float, operand2: float) -> float:
    """
    :return: result of operand1/operand2
    :raises: ZeroDivisionError if operand2 is 0
    """
    return float(operand1 / operand2)


def power(operand1: float, operand2: float) -> float:
    try:
        return pow(operand1, operand2)
    except ValueError:
        raise ValueError(f"Can't do {operand1}^{operand2}")


def my_avg(operand1: float, operand2: float) -> float:
    return float((operand1 + operand2) / 2)


def my_max(operand1: float, operand2: float) -> float:
    return max(operand1, operand2)


def my_min(operand1: float, operand2: float) -> float:
    return min(operand1, operand2)


def modulo(operand1: float, operand2: float) -> float:
    return float(operand1 % operand2)


def neg(operand1: float) -> float:
    return -operand1


def factorial(operand1: float) -> float:
    """
    calculates factorial of operand1
    :param operand1: number to calculate factorial of.
    :return: factorial of operand1
    :raises: ValueError if factorial can't be performed on operand
    """
    if not operand1.is_integer() or operand1 < 0:
        raise ValueError(f"Invalid input for factorial: {operand1}")
    fact = 1
    operand1 = int(operand1)
    for i in range(1, operand1 + 1):
        fact *= i
    return float(fact)
