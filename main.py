import os
import signal
import time

# Compile libextrapi.so for this to work
import mcpi_addons.block as block
import mcpi_addons.minecraft as minecraft


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

hostip = get_user_input("string", "Enter host IP or leave blank for localhost")

if not hostip:
    hostip = "localhost"

try:
    mc = minecraft.Minecraft.create()
except ConnectionRefusedError:
    print(f"\n{Artifacts.BOLD}{Colors.FAIL}Connection refused! Exiting...{Colors.ENDC}")
    exit()


def block_size_validator(number):
    if not number.isdigit():
        return "Must be a number"
    elif int(number) < 2:
        return "Must be at least 2 blocks"
    elif int(number) > 24:
        return "Can't be larger than 24 blocks"
    else:
        return True


def select_player():
    players = mc.getUsernames()
    print(f"{Artifacts.BOLD}Players for which entity IDs were identified:{Colors.ENDC}")
    for idx in range(len(players)):
        print(f"{idx+1}. {players[idx]}")

    selected_ply = False

    while not selected_ply:
        choice = get_user_input("integer", "Select a player")
        if choice in range(1, len(players) + 1):
            selected_ply = players[choice - 1]
        else:
            print(
                f"{Colors.FAIL}Invalid choice. Please select a valid option.{Colors.ENDC}"
            )
    return mc.getPlayerEntityId(selected_ply)


def air_nuke():
    tnt = get_user_input(
        "boolean",
        f"{Artifacts.UNDERLINE}{Colors.FAIL}DO YOU WANT TO DO A LITTLE TROLLING?",
    )
    nukeblock = block.TNT if tnt else block.AIR
    print(f"{Colors.WARNING}WARNING: AIR NUKE WILL CAUSE DAMAGE{Colors.ENDC}")
    player = select_player()

    size = get_user_input("integer", "Input size", block_size_validator)
    print(f"Nuking radius of {size}")
    playerTilePos = mc.entity.getTilePos(player)
    mc.setBlocks(
        playerTilePos.x - size,
        playerTilePos.y - size,
        playerTilePos.z - size,
        playerTilePos.x + size,
        playerTilePos.y + size,
        playerTilePos.z + size,
        nukeblock,
        1,
    )
    input(f"{Colors.OKGREEN}Nuke successful! Press enter key to return.{Colors.ENDC}")


def b52_time_validator(number):
    if not number.isdigit():
        return "Must be a number"
    elif int(number) < 3:
        return "Must be at least 3 seconds"
    elif int(number) > 30:
        return "Can't be longer than 30 seconds"
    else:
        return True


def continuous_bomb():
    print(f"{Colors.WARNING}WARNING: B-52 MODE WILL CAUSE DAMAGE{Colors.ENDC}")
    player = select_player()
    duration = get_user_input(
        "integer", "How long should this go on?", b52_time_validator
    )
    t_end = time.time() + duration
    while time.time() < t_end:
        tile_pos = mc.entity.getTilePos(player)
        mc.setBlock(tile_pos.x, tile_pos.y - 2, tile_pos.z, block.TNT, 1)
    input(f"{Colors.OKGREEN}Success! Press enter key to return.{Colors.ENDC}")


def noah():
    for y in range(-4, 64):
        for x in range(-128, 128):
            for z in range(-128, 128):
                if mc.getBlock(x, y, z) == 0:
                    mc.setBlock(x, y, z, block.WATER_STATIONARY)


def wall():
    print("You have made Donaldus proud :)")
    mc.setBlocks(-128, -10, -1, 128, 64, 1, block.BEDROCK)
    input(f"{Colors.OKGREEN}Success! Press enter key to return.{Colors.ENDC}")


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
    "Turn User into B-52": continuous_bomb,
    "Flood": noah,
    "Wall": wall,
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
