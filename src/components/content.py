from tkinter import ttk as tk
from src.components.apps import Apps

class ContentArea(tk.Frame):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    self.setup_ui()
  
  def setup_ui(self):
    self.config(borderwidth=1, relief="solid", padding=10)
  
  def clear(self):
    for widget in self.winfo_children():
      widget.destroy()

  def show_dashboard(self):
    self.clear()
    tk.Label(self, text="dashboard dasdklaskdjaskdj").pack()
  
  def show_apps(self):
    self.clear()
    self.apps = Apps(self)
    self.apps.pack(side="left", fill="both", expand=True)
    
    