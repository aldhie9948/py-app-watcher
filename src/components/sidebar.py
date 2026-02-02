from tkinter import ttk as tk

class Sidebar(tk.Frame):
  def __init__(self, parent, on_menu_click=None, **kwargs):
    super().__init__(parent, **kwargs)
    self.on_menu_click = on_menu_click
    self.setup_ui()
  
  def setup_ui(self):
    self.config(borderwidth=5, relief="solid", width=200)
    self.pack_propagate(False)
    tk.Label(self, text="Sidebar Menu", font=("Arial", 12, "bold")).pack(pady=10)

    menus = ["Dashboard", "Apps", "Logs"]
    for menu in menus: 
      tk.Button(self, text=menu, command=lambda m=menu: self.handle_click(m)).pack(fill="x", pady=5, padx=10,)

    tk.Separator(self, orient="horizontal").pack(fill="x", pady=20)
    tk.Button(self, text="Start").pack(fill="x")
    tk.Button(self, text="Stop").pack(fill="x", side="bottom")

  def handle_click(self, menu:str): 
    if self.on_menu_click:
      self.on_menu_click(menu)