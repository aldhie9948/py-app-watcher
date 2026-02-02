from tkinter import Tk, ttk as tk
from src.components.sidebar import Sidebar
from src.components.content import ContentArea

BASE_WINDOW = 360
MIN_WINDOW_WIDTH = BASE_WINDOW * 3
MIN_WINDOW_HEIGHT = BASE_WINDOW * 2

SIDEBAR_WIDTH = 200
WRAP_LENGTH_OFFSET = 50
WRAP_LENGTH = MIN_WINDOW_WIDTH - SIDEBAR_WIDTH - WRAP_LENGTH_OFFSET 

class MyApp(Tk):
  def __init__(self):
    super().__init__()
    self.setup_window()
    self.setup_ui()
  
  def setup_window(self):
    self.title("MMS App Monitoring")
    self.geometry(f'{MIN_WINDOW_WIDTH}x{MIN_WINDOW_HEIGHT}')
  
  def setup_ui(self):
    main_frm = tk.Frame(self, padding=20)
    main_frm.pack(fill="both", expand=True)

    self.content = ContentArea(main_frm)
    self.content.pack(side="right", fill="both", expand=True, padx=(10, 0))

    self.sidebar = Sidebar(main_frm, on_menu_click=self.handle_menu)
    self.sidebar.pack(side="left", fill="y")

  def handle_menu(self, menu:str):
    value = menu.lower()
    if value == "dashboard": 
      self.content.show_dashboard()
    elif value == "apps":
      self.content.show_apps()

    
if __name__ == "__main__":
  app = MyApp()
  app.mainloop()