# -*- coding: utf-8 -*-
"""
Created on Mon Mar 3 8:10:47 2025

@author: IAN CARTER KULANI

"""


import socket
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import threading

# Function to check if a port is open on the IP address
def check_port(ip_address, port):
    """Check if the given port is open on the specified IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Timeout after 1 second
            result = sock.connect_ex((ip_address, port))
            return result == 0  # Port is open if connect_ex returns 0
    except socket.error:
        return False  # Port is closed if there's an error

# Function to scan ports on an IP address
def scan_ports(ip_address, start_port, end_port):
    """Scan a range of ports on the given IP address."""
    open_ports = []
    closed_ports = []
    
    for port in range(start_port, end_port + 1):
        if check_port(ip_address, port):
            open_ports.append(port)
        else:
            closed_ports.append(port)
    
    return open_ports, closed_ports

# Function to generate the pie chart and display it
def generate_pie_chart(open_ports, closed_ports):
    """Generate a pie chart representing open and closed ports."""
    open_count = len(open_ports)
    closed_count = len(closed_ports)
    
    # Pie chart data
    labels = ['Open Ports', 'Closed Ports']
    sizes = [open_count, closed_count]
    colors = ['#8A2BE2', '#D3D3D3']  # Purple and light gray

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.

    return fig

# Function to handle the scanning and displaying of results
def start_scan():
    try:
        ip_address = ip_entry.get().strip()
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
        
        # Validate the port range
        if start_port < 0 or end_port > 65535 or start_port > end_port:
            messagebox.showerror("Invalid Port Range", "Port range should be between 0 and 65535 and start port should be less than or equal to end port.")
            return
        
        # Scan the ports
        open_ports, closed_ports = scan_ports(ip_address, start_port, end_port)

        # Update the results in the GUI
        open_ports_label.config(text=f"Open Ports: {open_ports}")
        closed_ports_label.config(text=f"Closed Ports: {closed_ports}")
        
        # Generate and display the pie chart
        fig = generate_pie_chart(open_ports, closed_ports)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=3)
        canvas.draw()
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for ports.")

# Function to monitor network traffic
def monitor_traffic():
    """Monitor the network traffic (bytes sent/received) on the system."""
    while True:
        # Get network statistics
        net_stats = psutil.net_io_counters()
        
        # Update traffic information in the GUI
        sent_label.config(text=f"Bytes Sent: {net_stats.bytes_sent / (1024 * 1024):.2f} MB")
        recv_label.config(text=f"Bytes Received: {net_stats.bytes_recv / (1024 * 1024):.2f} MB")
        
        # Refresh every 1 second
        window.after(1000, monitor_traffic)

# Creating the main window using Tkinter
window = tk.Tk()
window.title("Port Scan and Traffic Monitor Tool")
window.geometry("600x600")
window.config(bg="#D3D3D3")  # Light gray background color

# Title label
title_label = tk.Label(window, text="Port Scan and Open Port Finder", font=("Arial", 18), fg="#8A2BE2", bg="#D3D3D3")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# IP Address label and entry field
ip_label = tk.Label(window, text="Enter IP Address:", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
ip_label.grid(row=1, column=0, padx=10, pady=10)
ip_entry = tk.Entry(window, font=("Arial", 12), width=20)
ip_entry.grid(row=1, column=1)

# Start Port label and entry field
start_port_label = tk.Label(window, text="Start Port:", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
start_port_label.grid(row=2, column=0, padx=10, pady=10)
start_port_entry = tk.Entry(window, font=("Arial", 12), width=20)
start_port_entry.grid(row=2, column=1)

# End Port label and entry field
end_port_label = tk.Label(window, text="End Port:", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
end_port_label.grid(row=3, column=0, padx=10, pady=10)
end_port_entry = tk.Entry(window, font=("Arial", 12), width=20)
end_port_entry.grid(row=3, column=1)

# Scan Button
scan_button = tk.Button(window, text="Start Scan", font=("Arial", 12), bg="#8A2BE2", fg="white", command=start_scan)
scan_button.grid(row=4, column=0, columnspan=3, pady=20)

# Labels for open and closed ports
open_ports_label = tk.Label(window, text="Open Ports: []", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
open_ports_label.grid(row=6, column=0, columnspan=3, pady=5)

closed_ports_label = tk.Label(window, text="Closed Ports: []", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
closed_ports_label.grid(row=7, column=0, columnspan=3, pady=5)

# Network Traffic labels
sent_label = tk.Label(window, text="Bytes Sent: 0 MB", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
sent_label.grid(row=8, column=0, columnspan=3, pady=5)

recv_label = tk.Label(window, text="Bytes Received: 0 MB", font=("Arial", 12), fg="#8A2BE2", bg="#D3D3D3")
recv_label.grid(row=9, column=0, columnspan=3, pady=5)

# Start monitoring traffic in a separate thread
traffic_thread = threading.Thread(target=monitor_traffic, daemon=True)
traffic_thread.start()

# Run the Tkinter event loop
window.mainloop()
