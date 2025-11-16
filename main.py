import tkinter as tk
from tkinter import ttk
import cpu_util


def show_frame(frame_name):
    system_frame.pack_forget()
    process_frame.pack_forget()

    sys_button.config(bg='#2d2d2d', fg="#e0e0e0",relief="flat", activebackground='#3d3d3d')
    pgm_button.config(bg='#2d2d2d', fg="#e0e0e0",relief="flat", activebackground='#3d3d3d')

    if frame_name == "System":
        system_frame.pack(fill='both',expand = True, padx=20, pady=20)
        sys_button.config(bg="#00d4aa", fg="white",relief="flat", activebackground='#00BFA5')
    else:
        system_frame.pack(fill='both',expand = True, padx=20, pady=20)
        sys_button.config(bg="#00d4aa", fg="white",relief="flat", activebackground='#00BFA5')
        
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
process_frame = tk.Frame(root, bg='#1a1a1a')

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

# cpu_util.add_memory_graph(mem_frame, height = 150)


root.mainloop()