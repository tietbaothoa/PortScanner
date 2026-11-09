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
import re
from concurrent.futures import ThreadPoolExecutor

import utils

# Regex nhận diện IPv4 và IPv6
# Regex nhận diện IPv4 và IPv6
def port_scan(start_port, end_port, output, threads):
    IPv4_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    IPv6_REGEX = re.compile(r"^[a-fA-F0-9:]+$")

    def is_ipv4(ip):
        return bool(IPv4_REGEX.match(ip))
    def is_ipv6(ip):
        return bool(IPv6_REGEX.match(ip))
    def get_process_name(pid):
        """
        Retrieves process name for a given PID.

        Args:
            pid (int): Process ID

        Returns:
            str: Process name or 'N/A' if not found/accessible
        """
        try:
            return psutil.Process(pid).name() if pid else "N/A"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return "N/A"

    def scan_connection(conn, start_port, end_port):
        """
        Scans a single connection and returns connection details if port is in range.

        Args:
            conn: Network connection object
            start_port (int): Lower bound of port range
            end_port (int): Upper bound of port range

        Returns:
            list: [protocol, IP, port, PID, process_name] if in range, None otherwise
        """        
        if conn.laddr and start_port <= conn.laddr.port <= end_port:
            proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            ip = conn.laddr.ip
            port = str(conn.laddr.port)
            pid = str(conn.pid) if conn.pid else "N/A"
            process_name = get_process_name(conn.pid)

            return [proto, ip, port, pid, process_name]
        return None  # Bỏ qua kết nối không thuộc phạm vi cổng

    def scan_local_ports(start_port, end_port, output, threads):
        """
        Performs multi-threaded scan of local ports and formats results.

        Args:
            start_port (int): Starting port number
            end_port (int): Ending port number
            output (str): Output file path
            threads (int): Number of scanning threads

        Output:
            Prints formatted results to console or writes to file
        """
        results = []
        header = ["Proto", "IP Address", "Port", "PID", "Process Name"]
        column_widths = [6, 40, 8, 8, 30]

        formatted_header = " || ".join(h.ljust(w) for h, w in zip(header, column_widths))
        results.append(formatted_header)
        results.append("=" * len(formatted_header))
        connections = psutil.net_connections(kind='inet')

        with ThreadPoolExecutor(max_workers=threads) as executor:
            scan_results = list(executor.map(lambda conn: scan_connection(conn, start_port, end_port), connections))

        scan_results = [res for res in scan_results if res]

        for res in scan_results:
            line = " || ".join(val.ljust(w) for val, w in zip(res, column_widths))
            results.append(line)

        if not output:
            for line in results:
                print(line)
        else:
            with open(output, 'w', encoding='utf-8') as f:
                f.write("\n".join(results))
            print(f"\n✅ Kết quả đã được lưu vào file: {output}")
        
    scan_local_ports(start_port, end_port, output, threads)


def service_scan(output, threads):
    """
    Scans for known services running on local ports.

    Args:
        output (str): Path to output file (None for console output)
        threads (int): Number of concurrent scanning threads

    Output format:
        Port || Service Name || PID || Process Name || Status
    """
    def get_process_info(port):
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port and conn.pid:
                try:
                    process = psutil.Process(conn.pid)
                    return conn.pid, process.name(), "Online"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return conn.pid, "N/A", "Online"
        return "N/A", "N/A", "Offline"

    def scan_port(port):
        if port not in COMMON_PORTS:
            return None
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                pid, process_name, status = get_process_info(port)
                return [port, COMMON_PORTS[port], pid, process_name, status]
        return None

    def scan_local_service(output, threads):
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            scan_results = list(executor.map(scan_port, COMMON_PORTS.keys()))

        open_ports = [res for res in scan_results if res]
        headers = ["Port", "Service Name", "PID", "Process Name", "Status"]
        column_widths = [8, 30, 8, 25, 10]

        formatted_header = " || ".join(h.ljust(w) for h, w in zip(headers, column_widths))
        results.append(formatted_header)
        results.append("=" * len(formatted_header)) 

        results_plain = results.copy() 
        for row in open_ports:
            status_colored = utils.colorize_text(row[4], "green" if row[4] == "Online" else "red")
            row_colored = row[:4] + [status_colored]
            formatted_row_colored = " || ".join(str(row_colored[i]).ljust(column_widths[i]) for i in range(5))
            results.append(formatted_row_colored)

            formatted_row_plain = " || ".join(str(row[i]).ljust(column_widths[i]) for i in range(5))
            results_plain.append(formatted_row_plain)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write("\n".join(results_plain))
            print(f"\n✅ Kết quả đã được lưu vào file: {output}")
        else:
            for line in results:
                print(line)

    COMMON_PORTS = utils.load_common_ports()
    scan_local_service(output, threads)