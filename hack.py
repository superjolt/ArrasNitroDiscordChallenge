import pyautogui
import time
import random

def random_y_solution(n, total, max_val=5):
    """
    Recursively generate a list of n integers (each between 0 and max_val) that sum to total.
    Returns None if no solution exists.
    """
    if n == 0:
        return [] if total == 0 else None
    valid_choices = []
    for i in range(0, min(max_val, total) + 1):
        if total - i <= (n - 1) * max_val:
            valid_choices.append(i)
    if not valid_choices:
        return None
    choice = random.choice(valid_choices)
    remainder = random_y_solution(n - 1, total - choice, max_val)
    if remainder is None:
        return None
    return [choice] + remainder

def generate_build():
    total_slots = 10
    build = [None] * total_slots

    # Fixed stats:
    build[0] = 5    # 1st stat is 5.
    build[6] = 2    # 7th stat is 2.

    # Choose one additional stat (from indexes other than 0 and 6) to be 2.
    allowed_extra2 = [i for i in range(total_slots) if i not in (0, 6)]
    extra2_index = random.choice(allowed_extra2)
    build[extra2_index] = 2

    # The remaining slots:
    fixed_sum = 5 + 2 + 2  # = 9
    remaining_sum = 42 - fixed_sum  # = 33

    # The remaining slots (let x = y + 3 so each stat is between 3 and 8)
    # The required sum of the y's is:
    y_total = remaining_sum - 7 * 3  # 33 - 21 = 12.
    variable_indices = [i for i in range(total_slots) if build[i] is None]
    n = len(variable_indices)  # This is 7.

    # Force one of the variables to be 5 (i.e. x value 8)
    forced_index = random.choice(variable_indices)
    # Remove the forced index from the list to solve for the other n-1 slots.
    variable_indices.remove(forced_index)
    forced_y = 5
    remaining_y_total = y_total - forced_y

    # Solve for the other slots.
    sol = random_y_solution(n - 1, remaining_y_total, 5)
    if sol is None:
        return None

    # Build the full list of y's in order.
    # Assign forced value.
    y_solution = {forced_index: forced_y}
    # Shuffle the order of the solution to match variable_indices order.
    for idx, y_val in zip(variable_indices, sol):
        y_solution[idx] = y_val

    # Convert y's back to x's (x = y + 3).
    for idx in range(total_slots):
        if build[idx] is None:
            build[idx] = y_solution[idx] + 3

    # Sanity check.
    if sum(build) != 42 or build[0] != 5 or build[6] != 2 or build.count(2) != 2 or max(build) != 8:
        return None

    return build

# Wait 5 seconds for you to focus the target textbox/window.
time.sleep(5)

while True:
    build = None
    while build is None:
        build = generate_build()
    # Format the build as "#/#/#/#/#/#/#/#/#/#"
    build_str = "/".join(str(stat) for stat in build)
    # Type the build instantly and press Enter.
    pyautogui.write(build_str, interval=0)
    pyautogui.press("enter")
    # Wait 10 milliseconds before the next build.
    time.sleep(0.01)
