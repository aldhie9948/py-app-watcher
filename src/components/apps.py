from tkinter import ttk as tk, Toplevel, IntVar, Menu
from src.helpers.database import Database
from src.components.notification import Notification

class Apps(tk.Frame):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    self.db = Database()
    self.apps_data = []
    self.setup_ui()
    self.load_data()
    
  def setup_ui(self):
    # setup container atau layout
    self.config()
    self.notif = Notification(self)
  
  def load_data(self):
    # load data dari database
    self.apps_data = self.db.fetch_all("SELECT * FROM apps ORDER BY id DESC")
    self.render_apps()
  
  def create_table(self):
    # table frame
    table_frm = tk.Frame(self)
    table_frm.pack(fill="both", expand=True, side="bottom")

    # buat scroll vertical dan horizontal untuk table frame
    y_scroll = tk.Scrollbar(table_frm, orient="vertical")
    y_scroll.pack(side="right", fill="y")

    x_scroll = tk.Scrollbar(table_frm, orient="horizontal")
    x_scroll.pack(side="bottom", fill="x")

    columns = ("id", "name", "type", "value")
    self.table = tk.Treeview(
      table_frm, 
      columns=columns, 
      show="headings", 
      yscrollcommand=y_scroll.set, 
      xscrollcommand=x_scroll.set,
    )

    # konfigurasi kolom table
    self.table.heading("id", text="ID")
    self.table.heading("name", text="Name")
    self.table.heading("type", text="Type")
    self.table.heading("value", text="Value")

    self.table.column("id", width=50, anchor="center")
    self.table.column("name", width=200, anchor="w")
    self.table.column("type", width=100, anchor="center")
    self.table.column("value", width=300, anchor="w")

    self.table.pack(side="left", fill="both", expand=True)

    y_scroll.config(command=self.table.yview)
    x_scroll.config(command=self.table.xview)

    # delete item
    self.table.bind("<Double-1>", lambda e: self.delete_app())

  def get_selection_app(self): 
    selection = self.table.selection()
    if not selection:
      return None
    
    item = self.table.item(selection[0])
    values = item['values']

    app_id = values[0]
    for app in self.apps_data:
      if app['id'] == app_id:
        return app
    
    return None
  
  def delete_app(self):
    app = self.get_selection_app()
    res = self.notif.ask_confirmation()

    if not res: 
      return

    try:   
      table_name = "apps"
      where_clause = "id = ?"
      id = app['id']
      where_params = (id,)

      self.db.delete(
        table=table_name, 
        where_clause=where_clause, 
        where_params=where_params
      )

      self.notif.show_info_popup()
      self.load_data()
    except Exception as e:
      self.notif.show_error_popup(e)



  def render_table(self):
    # hapus isi data table sebelumnya
    for item in self.table.get_children():
      self.table.delete(item)
    
    # masukkan data ke table
    for app in self.apps_data:
      self.table.insert("", "end", values=(
        app['id'], 
        app['name'], 
        app['type'], 
        app['value']
      ))
    
  def app_form_modal(self):
    # set posisi modal
    screen_divider = 3
    x = round(self.winfo_screenwidth() // screen_divider)
    y = round(self.winfo_screenheight() // screen_divider)

    # window modal (block parent)
    self.modal = Toplevel(self)
    self.modal.title("Form app")
    self.modal.geometry(f"360x360+{x}+{y}")

    # frame
    frame = tk.Frame(self.modal, padding=20)
    frame.pack(fill="both", expand=True)

    # buat id variable
    self.id_entry = IntVar()

    # type combobox
    type_combo_values = ["port", "process", "url"]
    self.type_entry = tk.Combobox(frame, values=type_combo_values)
    self.type_entry.set("port")

    tk.Label(frame, text="Name: ").grid(row=0, column=0, sticky="w", pady=5)
    self.name_entry = tk.Entry(frame, width=50)
    self.name_entry.grid(row=1, column=0, pady=5)

    tk.Label(frame, text="Type: ").grid(row=2, column=0, sticky="w", pady=5)
    self.type_entry.grid(row=3, column=0, sticky="w", pady=5)

    tk.Label(frame, text="Value: ").grid(row=4, column=0, sticky="w", pady=5)
    self.value_entry = tk.Entry(frame, width=50)
    self.value_entry.grid(row=5, column=0, pady=5)

    tk.Button(frame, text="Save", command=self.submit_form).grid(row=6, column=0, pady=10)

    # set sebagai modal
    self.modal.transient(self) # set parent
    self.modal.grab_set() # block interaction dengan parent

    self.modal.wait_window()
  
  def submit_form(self):
    try:
      id = self.id_entry.get()
      name = self.name_entry.get()
      type = self.type_entry.get()
      value = self.value_entry.get()

      data:dict[str, any] = {
        "name": name, 
        "type": type, 
        "value": value
      }

      table_name = "apps"
      msg = "New app created successfully."

      # variable id menentukan form update atau create
      if not id:
        self.db.insert(table_name, data)
        self.notif.show_info_popup(msg)
      else:
        where_clause = "id = ?"
        where_params = {"id": id}
        self.db.update(
          table=table_name, 
          data=data, 
          where_clause=where_clause, 
          where_params=where_params
        )

        msg = "App updated successfully."
        self.notif.show_info_popup(msg)

      # refetch data
      self.load_data()

      # close
      self.modal.destroy()

    except Exception as e:
      msg = e
      self.notif.show_error_popup(msg=msg)


  def render_apps(self):
    # clear container terlebih dahulu
    for widget in self.winfo_children():
      widget.destroy()
    
    # render apps
    if not self.apps_data:
      tk.Label(self, text="No data found yet.", justify="center", anchor="center").pack(fill="both", expand=True)
      return
    
    header_frm = tk.Frame(self)
    header_frm.pack(side="top", fill="x")
    
    # title header
    tk.Label(header_frm, text="Monitored Apps", font=("Arial", 12, "bold")).pack(anchor="nw", side="left")

    # button tambah / form app
    add_app_btn = tk.Button(header_frm, text="Add new app", command=self.app_form_modal)
    add_app_btn.pack(side="right")


    tk.Separator(self).pack(pady=10, fill="x", side="top")

    # render table
    self.create_table()

    # render table dengan data
    self.render_table()


    
