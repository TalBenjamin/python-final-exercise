from calculator import Calculator
import pytest


@pytest.mark.parametrize("expression, expected_result", [
    # Syntax tests
    ("3^*2", "ERROR"),
    ("(345+-)", "ERROR"),
    ("3.456. +0.54(", "ERROR"),
    ("4-3@$5#", "ERROR"),
    ("3!!-~~4", "ERROR"),
    ("(34+56", "ERROR"),
    ("--~--3", "ERROR"),
    ("~--~-3", "ERROR"),
    ("~~3", "ERROR"),
    # Empty string, gibberish string, whitespace string
    ("", "ERROR"),
    ("kjfdg(g-dfg';fs.", "ERROR"),
    ("\n\t   \n\t\t\t\n     ", "ERROR"),
])
def test_calculator_syntax(expression, expected_result):
    assert Calculator.testing(expression) == expected_result


@pytest.mark.parametrize("expression, expected_result", [
    # simple operators tests
    ("5 - 3", 2),
    ("2 * 4", 8),
    ("10 / 2 * 4", 20),
    ("5@-9", -2),
    ("(4345*23\n #)#", 17),
    ("-4\t^  2", -16),
    ("16^-0.5", 0.25),
    ("6.9   % 2.3", 0),
    ("3!!*2", 1440),
    ("4&2$3", 3),
    ("-5$19", -19),
    ("5$-19", 5),
    ("3!!+(4-2)!", 722),
    ("6!#", 9),
    ("3--3!", "ERROR"),
])
def test_operators(expression, expected_result):
    assert Calculator.testing(expression) == expected_result


@pytest.mark.parametrize("expression, expected_result", [
    # more complicated tests
    ("4 @ 6.4 - 3.5 * (7.9 + 2.2) #", -1.8),
    ("5 + 2 *3@2.5-1^2+4.8 % 2 & 3.2 @ 6 ! #", 14.3),
    ("9$2^3-4@2.8*(5.6 + 3.3)#", 671.2),
    ("2.2 * ~(7.7 - 3.4 @ 2) + 4 ^ (2 $ 5) / 524 % 8", 245),
    ("4.3 @ ~(6 - 3 * (7 + 2.2)) $ 1.5 ^ 2", 167.7025),
    ("6 + 3 % 2 ^ 2 $ 5.2 & ~(2.9 - 1.4 @ 7)#", 7),
    ("~(8 $ (4 ^ 2) - 3 & 6 + 3 * (9 @ 2) @ 3) + 2 $ 4.6", -21.15),
    ("5 & ~(3 + 2) * 80 % 9 + 16 $ 25 ^ 0.5", -35),
    ("(5 + 2 * (3 @ 2) + 19 ^ 3.5)# + 4 % 2 & 3.2 $ 6 ! @ 7 ^ 3 * 2 + 1.5", 214.5),
    ("9 & ~(5 ^ 2) + 3 @ 2 - 2 * 4 $ 3 / 8 ^ 2 + 3 ! @ 3", -18.125),
    ("33 #! * 1.2 - (6 - 3 / (7 + 2)) & 5 ^ 2 & 4", 839),
    ("12 $ (4 ^ 2) - 5 & 8 / 2.5 * (9 @ 6) @ 3 + 13 & 4 ^ -2 * 1.6 / 2", 5.55),
    ("7 ^ 3 / 7 * 13 @ ~(2.6 - 1.2) & 5.4 $ 9 + 81 ^ 0.75 - 4.5 / 1.5", 465),
])
def test_calculator(expression, expected_result):
    assert Calculator.testing(expression) == expected_result
