import pyautogui
import time
import random

def random_y_solution(n, total, max_val=5):
    """
    Generate a list of n nonnegative integers (each ≤ max_val) that sum to total.
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
    build[0] = 5    # 1st stat is 5
    build[6] = 2    # 7th stat is 2

    # Choose one additional (random) stat to be 2.
    allowed_extra2 = [i for i in range(total_slots) if i not in (0, 6)]
    extra2_index = random.choice(allowed_extra2)
    build[extra2_index] = 2

    # The remaining 8 - 1 = 7 variable positions (from allowed_extra2, excluding extra2_index)
    variable_indices = [i for i in allowed_extra2 if i != extra2_index]
    # These 7 positions must sum to: 42 - (5 + 2 + 2) = 33.
    # They must be between 3 and 8. Let x = y + 3 so that y ∈ [0, 5].
    # Then the 7 y's must sum to 33 - (7 * 3) = 12.
    # Also, at least one of the x's must be 8 ⟹ at least one y equals 5.
    n = 7
    target = 12
    y_solution = None
    for _ in range(1000):
        sol = random_y_solution(n, target, 5)
        if sol is not None and 5 in sol:  # ensures at least one x will be 8
            y_solution = sol
            break
    if y_solution is None:
        return None  # try again if a solution wasn’t found

    # Convert y values back to x values (x = y + 3)
    x_values = [y + 3 for y in y_solution]
    # Assign the generated x values to the 7 variable positions.
    for idx, val in zip(variable_indices, x_values):
        build[idx] = val

    # Sanity check (optional):
    #   Sum must be 42, exactly two stats equal 2, S1 is 5, S7 is 2, and max is 8.
    if sum(build) != 42 or build[0] != 5 or build[6] != 2 or build.count(2) != 2 or max(build) != 8:
        return None
    return build

# Wait 5 seconds so you can focus the target textbox/window.
time.sleep(5)

while True:
    build = None
    # Try until a valid build is generated.
    while build is None:
        build = generate_build()
    # Format the build as: "#/#/#/#/#/#/#/#/#/#"
    build_str = "/".join(str(stat) for stat in build)
    # Type the build instantly (each build is one complete message) and press Enter.
    pyautogui.write(build_str, interval=0)
    pyautogui.press("enter")
