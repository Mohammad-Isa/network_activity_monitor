from scapy.all import sniff
import time
import os

STOP_FILE_PATH = "/Users/mohammadisa/Library/CloudStorage/OneDrive-UniversityofHuddersfield/Uniwork/Side_Projects/pythonProject1/stop.txt"
OUTPUT_FILE_PATH = "/Users/mohammadisa/Library/CloudStorage/OneDrive-UniversityofHuddersfield/Uniwork/Side_Projects/pythonProject1/sniffer_output.txt"

def packet_callback(packet):
    with open("/Users/mohammadisa/Library/CloudStorage/OneDrive-UniversityofHuddersfield/Uniwork/Side_Projects/pythonProject1/sniffer_output.txt", "a") as f:
        f.write(str(packet) + "\n")

def run_sniffer():
    while not os.path.exists(STOP_FILE_PATH):
        sniff(prn=packet_callback, filter="ip", store=0, timeout=10)
        # Replace 'en0' with your active interface
        sniff(prn=packet_callback, filter="ip", store=0, iface="en0")

def clear_output_file():
    # Clear the output file
    with open(OUTPUT_FILE_PATH, "w") as f:
        f.write("")

if __name__ == "__main__":
    run_sniffer()
