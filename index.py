import tkinter as tk
import helpers
from tkinter import scrolledtext
from analysis import analyze_tone
from parts import Jumla
from tester import test
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize the tester
test()

def printa(txt: str):
    return str(txt)

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")
    if event.keycode==65535: 
        event.widget.event_generate("<<Clear>>")
    if event.keycode==65: 
        event.widget.event_generate("<<SelectAll>>")

def main_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Arabic Poetry Analyzer")
    root.geometry("700x500")  # Window size
    root.bind_all("<Key>", _onKeyRelease, "+")

    # Create a label for the input
    label = tk.Label(root, text="أدخل شطرًا واحدًا من البيت:")
    label.pack(pady=10)

    # Create an input field
    input_field = tk.Entry(root, width=70)
    input_field.pack(pady=10)

    # Create a ScrolledText widget to show the results
    output_area = scrolledtext.ScrolledText(root, height=10, width=70)
    output_area.pack(pady=10)

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)


    # Embed the Matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
    # Function to handle button click
    def on_button_click():
        try:
            # Get input text from the input field
            shatr = input_field.get()
            shatr = " ".join(shatr.split())  # Clean the input
            
            # Process the input
            jumla = Jumla(shatr)
            
            # Collect the results
            output_area.delete(1.0, tk.END)  # Clear the output area
            
            output_area.insert(tk.END, printa("الإيقاع:") + "\n")
            output_area.insert(tk.END, printa(helpers.beats_to_arood_writing(jumla.tone)) + "\n")
            
            determenistic, statistic = analyze_tone(jumla.tone)
            
            output_area.insert(tk.END, printa("الوزن المحدد:") + "\n")
            output_area.insert(tk.END, printa(determenistic) + "\n")
            
            output_area.insert(tk.END, printa("الوزن المرجّح:") + "\n")
            output_area.insert(tk.END, printa(max(statistic, key=statistic.get)) + "\n")
            
            output_area.insert(tk.END, printa("كافّة الترجيحات:") + "\n")
            output_area.insert(tk.END, printa(helpers.format_buhoor_scores_dict(statistic)) + "\n")

                # Extract keys and values
            keys = [x.name for x in list(statistic.keys())]
            values = list(statistic.values())

            # Create bar chart
            ax.clear()
            ax.bar(keys, values, color='skyblue')
            ax.set_title("Scores of common Buhoor")
            ax.set_xlabel("Bah")
            ax.set_ylabel("Score")
            canvas.draw()

        except Exception as e:
            print(e)
            output_area.insert(tk.END, "Error: {}".format(e) + "\n")

    # Create a button to trigger the analysis
    analyze_button = tk.Button(root, text="تحليل", command=on_button_click)
    analyze_button.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main_gui()
