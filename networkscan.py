import ipaddress
import socket
import os
import platform
import subprocess
import concurrent.futures
import argparse
from concurrent.futures import ThreadPoolExecutor
import utils

def parse_ip_input(ip_input):
    ip_list = []

    if "," in ip_input: 
        ip_list = [ip.strip() for ip in ip_input.split(",") if ip.strip()]
    elif "-" in ip_input:
        try:
            start_ip, end_ip = ip_input.split("-")
            start_ip = ipaddress.IPv4Address(start_ip.strip())
            end_ip = ipaddress.IPv4Address(end_ip.strip())
            
            if int(start_ip) <= int(end_ip):  
                ip_list = [str(ipaddress.IPv4Address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]
            else:
                print("Dải IP không hợp lệ. IP bắt đầu phải nhỏ hơn hoặc bằng IP kết thúc.")
        except ValueError:
            print("Lỗi định dạng IP trong dải IP!")
    else: 
        try:
            network = ipaddress.ip_network(ip_input, strict=False)
            ip_list = [str(ip) for ip in network.hosts()]
        except ValueError:
            ip_list = [ip_input]

    return ip_list

def read_ip_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[❌] Không tìm thấy file: {file_path}")
        return []
    
def ipexist_can(ip_list, output, threads):
    
    def is_ip_alive(ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception:
            return False

    def get_hostname(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return "Unknown"

    def check_ip_list(ip_list, output, threads):
        results = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            alive_status = list(executor.map(is_ip_alive, ip_list))

        # Header và phân cách bảng
        header = f"{'IP':<20} || {'Status':<10} || {'Hostname':<30}"
        separator = "=" * len(header)
        results.append(header)
        results.append(separator)
        for ip, is_alive in zip(ip_list, alive_status):
            status = "Alive" if is_alive else "Not Alive"
            hostname = get_hostname(ip) if is_alive else "-"
            results.append(f"{ip:<20} || {status:<10} || {hostname:<30}")

        if output:
            with open(output, "w", encoding='utf-8') as f:
                for res in results:
                    f.write(res + "\n")
        else:
            for res in results:
                print(res)

    check_ip_list(ip_list, output, threads)

def service_scan(ip_list, start_port, end_port, output, threads):
    """
    Scan for open ports and services on multiple IP addresses.

    Args:
        ip_list (list): List of IP addresses to scan
        start_port (int): Starting port number
        end_port (int): Ending port number
        output (str): Path to output file (None for console output)
        threads (int): Number of concurrent scanning threads

    Output format:
        IP || Port || Service
    """
    def scan_port(ip, port):
       
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    service_name = COMMON_PORTS.get(port, "Unknown Service")
                    return (port, service_name, "Open")
                else:
                    return (port, "Unknown Service", "Closed")
        except Exception:
            return (port, "Unknown Service", "Closed")

    def scan_ip_services(ip):
       
        open_services = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = list(executor.map(lambda port: scan_port(ip, port), range(start_port, end_port + 1)))

        for port, service, status in results:
            if status == "Open":
                open_services.append((ip, port, service))
        return open_services

    def scan_local_service(output):
        
        results = []
        
        header = f"{'IP':<20} || {'Port':<10} || {'Service':<20}"
        results.append(header)
        results.append("=" * len(header))

        for ip in ip_list:
            open_services = scan_ip_services(ip)
            if open_services:  # Chỉ in ra nếu có port mở
                for ip, port, service in open_services:
                    results.append(f"{ip:<20} || {port:<10} || {service:<20}")
                results.append("=" * len(header))  # Phân cách giữa các IP

        if output:
            with open(output, "w", encoding='utf-8') as f:
                for res in results:
                    f.write(res + "\n")
        else:
            for res in results:
                print(res)

    COMMON_PORTS = utils.load_common_ports()
    scan_local_service(output)