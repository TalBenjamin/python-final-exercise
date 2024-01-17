from calculator import Calculator


def main():
    try:
        exp = input("Enter math expression: ")
        calc = Calculator()
        result = calc.evaluate(exp)
        print(f"Result is:  {result}")
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as e:
        print(e)
    except EOFError:
        print("Invalid input")


if __name__ == '__main__':
    main()
