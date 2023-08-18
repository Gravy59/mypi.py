import os
import signal
import sys


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    CYAN = "\033[36m"


class Artifacts:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    QUERY = f"\033[1m{Colors.CYAN}? "


def get_user_input(input_type, message="", validate=None):
    if input_type not in ["integer", "string", "boolean"]:
        raise ValueError(
            "Invalid input type! Expected 'integer' | 'string' | 'boolean'"
        )

    if not message:
        message = f"Enter {input_type}"

    if input_type == "boolean":
        message = f"{message} [y/n]"

    while True:
        user_input = input(f"{Artifacts.QUERY}{message}: {Colors.ENDC}")

        if validate:
            validation_result = validate(user_input)
            if isinstance(validation_result, str):
                print(f"{Artifacts.BOLD}{Colors.FAIL}{validation_result}{Colors.ENDC}")
                continue

        if input_type == "integer" and user_input.isdigit():
            return int(user_input)
        elif input_type == "string":
            return user_input
        elif input_type == "boolean":
            if user_input.lower() == "y":
                return True
            elif user_input.lower() == "n":
                return False
            else:
                print(
                    f"{Artifacts.BOLD}{Colors.FAIL}Invalid boolean input. Please enter 'y' or 'n'.{Colors.ENDC}"
                )
        else:
            print(
                f"{Artifacts.BOLD}{Colors.FAIL}Invalid input type specified.{Colors.ENDC}"
            )


IS_DEBUG = os.environ.get("DEBUG") == "1"


def number_validator(number):
    if not number.isdigit():
        return "Must be a number"
    elif int(number) < 4:
        return "Must be at least 4 blocks"
    elif int(number) > 24:
        return "Can't be larger than 24 blocks"
    else:
        return True


def air_nuke():
    print(f"{Colors.WARNING}WARNING: AIR NUKE WILL CAUSE DAMAGE{Colors.ENDC}")
    size = get_user_input("integer", "Input size", number_validator)
    print(f"Nuking radius of {size}")
    # do stuff here later
    input(f"{Colors.OKGREEN}Nuke successful! Press enter key to return.{Colors.ENDC}")


def exit_program():
    print(f"{Colors.OKBLUE}Exiting the program.{Colors.ENDC}")
    exit()


def handle_interrupt(signum, frame):
    print(
        f"\n{Artifacts.BOLD}{Colors.FAIL}KeyboardInterrupt caught! Exiting...{Colors.ENDC}"
    )
    exit()


# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_interrupt)

# Create a dictionary to map function names to their corresponding functions
functions = {
    "Air nuke": air_nuke,
    "Exit": exit_program,
}

while True:
    # Display the list of function options to the user
    print(f"{Colors.HEADER}\nChoose a function:{Colors.ENDC}")
    for idx, func_name in enumerate(functions.keys(), start=1):
        print(f"{idx}. {func_name}")

    # Ask the user to select a function
    choice = get_user_input(
        "integer", "Enter the number of the function you want to run"
    )

    if choice in range(1, len(functions) + 1):
        # Retrieve the selected function and execute it
        selected_function = list(functions.values())[choice - 1]
        print("\033c", end="")
        selected_function()
    else:
        print("\033c", end="")
        print(
            f"{Colors.FAIL}Invalid choice. Please select a valid option.{Colors.ENDC}"
        )
