from datetime import datetime
import time
import sympy as sp
import re


def get_current_time():
    return datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")


def set_timer(seconds, botName):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(f"{botName}: Timer is currently on {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print(f"{botName}: Your timer has ended now at {get_current_time()}!")


def mathsSolver(expression):
    expression = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expression.replace("^", "**"))

    try:
        if "=" in expression:
            left_side, right_side = expression.split("=")
            equation = sp.Eq(sp.sympify(left_side), sp.sympify(right_side))
        else:
            equation = sp.Eq(sp.sympify(expression), 0)

        # Solve the equation
        return sp.solve(equation)
    except Exception as e:
        return f"Error: {str(e)}"
