import pyautogui
import time
import platform
import os

# Ask the user for a value to use throughout the script.
i = int(input("Enter value for i: "))

# Use 'return' for macOS, 'enter' otherwise.
enter_key = "return" if platform.system() == "Darwin" else "enter"

def deterministic_y_solution(n, total, max_val=6):
    """
    Deterministically generate a list of n integers (each between 0 and max_val)
    that sum to total using for loops. Returns None if no solution exists.
    """
    if n == 0:
        return [] if total == 0 else None
    for choice in range(0, min(max_val, total) + 1):
        if total - choice <= (n - 1) * max_val:
            remainder = deterministic_y_solution(n - 1, total - choice, max_val)
            if remainder is not None:
                return [choice] + remainder
    return None

def generate_build():
    total_slots = 10
    # In "y-space" we have x = y + 2, so x ranges from 2 to 8.
    # Total x sum must be 42, which means total y sum = 42 - 10*2 = 22.
    y_total_required = 22
    y_build = [None] * total_slots

    # Fixed positions (0-indexed):
    # 2nd stat must be 5 -> y = 5 - 2 = 3.
    y_build[1] = 3
    # 5th and 6th stats must match the 2nd.
    y_build[4] = 3
    y_build[5] = 3
    # 7th stat must be 2 -> y = 2 - 2 = 0.
    y_build[6] = 0

    # Identify free indices.
    free_indices = [0, 2, 3, 7, 8, 9]

    # Deterministically force one extra stat to be 2 (y = 0).
    extra2_index = free_indices[i % len(free_indices)]
    y_build[extra2_index] = 0
    free_indices.remove(extra2_index)

    # Deterministically force one stat to be the maximum 8 (y = 6).
    forced8_index = free_indices[i % len(free_indices)]
    y_build[forced8_index] = 6
    free_indices.remove(forced8_index)

    # Calculate the sum already fixed in y-space.
    fixed_sum = y_build[1] + y_build[4] + y_build[5] + y_build[6] + 0 + 6  # 3+3+3+0+0+6 = 15
    remaining_sum = y_total_required - fixed_sum  # 22 - 15 = 7

    # Distribute the remaining sum among the remaining free indices (each in [0,6]).
    sol = deterministic_y_solution(len(free_indices), remaining_sum, 6)
    if sol is None:
        return None
    for idx, y_val in zip(free_indices, sol):
        y_build[idx] = y_val

    # Convert back to x-space: stat value x = y + 2.
    build = [y + 2 for y in y_build]

    # Sanity checks.
    if sum(build) != 42:
        return None
    if build[1] != 5 or build[6] != 2:
        return None
    if build.count(2) != 2:
        return None
    if not (build[1] == build[4] == build[5]):
        return None
    if max(build) != 8:
        return None

    return build

# Wait 5 seconds to allow you to focus the target textbox/window.
time.sleep(5)
pyautogui.click(x=500, y=500)

print("Script is working!")
if platform.system() == "Darwin":
    os.system('say "Script is working"')

# Instead of an infinite loop, use a for loop that runs i times.
for counter in range(i):
    build = None
    while build is None:
        build = generate_build()
    build_str = "/".join(str(stat) for stat in build)
    pyautogui.write(build_str, interval=0)
    time.sleep(1.5)
    pyautogui.press(enter_key)
    time.sleep(0.01)
    
    # Pause every 25 builds.
    if (counter + 1) % 25 == 0:
        time.sleep(5)
