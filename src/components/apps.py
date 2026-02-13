from tkinter import ttk as tk, Toplevel, IntVar, Menu, StringVar, Text, END
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
        self.notif = Notification(self)

    def load_data(self):
        # load data dari database
        self.apps_data = self.db.fetch_all("SELECT * FROM apps ORDER BY id DESC")

        # create form var
        self.id_text = IntVar()
        self.name_text = StringVar()
        self.type_text = StringVar()
        self.value_text = StringVar()
        self.callback_text = StringVar()

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

        columns = ("id", "name", "type", "value", "callback")
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
        self.table.heading("value", text="Target")
        self.table.heading("callback", text="Callback")

        self.table.column("id", width=50, anchor="center", minwidth=50)
        self.table.column("name", width=200, anchor="w", minwidth=100)
        self.table.column("type", width=100, anchor="center", minwidth=80)
        self.table.column("value", width=300, anchor="w", minwidth=150)
        self.table.column("callback", width=500, anchor="w", minwidth=200)

        self.table.pack(side="left", fill="both", expand=True)

        y_scroll.config(command=self.table.yview)
        x_scroll.config(command=self.table.xview)

        # delete item
        self.table.bind("<Double-1>", lambda e: self.delete_app())

        self.table.bind("<Button-3>", self.show_context_menu)

    def get_selection_app(self):
        selection = self.table.selection()
        if not selection:
            return None

        item = self.table.item(selection[0])
        values = item["values"]

        app_id = values[0]
        for app in self.apps_data:
            if app["id"] == app_id:
                return app

        return None

    def load_data_for_update(self):
        # ambil data dari table
        app = self.get_selection_app()

        # set value ke entry
        self.id_text.set(app["id"])
        self.name_text.set(app["name"])
        self.type_text.set(app["type"])
        self.value_text.set(app["value"])
        self.callback_text.set(app["callback"])

        # tampilkan app form modal
        self.app_form_modal()

    def create_context_menu(self):
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.load_data_for_update)
        self.context_menu.add_command(label="Delete", command=self.delete_app)

    def show_context_menu(self, event):

        # create context menu
        self.create_context_menu()

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def delete_app(self):
        app = self.get_selection_app()
        res = self.notif.ask_confirmation("Are you sure to delete this item ?")

        if not res:
            return

        try:
            table_name = "apps"
            where_clause = "id = ?"
            id = app["id"]
            where_params = (id,)

            self.db.delete(
                table=table_name, where_clause=where_clause, where_params=where_params
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
            self.table.insert(
                "",
                "end",
                values=(
                    app["id"],
                    app["name"],
                    app["type"],
                    app["value"],
                    app["callback"],
                ),
            )

    def app_form_modal(self):
        # set posisi modal
        screen_divider = 3
        x = round(self.winfo_screenwidth() // screen_divider)
        y = round(self.winfo_screenheight() // screen_divider)

        # window modal (block parent)
        self.modal = Toplevel(self)
        self.modal.title("Form app")
        self.modal.geometry(f"480x360+{x}+{y}")

        # frame
        frame = tk.Frame(self.modal, padding=20)
        frame.pack(fill="both", expand=True)

        # type combobox
        type_combo_values = ["port", "process", "url"]
        type_entry = tk.Combobox(
            frame, values=type_combo_values, textvariable=self.type_text
        )
        type_entry.set(self.type_text.get())

        # form name
        tk.Label(frame, text="Name: ").grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(frame, width=70, textvariable=self.name_text).grid(
            row=1, column=0, pady=5, sticky="w"
        )

        # form type
        tk.Label(frame, text="Type: ").grid(row=2, column=0, sticky="w", pady=2)
        type_entry.grid(row=3, column=0, sticky="w", pady=5)

        # form value
        tk.Label(frame, text="Value: ").grid(row=4, column=0, sticky="w", pady=2)
        tk.Entry(frame, width=70, textvariable=self.value_text).grid(
            row=5, column=0, pady=5, sticky="w"
        )

        # form callback
        tk.Label(frame, text="Callback: ").grid(row=6, column=0, sticky="w", pady=2)
        self.callback_entry = Text(frame, width=50, height=5)
        self.callback_entry.grid(row=7, column=0, pady=5, sticky="w")
        if self.callback_text.get():
            self.callback_entry.insert(END, self.callback_text.get())

        tk.Button(frame, text="Save", command=self.submit_form).grid(
            row=8, column=0, pady=10
        )

        # set sebagai modal
        self.modal.transient(self)  # set parent
        self.modal.grab_set()  # block interaction dengan parent

        # on close event
        self.modal.protocol("WM_DELETE_WINDOW", self.reset_form)

        self.modal.wait_window()

    def submit_form(self):
        try:
            data: dict[str, any] = {
                "name": self.name_text.get(),
                "type": self.type_text.get(),
                "value": self.value_text.get(),
                "callback": self.callback_entry.get("1.0", END),
            }

            table_name = "apps"
            msg = "New app created successfully."

            # variable id menentukan form update atau create
            if not self.id_text.get():
                self.db.insert(table_name, data)
                self.notif.show_info_popup(msg)
            else:
                where_clause = "id = ?"
                where_params = (self.id_text.get(),)
                self.db.update(
                    table=table_name,
                    data=data,
                    where_clause=where_clause,
                    where_params=where_params,
                )

                msg = "App updated successfully."
                self.notif.show_info_popup(msg)

            # refetch data
            self.load_data()
            self.render_table()

        except Exception as e:
            msg = e
            self.notif.show_error_popup(msg=msg)

        finally:
            self.modal.destroy()

    def render_apps(self):
        # render apps
        if not self.apps_data:
            tk.Label(
                self, text="No data found yet.", justify="center", anchor="center"
            ).pack(fill="both", expand=True)
            return

        header_frm = tk.Frame(self)
        header_frm.pack(side="top", fill="x")

        # title header
        tk.Label(header_frm, text="Monitored Apps", font=("Arial", 12, "bold")).pack(
            anchor="nw", side="left"
        )

        # button tambah / form app
        add_app_btn = tk.Button(
            header_frm, text="Add new app", command=self.app_form_modal
        )
        add_app_btn.pack(side="right")

        tk.Separator(self).pack(pady=10, fill="x", side="top")

        # render table
        self.create_table()

        # render table dengan data
        self.render_table()

    def reset_form(self):
        self.id_text.set(None)
        self.name_text.set("")
        self.type_text.set("port")
        self.value_text.set("")
        self.callback_entry.delete("1.0", END)

        self.modal.destroy()
