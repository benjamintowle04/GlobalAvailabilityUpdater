############################################# GUI FOR Availability Updater #############################################
import tkinter as tk
from tkinter import ttk, messagebox


################################################# Opening Window #######################################################
def on_ok():
    print(f"External ID: {external_id.get()}")
    root.quit()  # Quit the application when OK is pressed

root = tk.Tk()
root.title("Global Availability Updater")
root.geometry("400x80")

# Label and Entry widget for External ID
ttk.Label(root, text="External ID:").grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
external_id = ttk.Entry(root, width=30)
external_id.grid(column=1, row=2, padx=10, pady=5)

# Button to generate the schedule
generate_button = ttk.Button(root, text="Update Availability", command=on_ok)
generate_button.grid(column=0, row=3, columnspan=2, pady=10)

# Add padding around the entire grid
for child in root.winfo_children():
    child.grid_configure(padx=10, pady=5)

# Run the application
root.mainloop()
