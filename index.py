import tkinter as tk
from tkinter import scrolledtext
from analysis import analyze_tone
from parts import Jumla
from tester import test

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
            output_area.insert(tk.END, printa(jumla.tone) + "\n")
            
            determenistic, statistic = analyze_tone(jumla.tone)
            
            output_area.insert(tk.END, printa("الوزن المحدد:") + "\n")
            output_area.insert(tk.END, printa(determenistic) + "\n")
            
            output_area.insert(tk.END, printa("الوزن المخمّن:") + "\n")
            output_area.insert(tk.END, printa(max(statistic, key=statistic.get)) + "\n")
            
            output_area.insert(tk.END, printa("كافّة التخمينات:") + "\n")
            output_area.insert(tk.END, printa(str(statistic)) + "\n")
            
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
