import pyautogui
import time
import random
import platform
import os

# Use 'return' for macOS, 'enter' otherwise.
enter_key = "return" if platform.system() == "Darwin" else "enter"

def random_y_solution(n, total, max_val=6):
    """
    Recursively generate a list of n integers (each between 0 and max_val)
    that sum to total. Returns None if no solution exists.
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
    # We work in y-space: x = y + 2, so x ranges from 2 to 8.
    # Total x sum should be 42, which means total y sum = 42 - 10*2 = 22.
    y_total_required = 22
    y_build = [None] * total_slots

    # Fixed positions (using 0-indexing, but we speak in 1-indexed terms):
    # The 2nd value must be 5 -> y = 5 - 2 = 3.
    y_build[1] = 3
    # The 5th and 6th must be the same as the 2nd.
    y_build[4] = 3
    y_build[5] = 3
    # The 7th value must be 2 -> y = 2 - 2 = 0.
    y_build[6] = 0

    # Free indices: those not fixed above.
    free_indices = [0, 2, 3, 7, 8, 9]

    # Force one extra stat (besides the 7th) to be 2.
    # That means y must be 0 (since 0+2=2).
    extra2_index = random.choice(free_indices)
    y_build[extra2_index] = 0
    free_indices.remove(extra2_index)

    # Force one stat to be the maximum 8 (so y = 6).
    forced8_index = random.choice(free_indices)
    y_build[forced8_index] = 6
    free_indices.remove(forced8_index)

    # Sum so far in y-space from fixed positions:
    # Already fixed: indices 1, 4, 5, 6, plus forced extra 0 and forced maximum 6.
    fixed_sum = y_build[1] + y_build[4] + y_build[5] + y_build[6] + 0 + 6
    # That is: 3 + 3 + 3 + 0 + 0 + 6 = 15.
    remaining_sum = y_total_required - fixed_sum  # 22 - 15 = 7

    # The remaining free indices (should be 4 indices) will share a total of 7,
    # with each y in [0,6].
    sol = random_y_solution(len(free_indices), remaining_sum, 6)
    if sol is None:
        return None
    for idx, y_val in zip(free_indices, sol):
        y_build[idx] = y_val

    # Convert y values back to x values (stat values): x = y + 2.
    build = [y + 2 for y in y_build]

    # Sanity checks:
    if sum(build) != 42:
        return None
    if build[1] != 5:  # 2nd stat must be 5.
        return None
    if build[6] != 2:  # 7th stat must be 2.
        return None
    # There must be exactly two stats with value 2.
    if build.count(2) != 2:
        return None
    # The 2nd, 5th, and 6th (indexes 1,4,5) must be identical.
    if not (build[1] == build[4] == build[5]):
        return None
    # The maximum value must be 8.
    if max(build) != 8:
        return None

    return build

# Wait 5 seconds for you to focus the target textbox/window.
time.sleep(5)
# Optionally click on the target window (adjust coordinates as needed).
pyautogui.click(x=500, y=500)

# Announce that the script is working.
print("Script is working!")
if platform.system() == "Darwin":
    os.system('say "Script is working"')

counter = 0
while True:
    build = None
    while build is None:
        build = generate_build()
    build_str = "/".join(str(stat) for stat in build)
    pyautogui.write(build_str, interval=0)
    time.sleep(2)
    pyautogui.press(enter_key)
    time.sleep(0.01)
    
    counter += 1
    if counter % 25 == 0:
        time.sleep(5)
