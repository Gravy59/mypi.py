# Gravy’s Minecraft Pi Trolling Script

## Description

This Python script provides a set of trolling functions using the `mcpi` library. Features include air nuking, continuous bombing, flooding, and wall creation. It has an interactive CLI interface for easy use.

## Functions

- **Air Nuke**: Create a large explosion or air pocket around a player.
- **Turn User into B-52**: Continuously drop TNT blocks beneath a player for a specified time.
- **Flood**: Flood the entire map with water.
- **Wall**: Create a bedrock wall.
- **Exit**: Exit the utility.

## Requirements

- Python 3.9+
- Minecraft Pi Edition
- `mcpi` library
- `mcpi_addons` library

## Installation

Clone this repository and install the `mcpi` and `mcpi-addons` libraries:

```bash
pip install mcpi mcpi-addons
```

Run the script
```bash
python main.py
```

## Usage

1. Run the script.
2. Follow the on-screen instructions to perform various actions in Minecraft Pi Edition.

## Signal Handling

The script has built-in signal handling for `SIGINT` (Ctrl+C). If the script is interrupted, it will safely exit.

## Customization

You can easily extend the `functions` dictionary to add more functionality to the utility.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Please see the `LICENSE` file for details on how the code in this repo is licensed.

