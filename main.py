import os
import signal
import time

import mcpi_addons.block as block
import mcpi_addons.minecraft as minecraft


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    RESET = "\033[0m"
    CYAN = "\033[36m"


class Artifacts:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    QUERY = f"\033[1m{Colors.CYAN}? "


def get_user_input(input_type, message="", validate=None):
    valid_types = ["integer", "string", "boolean"]
    if input_type not in valid_types:
        raise ValueError(
            "Invalid input type! Expected 'integer' | 'string' | 'boolean'"
        )

    input_prompt = (
        f"{Artifacts.QUERY}{message or f'Enter {input_type}'}: {Colors.RESET}"
    )

    while True:
        user_input = input(input_prompt)

        if validate:
            validation_result = validate(user_input)
            if isinstance(validation_result, str):
                print(f"{Artifacts.BOLD}{Colors.FAIL}{validation_result}{Colors.RESET}")
                continue

        if input_type == "integer" and user_input.isdigit():
            return int(user_input)
        elif input_type == "string":
            return user_input
        elif input_type == "boolean":
            if user_input.lower() in ["y", "n"]:
                return user_input.lower() == "y"


def block_size_validator(number):
    if not number.isdigit():
        return "Must be a number"
    num = int(number)
    if 2 <= num <= 24:
        return True
    return "Must be in range [2, 24]"


def b52_time_validator(number):
    if not number.isdigit():
        return "Must be a number"
    num = int(number)
    if 3 <= num <= 30:
        return True
    return "Must be in range [3, 30]"


def select_player(mc_instance):
    players = mc_instance.getUsernames()
    print(
        f"{Artifacts.BOLD}Players for which entity IDs were identified:{Colors.RESET}"
    )

    for idx, player in enumerate(players, start=1):
        print(f"{idx}. {player}")

    while True:
        choice = get_user_input("integer", "Select a player")
        if 1 <= choice <= len(players):
            return mc_instance.getPlayerEntityId(players[choice - 1])
        print(
            f"{Colors.FAIL}Invalid choice. Please select a valid option.{Colors.RESET}"
        )


def air_nuke(mc_instance):
    tnt = get_user_input("boolean", "DO YOU WANT TO DO A LITTLE TROLLING?")
    nuke_block = block.TNT if tnt else block.AIR

    player = select_player(mc_instance)
    size = get_user_input("integer", "Input size", block_size_validator)

    player_tile_pos = mc_instance.entity.getTilePos(player)
    mc_instance.setBlocks(
        player_tile_pos.x - size,
        player_tile_pos.y - size,
        player_tile_pos.z - size,
        player_tile_pos.x + size,
        player_tile_pos.y + size,
        player_tile_pos.z + size,
        nuke_block,
        1,
    )


def continuous_bomb(mc_instance):
    player = select_player(mc_instance)
    duration = get_user_input(
        "integer", "How long should this go on?", b52_time_validator
    )
    t_end = time.time() + duration

    while time.time() < t_end:
        tile_pos = mc_instance.entity.getTilePos(player)
        mc_instance.setBlock(tile_pos.x, tile_pos.y - 2, tile_pos.z, block.TNT, 1)


def noah(mc_instance):
    for y in range(-4, 64):
        for x in range(-128, 128):
            for z in range(-128, 128):
                if mc_instance.getBlock(x, y, z) == 0:
                    mc_instance.setBlock(x, y, z, block.WATER_STATIONARY)


def wall(mc_instance):
    mc_instance.setBlocks(-128, -10, -1, 128, 64, 1, block.BEDROCK)


def exit_program():
    exit()


def handle_interrupt(signum, frame):
    print(
        f"\n{Artifacts.BOLD}{Colors.FAIL}KeyboardInterrupt caught! Exiting...{Colors.RESET}"
    )
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    IS_DEBUG = os.environ.get("DEBUG") == "1"

    host_ip = (
        get_user_input("string", "Enter host IP or leave blank for localhost")
        or "localhost"
    )

    try:
        mc_instance = minecraft.Minecraft.create(host_ip)
    except ConnectionRefusedError:
        print(
            f"\n{Artifacts.BOLD}{Colors.FAIL}Connection refused! Exiting...{Colors.RESET}"
        )
        exit()

    functions = {
        "Air nuke": air_nuke,
        "Turn User into B-52": continuous_bomb,
        "Flood": noah,
        "Wall": wall,
        "Exit": exit_program,
    }

    while True:
        print(f"{Colors.HEADER}\nChoose a function:{Colors.RESET}")
        for idx, func_name in enumerate(functions.keys(), start=1):
            print(f"{idx}. {func_name}")

        choice = get_user_input(
            "integer", "Enter the number of the function you want to run"
        )

        if 1 <= choice <= len(functions):
            selected_function = list(functions.values())[choice - 1]
            selected_function(mc_instance)
        else:
            print(
                f"{Colors.FAIL}Invalid choice. Please select a valid option.{Colors.RESET}"
            )
