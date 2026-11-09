import socket
import psutil
import concurrent.futures
import threading
import itertools
import time
import sys
import os
import json
from colorama import Fore, Style, init

# Khởi tạo colorama để hỗ trợ màu trên Windows
init(autoreset=True)

# Mapping màu sắc
COLOR_MAP = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE
}

def colorize_text(text, color):
    """
    Applies color formatting to text for terminal output.

    Args:
        text (str): The text to be colored
        color (str): Color name from available options:
                    red, green, yellow, blue, cyan, magenta, white

    Returns:
        str: Color-formatted text string with reset sequence
    """
    return f"{COLOR_MAP.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}"

# def loading_animation(stop_event):
#     """Hiển thị hiệu ứng | / - \ khi quét"""
#     for symbol in itertools.cycle(["|", "/", "-", "\\"]):
#         if stop_event.is_set():
#             break
#         sys.stdout.write(f"\r{utils.colorize_text(symbol, 'yellow')} Processing...")
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write("\rDone!           \n")
    
def load_common_ports(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), r"Database\service_port.json")):
    """
    Loads common port numbers and their associated services from a JSON file.

    Args:
        filename (str): Path to JSON file containing port-service mappings
                       Defaults to 'Database/service_port.json' in module directory

    Returns:
        dict: Dictionary mapping port numbers (int) to service names (str)

    Raises:
        FileNotFoundError: If the specified JSON file doesn't exist
        json.JSONDecodeError: If the JSON file is invalid

    Example:
        >>> ports = load_common_ports()
        >>> ports[80]
        'HTTP'
    """
    with open(filename, "r", encoding="utf-8") as f:
        ports = json.load(f)
    return {int(k): v for k, v in ports.items()}  # Đảm bảo key là số nguyên

def read_file_to_list(file_path):
    """
    Reads a text file and returns non-empty lines as a list.

    Args:
        file_path (str): Path to the text file to read

    Returns:
        list: List of non-empty lines from the file, with whitespace stripped

    Raises:
        FileNotFoundError: If the specified file doesn't exist

    Example:
        >>> read_file_to_list("domains.txt")
        ['example.com', 'test.com', 'domain.com']
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]  # Loại bỏ dòng trống
        return lines
    except FileNotFoundError:
        return []