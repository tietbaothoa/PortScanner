import socket
import argparse
import time
import psutil
import pyfiglet
from concurrent.futures import ThreadPoolExecutor

import instruction
import localscan
import webscan
import networkscan
import utils

if __name__ == "__main__":
    # Generate and display the application banner
    banner = pyfiglet.figlet_format("Scanner Toolkit", font="Cybermedium")
    print(utils.colorize_text(banner, "green"), end="")
    print(utils.colorize_text("="*80, "green"))
    
    parser = argparse.ArgumentParser(description="Port Scanner Toolkit.")
    args = instruction.parse_args(h_parser=parser)
    print(f"\nMode: {args.command}")
    print(f"Threads: {args.threads}")
    if args.command == "Local":
        """
        Local scanning mode handler
        Options:
            PORT: Scans specific port range on local machine
            SERVICE: Scans for running services on local machine
        """
        print(f"Scanning Type: {args.l}")
        print(f"Start Port: {args.sP}")
        print(f"End Port: {args.eP}")

        if args.l == "PORT":
            if args.o:
                localscan.port_scan(args.sP, args.eP, args.o, args.threads)
                exit(0)
            localscan.port_scan(args.sP, args.eP, None, args.threads)
        elif args.l == "SERVICE":
            if args.o:
                localscan.service_scan(args.o, args.threads)
                exit(0)
            localscan.service_scan(None, args.threads)
            
    elif args.command == "Web":
        """
        Web scanning mode handler
        Options:
            SERVICE: Scans for open ports and services on web targets
            SUBDOMAIN: Performs subdomain enumeration
            PATH: Performs filepath scanning
        """
        print(f"Scanning Type: {args.w}")
        print(f"Start Port: {args.sP}")
        print(f"End Port: {args.eP}")
        
        domain_or_list = None
        if args.u:
            domain_or_list = args.u
        elif args.f:
            # domain_or_list = utils.read_file_to_list(args.f)
            domain_or_list = args.f

        if args.w == "SERVICE":
            if args.o:
                webscan.service_scan(domain_or_list, args.sP, args.eP, args.o, args.threads)
                exit(0)
            webscan.service_scan(domain_or_list, args.sP, args.eP, None, args.threads)
        elif args.w == "SUBDOMAIN":
            if args.o:
                webscan.subdomain_scan(domain_or_list, args.o, args.threads)
                exit(0)
            webscan.subdomain_scan(domain_or_list, None, args.threads)
        elif args.w == "PATH":
            if args.o:
                webscan.filepath_scan(domain_or_list, args.o, args.threads)
                exit(0)
            webscan.filepath_scan(domain_or_list, None, args.threads)
            
    elif args.command == "Network":
        """
        Network scanning mode handler
        Options:
            EXIST: Checks for existence of IP addresses
            SERVICE: Scans for services on network targets
        """
        print(f"Scanning Type: {args.n}")
        print(f"Start Port: {args.sP}")
        print(f"End Port: {args.eP}")
        
        ip_or_listip = None
        if args.i:
            ip_or_listip = networkscan.parse_ip_input(args.i)
        elif args.f:
            ip_or_listip = networkscan.read_ip_from_file(args.f) 

        if args.n == "EXIST":
            if args.o:
                networkscan.ipexist_can(ip_or_listip, args.o, args.threads)
                exit(0)
            networkscan.ipexist_can(ip_or_listip, None, args.threads)
        elif args.n == "SERVICE":
            if args.o:
                networkscan.service_scan(ip_or_listip, args.sP, args.eP, args.o, args.threads)
                exit(0)
            networkscan.service_scan(ip_or_listip, args.sP, args.eP, None, args.threads)