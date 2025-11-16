import tkinter as tk
from tkinter import ttk
import cpu_util
import process_manager


def show_frame(frame_name):
    system_frame.pack_forget()
    process_frame.pack_forget()

    sys_button.config(bg='#2d2d2d', fg="#e0e0e0",relief="flat", activebackground='#3d3d3d')
    pgm_button.config(bg='#2d2d2d', fg="#e0e0e0",relief="flat", activebackground='#3d3d3d')

    if frame_name == "System":
        system_frame.pack(fill='both',expand = True, padx=20, pady=20)
        sys_button.config(bg="#00d4aa", fg="white",relief="flat", activebackground='#00BFA5')
    else:
        process_frame.pack(fill='both',expand = True, padx=20, pady=20)
        pgm_button.config(bg="#00d4aa", fg="white",relief="flat", activebackground='#00BFA5')
        
root = tk.Tk()
root.title("Latency Monitering using Performance counter")
root.config(bg='#1a1a1a')

screen_width = root.winfo_screenwidth()
screen_height = 2 * root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")


#Header========================================
header_frame = tk.Frame(root, bg='#1a1a1a')
header_frame.pack(fill='x' , padx=20, pady=(10,0))

#Title
title_label = tk.Label(
    header_frame,
    text="System Performance Monitor",
    font=("Segoe UI", 20 , "bold"),
    bg="#1a1a1a",
    fg='#00d4aa'
)
title_label.pack(pady=(10,5))

'''
subtitle_label = tk.Label(
    header_frame,
    text="Real-time Performance Counter Monitoring",
    font=("Segoe UI", 10),
    bg='#1a1a1a',
    fg='#888888'
)
subtitle_label.pack(pady=(0, 10))
'''

#canvas rtectangle

canvas_width = int(screen_width * 1/2)
canvas_height = 40
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#1a1a1a", highlightthickness=0,bd =0)
canvas.pack(padx=10, pady=(0,10))# ======

#Top Buttons
button_width = 22
sys_button = tk.Button(canvas, text="System", width=button_width, font=("Segoe UI", 11, "bold"), bg ='#2d2d2d',fg='#e0e0e0', relief="flat", bd=0, padx=20 , pady=10, cursor="hand2", activebackground="#3d3d3d", activeforeground='white', command=lambda: show_frame("System"))
pgm_button = tk.Button(canvas, text="Process", width=button_width, font=("Segoe UI", 11, "bold"), bg ='#2d2d2d',fg='#e0e0e0', relief="flat", bd=0, padx=20 , pady=10, cursor="hand2", activebackground="#3d3d3d", activeforeground='white', command=lambda: show_frame("Process"))
sys_x = canvas_width * 0.25
pgm_x = canvas_width * 0.75
canvas.create_window(sys_x, canvas_height / 2, window=sys_button)
canvas.create_window(pgm_x, canvas_height / 2, window=pgm_button)
#Frames
system_frame = tk.Frame(root, bg='#1a1a1a')

# system monitering page
header_sys = tk.Frame(system_frame, bg="#1a1a1a")
header_sys.pack(pady=(0, 20))
tk.Label(header_sys, text = "System Monitering Dashboard",font=("Segeo UI",18,"bold"),bg="#1a1a1a",fg="#ffffff").pack()
tk.Label(header_sys, text = "Live tracking of CPU cores and memory usages",font=("Segeo UI",10),bg="#1a1a1a",fg="#888888").pack(pady=(5,0))

cpu_container = tk.Frame(system_frame, bg="#252525", highlightbackground="#00d4aa", highlightthickness=2)
cpu_container.pack(fill="both", padx=10, pady=(0, 15), expand=True)

cpu_header = tk.Frame(cpu_container, bg="#252525")
cpu_header.pack(fill="both", padx=15, pady=(10, 5))
tk.Label(cpu_header,text="CPU Utilization",font=("Segoe UI", 13, "bold"),bg="#252525",fg="#00d4aa").pack(side="left")


#rectangle for Cpu_utils
cpu_frame = tk.Frame(system_frame, bg="#1e1e1e", height=200)
cpu_frame.pack(fill="both", padx=10, pady=(0,10), expand=True)
cpu_frame.pack_propagate(False)

cpu_util.cpu_graph(cpu_frame,height=150)

#rectangle for memeory_utils
mem_container = tk.Frame(system_frame, bg="#252525", highlightbackground="#ff6b6b", highlightthickness=2)
mem_container.pack(fill="both", padx=10, pady=(0, 10), expand=True)

mem_header = tk.Frame(mem_container, bg="#252525")
mem_header.pack(fill="x", padx=15, pady=(10, 5))

tk.Label(mem_header,
    text=" Memory Usage",
    font=("Segoe UI", 13, "bold"),
    bg="#252525",
    fg="#ff6b6b"
).pack(side="left")

mem_frame = tk.Frame(system_frame, bg="gray20", height=200)
mem_frame.pack(fill="both", padx=10, pady=(0,10), expand=True)
mem_frame.pack_propagate(False)

cpu_util.memory_graph(mem_frame, height = 150)




# Process monitering page
#--------------------------------------------------------====================
process_frame = tk.Frame(root, bg='#1a1a1a')
#-----------------------------------------------------------
header_proc = tk.Frame(process_frame, bg='#1a1a1a')
header_proc.pack(pady=(0,10))
tk.Label(header_proc, text = "Process Monitering Dashboard",font=("Segeo UI",18, "bold"),bg="#1a1a1a",fg="#ffffff").pack()
tk.Label(header_proc, text = "Track individual process",font=("Segeo UI",10),bg="#1a1a1a",fg="#888888").pack(pady=(5,0))

process_main_container = tk.Frame(process_frame, bg="#1a1a1a")
process_main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

#side  rect frame for  search
process_search_frame = tk.Frame(process_main_container,bg="#252525", width=(screen_width/5), highlightbackground="#00d4aa", highlightthickness=2)
process_search_frame.pack(side="left", fill='y',padx=(0,10), pady=0,expand=False)
process_search_frame.pack_propagate(False)


search_header = tk.Frame(process_search_frame, bg="#252525")
search_header.pack(fill="x", padx=10, pady=(10, 5))
tk.Label(search_header,text="🔍 Search Process",font=("Segoe UI", 13, "bold"),bg="#252525",fg="#00d4aa").pack()

search_input_frame = tk.Frame(process_search_frame, bg="#252525")
search_input_frame.pack(fill="x", padx=10, pady=(10, 5))

tk.Label(
    search_input_frame,
    text="Name or PID:",
    font=("Segoe UI", 9),
    bg="#252525",
    fg="#e0e0e0"
).pack(anchor="w", pady=(0, 5))

search_var = tk.StringVar()
search_entry = tk.Entry(
    search_input_frame,
    textvariable=search_var,
    font=('Segoe UI',10),
    bg="#1e1e1e",
    fg="#e0e0e0",
    insertbackground="#00d4aa",
    relief="flat",
    bd=0
)
search_entry.pack(fill='x', ipady=8)
search_entry.configure(highlightbackground='#00d4aa',highlightthickness=1)

#search buttons
search_buttons_frame = tk.Frame(process_search_frame, bg="#252525")
search_buttons_frame.pack(fill="x", padx=10, pady=(10, 5))

search_button = tk.Button(
    search_buttons_frame,
    text="Search",
    font=("Segoe UI", 10, "bold"),
    bg="#00d4aa",
    fg="white",
    relief="flat",
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2",
    activebackground="#00bfa5",
    command=lambda: process_manager.search_process(search_var.get(), process_list)
)

search_button.pack(fill="x", pady=(0, 5))

clear_button = tk.Button(
    search_buttons_frame,
    text="Clear",
    font=("Segoe UI", 10),
    bg="#310101",
    fg="#e0e0e0",
    relief="flat",
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2",
    activebackground="#3d3d3d",
    command=lambda: [search_var.set(""), process_manager.refresh_process_list(process_list)]
)
clear_button.pack(fill="x")


# # Filter options
# filter_header = tk.Frame(process_search_frame, bg="#252525")
# filter_header.pack(fill="x", padx=10, pady=(5, 10))

# tk.Label(
#     filter_header,
#     text="⚙️ Filter Options",
#     font=("Segoe UI", 11, "bold"),
#     bg="#252525",
#     fg="#4ecdc4"
# ).pack(anchor="w")


sort_frame = tk.Frame(process_search_frame, bg="#252525")
sort_frame.pack(fill="x", padx=10, pady=(5, 5))
tk.Label(
    sort_frame,
    text="Sort by:",
    font=("Segoe UI", 9),
    bg="#252525",
    fg="#e0e0e0"
).pack(anchor="w", pady=(0, 5))

sort_var = tk.StringVar(value="CPU")
sort_options = ["CPU", "Memory", "Name", "PID"]
for option in sort_options:
    rb = tk.Radiobutton(
        sort_frame,
        text=option,
        variable=sort_var,
        value=option,
        font=("Segoe UI", 9),
        bg="#252525",
        fg="#e0e0e0",
        selectcolor="#1e1e1e",
        activebackground="#252525",
        activeforeground="#00d4aa",
        cursor="hand2",
        #use process_managers fun
        command=lambda: process_manager.sort_process_list(process_list, sort_var.get())
    )
    rb.pack(anchor="w", pady=2)

# Process count display at bottom
process_count_frame = tk.Frame(process_search_frame, bg="#1e1e1e")
process_count_frame.pack(side="bottom", fill="x", padx=10, pady=10)

process_count_label = tk.Label(
    process_count_frame,
    text="Processes: 0",
    font=("Segoe UI", 9, "bold"),
    bg="#1e1e1e",
    fg="#00d4aa",
    pady=8
)
process_count_label.pack()


#process list (right)
process_list_container = tk.Frame(
    process_main_container,
    bg="#252525",
    highlightbackground="#4ecdc4",
    highlightthickness=2
)
process_list_container.pack(side="left", fill="both", expand=True)

list_header = tk.Frame(process_list_container, bg="#252525")
list_header.pack(fill="x", padx=15, pady=(10, 5))
tk.Label(
    list_header,
    text="📋 Running Processes",
    font=("Segoe UI", 13, "bold"),
    bg="#252525",
    fg="#4ecdc4"
).pack(side="left")

# Refresh button
refresh_button = tk.Button(
    list_header,
    text="Refresh",
    font=("Segoe UI", 9, "bold"),
    bg="#4ecdc4",
    fg="white",
    relief="flat",
    bd=0,
    padx=15,
    pady=5,
    cursor="hand2",
    activebackground="#3dbdb3",
    command=lambda: process_manager.show_process_list(process_list, process_count_label)
)
refresh_button.pack(side="right")
# Auto-refresh toggle
auto_refresh_var = tk.BooleanVar(value=True)
auto_refresh_check = tk.Checkbutton(
    list_header,
    text="Auto-refresh",
    variable=auto_refresh_var,
    font=("Segoe UI", 9),
    bg="#252525",
    fg="#e0e0e0",
    selectcolor="#1e1e1e",
    activebackground="#252525",
    activeforeground="#4ecdc4",
    cursor="hand2"
)
auto_refresh_check.pack(side="right", padx=(0, 10))

# Process list frame
list_frame = tk.Frame(process_list_container, bg="#1e1e1e")
list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
#creating treeview
tree_scroll_y = tk.Scrollbar(list_frame)
tree_scroll_y.pack(side="right", fill="y")
#horizontal scro;;
tree_scroll_x = tk.Scrollbar(list_frame, orient="horizontal")
tree_scroll_x.pack(side="bottom", fill="x")

# showing process==============
process_list = ttk.Treeview(
    list_frame,
    columns=("PID", "Name", "CPU%", "Memory%", "Status", "Threads", "More"),
    show="headings",
    yscrollcommand=tree_scroll_y.set,
    xscrollcommand=tree_scroll_x.set,
    height=20
)
tree_scroll_y.config(command=process_list.yview)
tree_scroll_x.config(command=process_list.xview)

# columns
process_list.heading("PID", text="PID")
process_list.heading("Name", text="Process Name")
process_list.heading("CPU%", text="CPU %")
process_list.heading("Memory%", text="Memory %")
process_list.heading("Status", text="Status")
process_list.heading("Threads", text="Threads")
process_list.heading("More", text="Perf Values")

# width
process_list.column("PID", width=80, anchor="center")
process_list.column("Name", width=220, anchor="w")
process_list.column("CPU%", width=100, anchor="center")
process_list.column("Memory%", width=120, anchor="center")
process_list.column("Status", width=100, anchor="center")
process_list.column("Threads", width=80, anchor="center")
process_list.column("More", width=120, anchor="center")

process_list.pack(fill="both", expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="#1e1e1e",
    foreground="#e0e0e0",
    fieldbackground="#1e1e1e",
    borderwidth=0,
    font=("Segoe UI", 9),
    rowheight=25
)
style.configure(
    "Treeview.Heading",
    background="#2d2d2d",
    foreground="#00d4aa",
    font=("Segoe UI", 10, "bold"),
    borderwidth=1,
    relief="flat"
)
style.map("Treeview", background=[("selected", "#00d4aa")], foreground=[("selected", "white")])
process_list.bind("<Double-1>", lambda e: process_manager.show_process_details(process_list))

# to show perf
def on_tree_click(event):
    reg =process_list.identify("region", event.x, event.y)
    if reg =='cell':
        column = process_list.identify_column(event.x)
        row_id = process_list.identify_row(event.y)

        if column == "#7" and row_id:
            values = process_list.item(row_id)['values']
            if values and values[0] != '':
                try:
                    pid = int(values[0])
                    process_name = values[1]
                    process_manager.show_performance_counters(pid,process_name)
                except:
                    pass
                
process_list.bind("<Button-1>", on_tree_click)
process_manager.show_process_list(process_list, process_count_label)
# process_manager.start_auto_refresh(process_list, auto_refresh_var, process_count_label)


show_frame("System")
root.mainloop()