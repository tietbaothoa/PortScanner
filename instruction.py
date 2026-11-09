import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

# Các tính năng trong bộ công cụ
# Xử lý các tham số dòng lệnh 
# Scan local port, web port, network port
# Scan local service, web service, network service

def local_parse(subparsers):
    """
    Creates and configures a subparser for local computer scanning operations.
    
    Parameters:
        subparsers: argparse._SubParsersAction
            The subparser container to which the local parser will be added
    
    Returns:
        argparse.ArgumentParser: Configured parser for local scanning with options:
            -l: Type of scan (PORT/SERVICE)
            -sP: Start port number (default=1)
            -eP: End port number (default=65535) 
            -o: Output file path (optional)
    """
    local_parser = subparsers.add_parser("Local", help="Local Computer Scanner.")
    # local_parser.add_argument("file", help="Path to file")
    local_parser.add_argument(
        "-l",
        type=str,
        help="Local Scanner Port or Service",
        choices=["PORT", "SERVICE"],
        default="SERVICE",
        required=True,
    )
    local_parser.add_argument(
        "-sP",
        type=int,
        default=1,
        metavar="STARTPORT",
        help="Start Port",
        required=False
    )
    local_parser.add_argument(
        "-eP",
        type=int,
        default=65535,
        metavar="ENDPORT",
        help="End Port",
        required=False
    )
    local_parser.add_argument(
        "-o",
        type=str,
        nargs="?",  # Cho phép giá trị tùy chọn
        const="local_scan_output.txt",
        # default="output.txt",
        metavar="PATH",
        help="Path output file",
        required=False
    )
    return local_parser

def web_parse(subparsers):
    """
    Creates and configures a subparser for web scanning operations.
    
    Parameters:
        subparsers: argparse._SubParsersAction
            The subparser container to which the web parser will be added
    
    Returns:
        argparse.ArgumentParser: Configured parser for web scanning with options:
            -w: Type of scan (SERVICE/SUBDOMAIN/PATH)
            -u: Target URL/IP address
            -f: File containing list of domains/IPs
            -sP: Start port number (default=1)
            -eP: End port number (default=65535)
            -o: Output file path (optional)
    """
    web_parser = subparsers.add_parser("Web", help="Website Scanner.")
    # web_parser.add_argument("HOST", help="URL or IP Address")
    web_parser.add_argument(
        "-w",
        type=str,
        choices=["SERVICE", "SUBDOMAIN", "PATH"],
        default="SERVICE",
        help="Web Scanner Port, Service, Sub-Domain or Path",
        required=True,
    )
    web_parser.add_argument(
        "-u",
        type=str,
        metavar="URL/IP",
        help="URL or IP Address",
        required=False
    )
    web_parser.add_argument(
        "-f",
        type=str,
        metavar="FILE LIST",
        help="File List Domain or IP",
        required=False
    )
    web_parser.add_argument(
        "-sP",
        type=int,
        default=1,
        metavar="STARTPORT",
        help="Start Port",
        required=False
    )
    web_parser.add_argument(
        "-eP",
        type=int,
        default=65535,
        metavar="ENDPORT",
        help="End Port",
        required=False
    )
    web_parser.add_argument(
        "-o",
        type=str,
        nargs="?",  
        const="web_scan_output.txt",
        # default="output.txt",
        metavar="PATH",
        help="Path output file",
        required=False
    )
    return web_parser

def network_parse(subparsers):
    """
    Creates and configures a subparser for network scanning operations.
    
    Parameters:
        subparsers: argparse._SubParsersAction
            The subparser container to which the network parser will be added
    
    Returns:
        argparse.ArgumentParser: Configured parser for network scanning with options:
            -n: Type of scan (EXIST/SERVICE/NETWORK)
            -i: Target IP/IP range/IP list
            -f: File containing list of IPs
            -sP: Start port number (default=1)
            -eP: End port number (default=65535)
            -o: Output file path (optional)
    """
    network_parser = subparsers.add_parser("Network", help="Network Computer Scanner.")
    network_parser.add_argument(
        "-n",
        type=str,
        choices=["EXIST", "SERVICE", "NETWORK"],
        default="EXIST",
        help="Network Scan Exist, Service, Infomation, Network Service of Computer in Internal",
        required=True
    )
    network_parser.add_argument(
        "-i",
        type=str,
        metavar="IP",
        help="IP, IP List or IP Range Separated by Commas",
        required=False
    )
    network_parser.add_argument(
        "-f",
        type=str,
        metavar="FILE LIST",
        help="File List IP",
        required=False
    )
    network_parser.add_argument(
        "-sP",
        type=int,
        default=1,
        metavar="STARTPORT",
        help="Start Port",
        required=False
    )
    network_parser.add_argument(
        "-eP",
        type=int,
        default=65535,
        metavar="ENDPORT",
        help="End Port",
        required=False
    )
    network_parser.add_argument(
        "-o",
        type=str,
        nargs="?",  # Cho phép giá trị tùy chọn
        const="network_scan_output.txt",
        # default="output.txt",
        metavar="PATH",
        help="Path output file",
        required=False
    )
    return network_parser

def parse_args(h_parser: argparse.ArgumentParser) -> argparse.Namespace:
    """
    Configures and parses command line arguments for the scanning toolkit.
    
    Parameters:
        h_parser: argparse.ArgumentParser
            The main argument parser object
    
    Returns:
        argparse.Namespace: Parsed command line arguments containing:
            - Global thread count setting (-t/--threads)
            - Command mode selection (Local/Web/Network)
            - Mode-specific arguments based on selected command
    
    Example Usage:
        parser = argparse.ArgumentParser(description="Port Scanner Toolkit")
        args = parse_args(parser)
    """
    h_parser.add_argument(
        "-t", "--threads",
        type=int,
        default=10,
        metavar="THREADS",
        help="Multi-thread scan, default uses 10 threads.",
        required=False,
    )
    subparsers = h_parser.add_subparsers(title="Commands in modes", dest="command")
    
    local_parser = local_parse(subparsers)
    web_parser = web_parse(subparsers)
    network_parser = network_parse(subparsers)
    
    return h_parser.parse_args()
