import socket
import sys
from datetime import datetime

def scan_ports(target_host, start_port, end_port):
    print(f"\n[INFO] Starting scan on host: {target_host}")
    print(f"[INFO] Port range: {start_port} - {end_port}")
    print(f"[INFO] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print(f"[ERROR] Could not resolve hostname: {target_host}")
        return
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  
                result = s.connect_ex((target_ip, port))  

                if result == 0:
                    print(f"[OPEN] Port {port} is open")
                else:
                    print(f"[CLOSED] Port {port} is closed")

        except socket.timeout:
            print(f"[TIMEOUT] Port {port} scan timed out")
        except socket.error as e:
            print(f"[ERROR] Could not scan port {port}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error on port {port}: {e}")

    print(f"\n[INFO] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def validate_input(host, start, end):
    if not (0 <= start <= 65535 and 0 <= end <= 65535):
        raise ValueError("Ports must be between 0 and 65535")
    if start > end:
        raise ValueError("Start port must be less than or equal to end port")
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError("Invalid hostname or IP address")

if __name__ == "__main__":
    try:
        target = input("Enter target host (e.g., 127.0.0.1 or scanme.nmap.org): ").strip()
        start_port = int(input("Enter start port: ").strip())
        end_port = int(input("Enter end port: ").strip())

        validate_input(target, start_port, end_port)
        scan_ports(target, start_port, end_port)

    except ValueError as ve:
        print(f"[INPUT ERROR] {ve}")
    except KeyboardInterrupt:
        print("\n[INFO] Scan cancelled by user.")
        sys.exit()
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")