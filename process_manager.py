import psutil
import tkinter as tk
from threading import Thread
import time

def show_process_list(tree, count_label=None):
    #clear if there something
    for proc in tree.get_children():
        tree.delete(proc)
    
    #Get new process
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent','memory_percent','status','num_threads']):
        try:
            processes.append(proc.info)
        except(psutil.NoSuchProcess,psutil.ZombieProcess, psutil.AccessDenied):
            pass
    
    processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    # print(processes)

    for proc in processes[:160]:
        pid=proc.get('pid','N/A')
        name = proc.get('name', 'N/A')
        cpu = f"{proc.get('cpu_percent', 0):.1f}"
        memory = f"{proc.get('memory_percent', 0):.2f}"
        status = proc.get('status', 'N/A')
        status = proc.get('status', 'N/A')
        threads = proc.get('num_threads', 'N/A')

        tree.insert("","end",values=(pid,name,cpu,memory,status,threads,"View"))
        
    #count processes
    if count_label:
        count_label.config(text=f"Processes : {len(processes)}")