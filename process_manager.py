import psutil
import numpy as np
from threading import Thread
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess
import re

def show_process_list(tree, count_label=None):
    for proc in tree.get_children():
        tree.delete(proc)
    
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
        
    if count_label:
        count_label.config(text=f"Processes : {len(processes)}")
        

def get_perf_counters(pid, duration=2):
    
    try:
        cmd = [
            'perf', 'stat',
            '-e', 'cycles,instructions,cache-references,cache-misses,branches,branch-misses,page-faults,context-switches',
            '-p', str(pid),
            'sleep', str(duration)
        ]
        
        result = subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            timeout=duration + 2
        )
        
        output = result.stderr + result.stdout
        
        perf_data = {
            'cpu_cycles': 'N/A',
            'instructions': 'N/A',
            'ipc': 'N/A',  
            'cache_references': 'N/A',
            'cache_misses': 'N/A',
            'cache_miss_rate': 'N/A',
            'branches': 'N/A',
            'branch_misses': 'N/A',
            'branch_miss_rate': 'N/A',
            'page_faults': 'N/A',
            'context_switches': 'N/A'
        }
        
        cycles_match = re.search(r'([\d,]+)\s+cycles', output)
        if cycles_match:
            perf_data['cpu_cycles'] = cycles_match.group(1)
        
        inst_match = re.search(r'([\d,]+)\s+instructions', output)
        if inst_match:
            perf_data['instructions'] = inst_match.group(1)
        
        ipc_match = re.search(r'([\d.]+)\s+insn per cycle', output)
        if ipc_match:
            perf_data['ipc'] = ipc_match.group(1)
        
        cache_ref_match = re.search(r'([\d,]+)\s+cache-references', output)
        if cache_ref_match:
            perf_data['cache_references'] = cache_ref_match.group(1)
        
        cache_miss_match = re.search(r'([\d,]+)\s+cache-misses', output)
        if cache_miss_match:
            perf_data['cache_misses'] = cache_miss_match.group(1)
            if perf_data['cache_references'] != 'N/A':
                try:
                    misses = int(cache_miss_match.group(1).replace(',', ''))
                    refs = int(perf_data['cache_references'].replace(',', ''))
                    if refs > 0:
                        miss_rate = (misses / refs) * 100
                        perf_data['cache_miss_rate'] = f"{miss_rate:.2f}%"
                except:
                    pass
        
        branch_match = re.search(r'([\d,]+)\s+branches', output)
        if branch_match:
            perf_data['branches'] = branch_match.group(1)
        
        branch_miss_match = re.search(r'([\d,]+)\s+branch-misses', output)
        if branch_miss_match:
            perf_data['branch_misses'] = branch_miss_match.group(1)
            if perf_data['branches'] != 'N/A':
                try:
                    misses = int(branch_miss_match.group(1).replace(',', ''))
                    total = int(perf_data['branches'].replace(',', ''))
                    if total > 0:
                        miss_rate = (misses / total) * 100
                        perf_data['branch_miss_rate'] = f"{miss_rate:.2f}%"
                except:
                    pass
        
        pf_match = re.search(r'([\d,]+)\s+page-faults', output)
        if pf_match:
            perf_data['page_faults'] = pf_match.group(1)
        
        cs_match = re.search(r'([\d,]+)\s+context-switches', output)
        if cs_match:
            perf_data['context_switches'] = cs_match.group(1)
        
        return perf_data
        
    except subprocess.TimeoutExpired:
        return {'error': 'Perf command timed out'}
    except FileNotFoundError:
        return {'error': 'Perf tool not found. Please install linux-tools package.'}
    except PermissionError:
        return {'error': 'Permission denied. Run with sudo or adjust perf_event_paranoid settings.'}
    except Exception as e:
        return {'error': f'Error running perf: {str(e)}'}
     
        
        
def show_performance_counters(pid, process_name):
    perf_window = tk.Toplevel()
    perf_window.title(f"Performance Counters - {process_name}")
    perf_window.geometry("700x600")
    perf_window.configure(bg="#1a1a1a")
    
    header = tk.Frame(perf_window, bg="#252525")
    header.pack(fill="x", padx=10, pady=10)
    
    tk.Label(
        header,
        text=f" Performance Counters",
        font=("Segoe UI", 16, "bold"),
        bg="#252525",
        fg="#00d4aa"
    ).pack()
    
    tk.Label(
        header,
        text=f"{process_name} (PID: {pid})",
        font=("Segoe UI", 11),
        bg="#252525",
        fg="#888888"
    ).pack(pady=(5, 0))
    
    status_label = tk.Label(
        perf_window,
        text="Collecting performance data...",
        font=("Segoe UI", 10, "italic"),
        bg="#1a1a1a",
        fg="#ffd93d"
    )
    status_label.pack(pady=10)
    
    details_frame = tk.Frame(perf_window, bg="#1e1e1e")
    details_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    scrollbar = tk.Scrollbar(details_frame)
    scrollbar.pack(side="right", fill="y")
    
    text_widget = tk.Text(
        details_frame,
        font=("Consolas", 10),
        bg="#1e1e1e",
        fg="#e0e0e0",
        wrap="word",
        padx=15,
        pady=15,
        yscrollcommand=scrollbar.set
    )
    text_widget.pack(fill="both", expand=True)
    scrollbar.config(command=text_widget.yview)
    
    # Button frame
    button_frame = tk.Frame(perf_window, bg="#1a1a1a")
    button_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    # Refresh button
    refresh_btn = tk.Button(
        button_frame,
        text="Refresh",
        font=("Segoe UI", 10, "bold"),
        bg="#4ecdc4",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        activebackground="#3dbdb3",
        command=lambda: refresh_perf_data()
    )
    refresh_btn.pack(side="left", padx=(0, 5))
    
    # Close button
    close_btn = tk.Button(
        button_frame,
        text="Close",
        font=("Segoe UI", 10, "bold"),
        bg="#ff6b6b",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        activebackground="#ff5252",
        command=perf_window.destroy
    )
    close_btn.pack(side="right")
    
    def refresh_perf_data():
        status_label.config(text="Collecting performance data...", fg="#ffd93d")
        text_widget.config(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", "Please wait while collecting performance counters...\n")
        text_widget.config(state="disabled")
        perf_window.update()
        
        def collect_data():
            perf_data = get_perf_counters(pid, duration=2)
            
            if 'error' in perf_data:
                details = f"""
ERROR: {perf_data['error']}

# TROUBLESHOOTING:
# 1. Install perf tools:
#    sudo apt-get install linux-tools-common linux-tools-generic
   
# 2. Adjust permissions (if permission denied):
#    sudo sysctl -w kernel.perf_event_paranoid=-1
   
#    Or for permanent change:
#    echo 'kernel.perf_event_paranoid=-1' | sudo tee -a /etc/sysctl.conf
   
3. Run this application with sudo for full access to perf counters.
"""
                status_label.config(text="Error collecting data", fg="#ff6b6b")
            else:
                details = f"""
===============================================================
                    CPU PERFORMANCE METRICS
===============================================================

 CPU CYCLES
   Total Cycles: {perf_data['cpu_cycles']}
   
 INSTRUCTIONS
   Total Instructions: {perf_data['instructions']}
   Instructions Per Cycle (IPC): {perf_data['ipc']}
   
   Note: Higher IPC show better CPU efficiency
   
================================================================
                    CACHE PERFORMANCE
================================================================

 CACHE REFERENCES
   Total References: {perf_data['cache_references']}
   
 CACHE MISSES
   Total Misses: {perf_data['cache_misses']}
   Miss Rate: {perf_data['cache_miss_rate']}
   
   Note: Lower cache miss rate shows better memory access patterns
   
================================================================
                    BRANCH PREDICTION
================================================================

 BRANCHES
   Total Branches: {perf_data['branches']}
   
  BRANCH MISSES
   Total Misses: {perf_data['branch_misses']}
   Miss Rate: {perf_data['branch_miss_rate']}
   
   Note: Lower branch miss rate shows better code predictability
   
================================================================
                    MEMORY & CONTEXT
================================================================

 PAGE FAULTS
   Total Page Faults: {perf_data['page_faults']}
   
   Note: High page faults may indicate insufficient memory
   
 CONTEXT SWITCHES
   Total Context Switches: {perf_data['context_switches']}
   
   Note: High context switches may shows CPU contention
   
================================================================

Data collected over 2 second sampling period
"""
                status_label.config(text="Performance data updated successfully", fg="#00d4aa")
            
            text_widget.config(state="normal")
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", details)
            text_widget.config(state="disabled")
        
        Thread(target=collect_data, daemon=True).start()
    
    refresh_perf_data()



# def show_process_list(tree, count_label=None):
#     for item in tree.get_children():
#         tree.delete(item)
    
#     processes = []
#     for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'num_threads']):
#         processes.append(proc.info)
        
    
#     processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    
#     for proc in processes[:150]:  
#         pid = proc.get('pid', 'N/A')
#         name = proc.get('name', 'N/A')
#         cpu = f"{proc.get('cpu_percent', 0):.1f}"
#         memory = f"{proc.get('memory_percent', 0):.2f}"
#         status = proc.get('status', 'N/A')
#         threads = proc.get('num_threads', 'N/A')
        
#         tree.insert("", "end", values=(pid, name, cpu, memory, status, threads,"View"))

#     if count_label:
#         count_label.config(text=f"Processes: {len(processes)}")


# searching a process
def search_process(search_term, tree, count_label=None):
    """Search for a process by name or PID"""
    for item in tree.get_children():
        tree.delete(item)
    
    if not search_term.strip():
        show_process_list(tree, count_label)
        return
    
    processes = []
    search_lower = search_term.lower()
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'num_threads']):
        try:
            proc_info = proc.info
            proc_name = proc_info.get('name', '').lower()
            proc_pid = str(proc_info.get('pid', ''))
            
            if search_lower in proc_name or search_term in proc_pid:
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    
    for proc in processes:
        try:
            pid = proc.get('pid', 'N/A')
            name = proc.get('name', 'N/A')
            cpu = f"{proc.get('cpu_percent', 0):.1f}"
            memory = f"{proc.get('memory_percent', 0):.2f}"
            status = proc.get('status', 'N/A')
            threads = proc.get('num_threads', 'N/A')
            
            tree.insert("", "end", values=(pid, name, cpu, memory, status, threads))
        except Exception:
            continue
    
    if count_label:
        count_label.config(text=f"Results: {len(processes)}")
    
    if not processes:
        tree.insert("", "end", values=("", f"No processes found matching '{search_term}'", "", "", "", ""))



def sort_process_list(tree, sort_by):
    items = []
    for item in tree.get_children():
        values = tree.item(item)['values']
        items.append(values)
    
    for item in tree.get_children():
        tree.delete(item)
    
    
    if sort_by == "CPU":
        items.sort(key=lambda x: float(x[2]) if x[2] != '' else 0, reverse=True)
    elif sort_by == "Memory":
        items.sort(key=lambda x: float(x[3]) if x[3] != '' else 0, reverse=True)
    elif sort_by == "Name":
        items.sort(key=lambda x: str(x[1]).lower())
    elif sort_by == "PID":
        items.sort(key=lambda x: int(x[0]) if str(x[0]).isdigit() else 0)

    for item in items:
        tree.insert("", "end", values=item)



def show_process_details(tree):
    selection = tree.selection()
    if not selection:
        return
    
    item = tree.item(selection[0])
    values = item['values']
    
    if not values or values[0] == '':
        return
    
    try:
        pid = int(values[0])
        proc = psutil.Process(pid)
        
        detail_window = tk.Toplevel()
        detail_window.title(f"Process Details - {values[1]}")
        detail_window.geometry("500x400")
        detail_window.configure(bg="#1a1a1a")
        
        header = tk.Frame(detail_window, bg="#252525")
        header.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            header,
            text=f"📊 {values[1]}",
            font=("Segoe UI", 14, "bold"),
            bg="#252525",
            fg="#00d4aa"
        ).pack()
        
        details_frame = tk.Frame(detail_window, bg="#1e1e1e")
        details_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        text_widget = tk.Text(
            details_frame,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#e0e0e0",
            wrap="word",
            padx=15,
            pady=15
        )
        text_widget.pack(fill="both", expand=True)
        
        details = f"""
PID: {proc.pid}
Name: {proc.name()}
Status: {proc.status()}
CPU Usage: {proc.cpu_percent(interval=0.1):.1f}%
Memory Usage: {proc.memory_percent():.2f}%
Memory Info: {proc.memory_info().rss / (1024**2):.1f} MB
Threads: {proc.num_threads()}
Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proc.create_time()))}

Command Line:
{' '.join(proc.cmdline()) if proc.cmdline() else 'N/A'}

Working Directory:
{proc.cwd() if proc.cwd() else 'N/A'}
"""
        
        text_widget.insert("1.0", details)
        text_widget.config(state="disabled")
        
        # Close button
        close_btn = tk.Button(
            detail_window,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg="#00d4aa",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=detail_window.destroy
        )
        close_btn.pack(pady=(0, 10))
        
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"Error accessing process: {e}")


# auto refresh
def start_auto_refresh(process_list, auto_refresh_var, process_count_label):
    """Start auto-refresh thread for process list"""
    def auto_refresh():
        while True:
            if auto_refresh_var.get():
                try:
                    show_process_list(process_list, process_count_label)
                except Exception:
                    pass
            time.sleep(3)  
    
    Thread(target=auto_refresh, daemon=True).start()