from tkinter import ttk as tk
from src.helpers.database import Database

class ContentArea(tk.Frame):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    self.setup_ui()
    self.db = Database()
  
  def setup_ui(self):
    self.config(borderwidth=5, relief="solid")
  
  def clear(self):
    for widget in self.winfo_children():
      widget.destroy()

  def show_dashboard(self):
    self.clear()
    tk.Label(self, text="dashboard dasdklaskdjaskdj").pack()
  
  def show_apps(self):
    self.clear()
    apps = self.db.fetch_all('SELECT * FROM apps')
    for app in apps:
      tk.Label(self, text=app['name']).pack()
    
    