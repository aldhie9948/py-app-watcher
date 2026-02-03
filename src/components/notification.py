from tkinter import ttk as tk, messagebox

class Notification(tk.Frame):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
  
  def show_info_popup(self, msg:str="Operation completed successfully."):
    messagebox.showinfo("Information", msg)

  def show_error_popup(self, msg:str="Error occurred."):
    messagebox.showerror("Error Info", msg)
  
  def ask_confirmation(self, msg:str="Are you sure?"):
    response = messagebox.askyesno("Confirmation", msg)
    return response

  