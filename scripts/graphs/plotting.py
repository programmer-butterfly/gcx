import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from constants import COLOR_MAP, MARKER, COLOR_MAP
from matplotlib.ticker import MaxNLocator

width_bar = 0.2

def customize_chart(information, title):
    font=13
    plt.xlabel(information['x_label'], fontsize=font)
    plt.ylabel(information['y_label'], fontsize=font)
    plt.title(title, fontsize=font+2)
    plt.legend(title=information["legend"], fontsize=font)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=20))
    plt.xticks(rotation=45)
    plt.tight_layout(pad=3.0)  
    plt.grid(linestyle=':', alpha=0.5)

def generate_chart_bar_without_gcn(results_gcx, others, information, output_dir, max_value=None):
    plt.figure(figsize=(10,8))
   
    target_column = information['col'] #analyzed metric
    gcx = results_gcx[results_gcx['algorithm'] == 'GCX']

    column_color = target_column + "_bar"
    plt.bar(gcx['algorithm'].tolist(), gcx[target_column], width=0.5, color=COLOR_MAP[column_color][0], edgecolor='black', label="GCX")

    j=1
    for _, row in others.iterrows():
        plt.bar(row['algorithm'], row[target_column], width=0.5, color=COLOR_MAP[column_color][j], edgecolor='black', label=row['algorithm'])
        j+=1

    file=results_gcx.index[0].upper().split("-")[-1]
    customize_chart(information, f"{information['title']} {file}")

    if max_value != None:
        plt.ylim(0, max_value)

    file = f"{output_dir}/{information['output_file']}-{results_gcx.index[0]}_EN.png"
    plt.savefig(file)
    plt.close()


def generate_chart_bar(results_gcx, others, information, output_dir, max_value=None, without_gcn=False):
    if without_gcn == False:
        plt.figure(figsize=(10,8))
    
        target_column = information['col'] #analyzed metric
        
        algorithms = results_gcx['algorithm'].unique().tolist()
        gcx_number = len(algorithms)
        gc_star = results_gcx[results_gcx['algorithm'] != 'GCX']
        gcx = results_gcx[results_gcx['algorithm'] == 'GCX']

        #GCX results
        plt.bar(gcx['algorithm'].tolist(), gcx[target_column], width=0.5, color=COLOR_MAP[target_column]["highlighted_color"], edgecolor='black', label="GCX")
        plt.bar(gc_star['algorithm'].tolist(), gc_star[target_column], width=0.5, color=COLOR_MAP[target_column]["default_color"], edgecolor='black', label="GC*")

        j=0
        #repair and gcis results
        for index, row in others.iterrows():
            x = np.linspace(-1, gcx_number, 35 + (j*10)) 
            y = np.full_like(x, row[target_column])
            if row['algorithm'] == "REPAIR":
                plt.scatter(x, y, color=COLOR_MAP['line'][j], marker=MARKER[j], s=15, linestyle='None', label=row['algorithm'])
            else:
                plt.scatter(x, y, color=COLOR_MAP['line'][j], marker=MARKER[j],  s=15, linestyle='None', label=row['algorithm'])
            j+=1

        file=results_gcx.index[0].upper().split("-")[-1]
        customize_chart(information, f"{information['title']} {file}")

        if max_value != None:
            plt.ylim(0, max_value)

        plt.xlim(-1, gcx_number)
        file = f"{output_dir}/{information['output_file']}-{results_gcx.index[0]}.png"
        plt.savefig(file)
        plt.close()
        return

    generate_chart_bar_without_gcn(results_gcx, others, information,output_dir, max_value)

def generate_chart_line(results, information, output_dir, max_value, min_value):
    plt.figure(figsize=(10,8))

    j=0
    for algorithm, group in results.groupby('algorithm'):
        plt.plot(group['substring_size'], group['time'], marker=MARKER[j], linewidth=0.5, label=algorithm)
        j= j+1

    #plt.ylim([0, max_value+5])
    plt.xscale('log')
    plt.yscale('log')

    file=results.index[0].upper().split("-")[-1]
    customize_chart(information, f"{information['title']} - {file}")

    file = f"{output_dir}/{information['output_file']}-{results.index[0]}.png"
    plt.savefig(file)
    plt.close()
