import signal
import time

import mcpi.minecraft as minecraft
import mcpi_addons.block as block
import mcpi_addons.minecraft as minecraft_client


class Colors:
    """Defines ANSI escape codes for frequently used colors."""

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"


class Styles:
    """Defines ANSI escape codes for various text styles."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    QUERY = f"\033[1m{Colors.CYAN}? "


class UserInput:
    """UserInput is a utility class designed to handle various types of user input.

    This class provides methods to easily obtain integers, strings, and booleans
    from the user in a consistent and error-tolerant manner.
    """

    @staticmethod
    def get_integer(prompt: str, valid_range: range | None = None) -> int:
        """Prompt the user for an integer input.

        :param prompt: The message displayed to the user.
        :return: The integer entered by the user.
        """
        input_prompt = f"{Styles.QUERY}{prompt}: {Styles.RESET}"
        while True:
            user_input = input(input_prompt)

            if not user_input.isdigit():
                print(
                    f"{Styles.BOLD}{Colors.RED}Invalid input: Must be an integer.{Styles.RESET}"
                )
                continue

            if valid_range and int(user_input) not in valid_range:
                print(
                    f"{Styles.BOLD}{Colors.RED}Invalid input: Must be within {min(valid_range)} to {max(valid_range)}.{Styles.RESET}"
                )
                continue

            return int(user_input)

    @staticmethod
    def get_string(prompt: str) -> str:
        """Prompt the user for a string input.

        :param prompt: The message displayed to the user.
        :return: The string entered by the user.
        """
        return input(f"{Styles.QUERY}{prompt}: {Styles.RESET}")

    @staticmethod
    def get_boolean(prompt: str) -> bool:
        """Prompt the user for a boolean input (y/n).

        :param prompt: The message displayed to the user.
        :return: True if 'y' or 'yes', False if 'n' or 'no'.
        """
        while True:
            response = (
                input(f"{Styles.QUERY}{prompt} [y/n]: {Styles.RESET}").strip().lower()
            )
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


class PlayerManger:
    def __init__(self, mc_instance: minecraft.Minecraft):
        self.mc_instance = mc_instance

    def select_player(self) -> int:
        """Select a player from a list of usernames.

        :return: The selected player.
        """
        players = self.mc_instance.getUsernames()
        print(
            f"{Styles.BOLD}Players for which entity IDs were identified:{Styles.RESET}"
        )

        for idx, player in enumerate(players, start=1):
            print(f"{idx}. {player}")

        while True:
            choice = UserInput.get_integer("Select a player")
            if 1 <= choice <= len(players):
                return self.mc_instance.getPlayerEntityId(players[choice - 1])
            print(
                f"{Colors.RED}Invalid choice. Please select a valid option.{Styles.RESET}"
            )


class Troller:
    def __init__(self):
        host_ip = (
            UserInput.get_string("Enter host IP or leave blank for localhost")
            or "localhost"
        )
        try:
            self.mc_instance = minecraft_client.Minecraft.create(host_ip)
        except ConnectionRefusedError:
            print(
                f"\n{Styles.BOLD}{Colors.RED}Connection refused! Exiting...{Styles.RESET}"
            )
            exit()

        self.player_manager = PlayerManger(self.mc_instance)

    def select_method(self):
        methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method))
            and not method.startswith("__")
            and not method == "select_method"
        ]
        while True:
            print(f"{Colors.CYAN}\nChoose a function:{Styles.RESET}")
            for idx, func_name in enumerate(methods):
                print(f"{idx+1}. {func_name.replace('_', ' ').capitalize()}")

            choice = UserInput.get_integer(
                "Enter the number of the function you want to run"
            )

            if 1 <= choice <= len(methods):
                selected_function = getattr(self, methods[choice - 1])
                selected_function()
            else:
                print(
                    f"{Colors.RED}Invalid choice. Please select a valid option.{Styles.RESET}"
                )

    def air_nuke(self):
        tnt = UserInput.get_boolean("DO YOU WANT TO DO A LITTLE TROLLING?")
        nuke_block = block.TNT if tnt else block.AIR

        player = self.player_manager.select_player()
        size = UserInput.get_integer("Input size", range(3, 25))

        player_tile_pos = self.mc_instance.entity.getTilePos(player)
        self.mc_instance.setBlocks(
            player_tile_pos.x - size,
            player_tile_pos.y - size,
            player_tile_pos.z - size,
            player_tile_pos.x + size,
            player_tile_pos.y + size,
            player_tile_pos.z + size,
            nuke_block,
            1,
        )

    def continuous_bomb(self):
        player = self.player_manager.select_player()
        duration = UserInput.get_integer("How long should this go on?", range(4, 61))
        t_end = time.time() + duration

        while time.time() < t_end:
            tile_pos = self.mc_instance.entity.getTilePos(player)
            self.mc_instance.setBlock(
                tile_pos.x, tile_pos.y - 2, tile_pos.z, block.TNT, 1
            )

    def wall(self):
        self.mc_instance.setBlocks(-128, -10, -1, 128, 64, 1, block.BEDROCK)

    @staticmethod
    def exit_program():
        exit()


def handle_interrupt(signum, frame):
    print(
        f"\n{Styles.BOLD}{Colors.RED}KeyboardInterrupt caught! Exiting...{Styles.RESET}"
    )
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    troll_manager = Troller()
    troll_manager.select_method()
