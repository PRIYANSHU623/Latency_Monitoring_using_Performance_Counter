import tkinter as tk #ui
import psutil #usage(cpu,rem,mem,systemprocess)
import numpy as np 
import time 
from threading import Thread #updating without freezing gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess
import re #regex


total_cores = psutil.cpu_count(logical=True)
DATA_PT = 50 # 50 data point in each core
Smoothing_win =5 
cpu_data = [[0]*DATA_PT for _ in range(total_cores)] # 50 data point in each core
memory_data = [0]*DATA_PT

DARK_BG = '#1e1e1e'
GRID_COLOR = '#333333'
TEXT_COLOR = '#e0e0e0'
MEMORY_COLOR = '#ff6b6b'


CPU_COLORS = [
    '#00d4aa', '#ff6b6b', '#4ecdc4', '#ffd93d',
    '#95e1d3', '#ff8787', '#6bcf7f', '#a8e6cf',
    '#ff85a1', '#84d9d2', '#ffc86b', '#b8c5d6',
    '#ff9999', '#7ed7c1', '#f5cd79', '#a2d5f2'
]

def moving_avg(data, window=3):
    if(len(data)<window):
        return data
    return np.convolve(data, np.ones(window)/window , mode='valid')

def cpu_graph(frame,height=100):
    fig = Figure(figsize=(8,height/100),dpi = 100, facecolor=DARK_BG)
    ax = fig.add_subplot(111, facecolor = DARK_BG)
    canvas  = FigureCanvasTkAgg(fig,master=frame)
    canvas.get_tk_widget().pack(fill='both', expand = True)
    
    
    ax.spines['top'].set_color(GRID_COLOR)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['right'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.tick_params(colors= TEXT_COLOR, which= 'both')

    def update_cpu():
        while True:
            utils = psutil.cpu_percent(interval = None, percpu=True)
            for i in range(len(utils)):
                cpu_data[i].append(utils[i])
                if len(cpu_data[i])> DATA_PT:
                    cpu_data[i].pop(0)

            ax.clear()
            ax.set_facecolor(DARK_BG)
            ax.set_ylim(0,105)
            ax.set_xlim(0,DATA_PT)
            
            # set title of cpu graph
            ax.set_title("CPU Utilization of each Core",color=TEXT_COLOR,fontsize = 12, fontweight = 'bold', pad=10)
            ax.set_ylabel("Usage % ",color=TEXT_COLOR, fontsize=10)
            ax.set_xlabel("Time",color=TEXT_COLOR, fontsize=10)
            
            ax.grid(True, alpha=0.15, color=GRID_COLOR, linestyle = '--',linewidth=0.5)

            for spine in ax.spines.values():
                spine.set_color(GRID_COLOR)
                
            ax.tick_params(colors= TEXT_COLOR, which='both')

            #each core color line
            for i in range(len(utils)):
                smoothed = moving_avg(cpu_data[i],window=Smoothing_win)
                color = CPU_COLORS[i % len(CPU_COLORS)]
                ax.plot(range(len(smoothed)),smoothed,label=f"Core_{i}",color=color,linewidth=2,alpha=0.9)
                
                
            legend = ax.legend(loc='upper right',facecolor = DARK_BG,edgecolor=GRID_COLOR,fontsize = 8, framealpha=0.9)
            for text in legend.get_texts():
                text.set_color(TEXT_COLOR)
                
            fig.tight_layout()
            canvas.draw()
            time.sleep(1)

    Thread(target=update_cpu,daemon=True).start()
    return fig,ax, canvas
            
            
def memory_graph(frame,height=100):
    fig = Figure(figsize=(8,height/100),dpi = 100, facecolor=DARK_BG)
    ax = fig.add_subplot(111, facecolor = DARK_BG)
    canvas  = FigureCanvasTkAgg(fig,master=frame)
    canvas.get_tk_widget().pack(fill='both', expand = True)
    
    
    ax.spines['top'].set_color(GRID_COLOR)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['right'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.tick_params(colors= TEXT_COLOR, which= 'both')

    def update_mem():
        while True:
            mem_util = psutil.virtual_memory().percent
            memory_data.append(mem_util)
            if len(memory_data) > DATA_PT:
                memory_data.pop(0)

            ax.clear()
            ax.set_facecolor(DARK_BG)
            ax.set_ylim(0,105)
            ax.set_xlim(0,DATA_PT)
            
            # set title of memory graph
            ax.set_title("Memory Usage",color=TEXT_COLOR,fontsize = 12, fontweight = 'bold', pad=10)
            ax.set_ylabel("Usage % ",color=TEXT_COLOR, fontsize=10)
            ax.set_xlabel("Time",color=TEXT_COLOR, fontsize=10)
            
            ax.grid(True, alpha=0.15, color=GRID_COLOR, linestyle = '--',linewidth=0.5)

            for spine in ax.spines.values():
                spine.set_color(GRID_COLOR)
                
            ax.tick_params(colors= TEXT_COLOR, which='both')

            
            ax.plot(range(len(memory_data)),memory_data,color=MEMORY_COLOR,linewidth=2.5,label = 'memory' , alpha=0.9)
            ax.fill_between(range(len(memory_data)),memory_data,alpha=0.3,color=MEMORY_COLOR)
            
            legend = ax.legend(loc='upper right',facecolor = DARK_BG,edgecolor=GRID_COLOR,fontsize = 9, framealpha=0.9)
            
            for text in legend.get_texts():
                text.set_color(TEXT_COLOR)
                
            fig.tight_layout()
            canvas.draw()
            time.sleep(1)

    Thread(target=update_mem,daemon=True).start()
    return fig,ax, canvas
            

# print(cpu_data)
# print(memory_data)
