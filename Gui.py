import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import sys

# Define paths
OUTPUT_FILE_PATH = "/Users/mohammadisa/Library/CloudStorage/OneDrive-UniversityofHuddersfield/Uniwork/Side_Projects/pythonProject1/sniffer_output.txt"
STOP_FILE_PATH = "/Users/mohammadisa/Library/CloudStorage/OneDrive-UniversityofHuddersfield/Uniwork/Side_Projects/pythonProject1/stop.txt"


class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Sniffer")

        # Clear Results Button
        self.clear_button = tk.Button(root, text="Clear Results", command=self.clear_results)
        self.clear_button.pack()

        # Stop Button
        self.stop_button = tk.Button(root, text="Stop Sniffing", command=self.stop_sniffing)
        self.stop_button.pack()

        # Text Box for displaying packet data
        self.text_box = tk.Text(root, height=10, width=80)
        self.text_box.pack()

        # Create a plot for showing packet count over time
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Initialize lists for plotting
        self.packet_times = []
        self.packet_counts = []

        # Flags for controlling threads
        self.sniffer_running = False

        # Start the plotting thread
        self.plotting_thread = threading.Thread(target=self.update_plot, daemon=True)
        self.plotting_thread.start()

        # Start the result updating thread
        self.result_thread = threading.Thread(target=self.update_results, daemon=True)
        self.result_thread.start()

    def clear_results(self):
        # Clear the output file
        try:
            with open(OUTPUT_FILE_PATH, "w") as f:
                f.truncate(0)  # Truncate the file to zero length
        except Exception as e:
            print(f"Failed to clear output file: {e}")
        # Clear the text box
        self.text_box.delete(1.0, tk.END)
        # Clear the plot
        self.packet_times = []
        self.packet_counts = []
        self.ax.clear()
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Number of Packets')
        self.ax.set_title('Packets Received Over Time')
        self.canvas.draw()

    def start_sniffer(self):
        if not self.sniffer_running:
            self.sniffer_running = True
            # Create a stop file to ensure sniffer script starts fresh
            if os.path.exists(STOP_FILE_PATH):
                os.remove(STOP_FILE_PATH)
            # Clear the output file before starting sniffing
            self.clear_results()
            # Start the packet sniffing in a separate thread
            self.sniffer_thread = threading.Thread(target=self.run_sniffer, daemon=True)
            self.sniffer_thread.start()

    def stop_sniffing(self):
        if self.sniffer_running:
            self.sniffer_running = False
            # Create a stop file to signal the sniffer script to stop
            with open(STOP_FILE_PATH, "w") as f:
                f.write("")
            # Optionally, terminate the program
            self.root.quit()
            sys.exit()

    def run_sniffer(self):
        # Run the sniffer script
        while self.sniffer_running:
            os.system(
                f'sudo python3 /Users/mohammadisa/Library/CloudStorage/OneDrive-UniversityofHuddersfield/Uniwork/Side_Projects/pythonProject1/sniffer.py')
            # Sleep for a short period to avoid rapid looping
            time.sleep(1)

    def update_results(self):
        # Continuously read results from the file and update the text box
        while True:
            if os.path.exists(OUTPUT_FILE_PATH):
                with open(OUTPUT_FILE_PATH, "r") as f:
                    data = f.read()
                    self.text_box.delete(1.0, tk.END)
                    self.text_box.insert(tk.END, data)
            else:
                self.text_box.insert(tk.END, "No data found. Make sure the sniffer script is running.")
            time.sleep(2)  # Update interval

    def update_plot(self):
        # Continuously update the plot with packet counts
        while True:
            if os.path.exists(OUTPUT_FILE_PATH):
                with open(OUTPUT_FILE_PATH, "r") as f:
                    lines = f.readlines()
                    packet_count = len(lines)

                    # Record the current time and packet count
                    self.packet_times.append(datetime.now())
                    self.packet_counts.append(packet_count)

                    # Remove old data to keep only the last 10 minutes
                    while self.packet_times and (datetime.now() - self.packet_times[0]).total_seconds() > 600:
                        self.packet_times.pop(0)
                        self.packet_counts.pop(0)

                    # Plot the data
                    self.ax.clear()
                    self.ax.plot(self.packet_times, self.packet_counts, label='Packets Count')
                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('Number of Packets')
                    self.ax.set_title('Packets Received Over Time')
                    self.ax.legend()
                    self.figure.autofmt_xdate()  # Auto-format date labels
                    self.canvas.draw()

            time.sleep(10)  # Update interval


if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)

    # Start the sniffing when the application starts
    app.start_sniffer()

    root.mainloop()
