import tkinter as tk

def on_click():
    global count
    count += 1
    label.config(text=f"Button clicked: {count} times", font=("Arial", 20))

def reset_counter():
    global count
    count = 0
    label.config(text=f"Button clicked: {count} times", font=("Arial", 20))

count = 0

root = tk.Tk()
root.title("Click Counter")

label = tk.Label(root, text="Button clicked: 0 times", font=("Arial", 20))
label.pack(pady=20)

button = tk.Button(root, text="Click me!", command=on_click, font=("Arial", 20))
button.pack(pady=20)

reset_button = tk.Button(root, text="Reset Counter", command=reset_counter, font=("Arial", 20))
reset_button.pack(pady=20)

root.mainloop()

