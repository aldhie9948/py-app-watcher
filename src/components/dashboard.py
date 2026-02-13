from tkinter import ttk as tk
from src.helpers.check_utils import execute_callback
from src.helpers.database import Database
from src.helpers.stoppable_thread import StoppableThread
from src.helpers.check_utils import check_proccess, check_website, check_port
from src.components.notification import Notification


class Dashboard(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.monitor_thread = StoppableThread()
        self.apps_data = []
        self.load_data()
        self.setup_ui()

    def setup_ui(self):
        self.config()
        self.notif = Notification(self)
        self.render_page()

    def load_data(self):
        self.db = Database()
        self.apps_data = self.db.fetch_all("SELECT * FROM apps ORDER BY type ASC")

    def create_table(self):
        table_frm = tk.Frame(self)
        table_frm.pack(fill="both", expand=True)

        y_scroll = tk.Scrollbar(table_frm, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frm, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        columns = ("id", "name", "type", "target", "status")
        self.table = tk.Treeview(
            table_frm,
            columns=columns,
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
        )

        for col in columns:
            self.table.heading(col, text=col.capitalize())

        self.table.column("id", width=30, anchor="center")
        self.table.column("name", width=200, anchor="w")
        self.table.column("type", width=50, anchor="center")
        self.table.column("target", width=200, anchor="w")
        self.table.column("status", width=50, anchor="center")

        self.table.pack(fill="both", expand=True)

        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)

        # load data
        self.load_data_table()

    def create_header(self):
        header_frm = tk.Frame(self)
        header_frm.pack(side="top", fill="x")
        tk.Label(header_frm, text="Monitoring Status", font=("Arial", 12, "bold")).pack(
            side="left", fill="x"
        )
        start_btn = tk.Button(header_frm, command=self.start_monitoring, text="Start")
        stop_btn = tk.Button(header_frm, command=self.stop_monitoring, text="Stop")

        stop_btn.pack(side="right")
        start_btn.pack(side="right", padx=10)

    def load_data_table(self):
        status_apps: list[dict[str, any]] = []
        # input data
        for item in self.table.get_children():
            self.table.delete(item)

        for app in self.apps_data:
            result = self.check_status(app)
            status_apps.append(result)
            self.table.insert(
                "",
                "end",
                values=(
                    app["id"],
                    app["name"],
                    app["type"],
                    app["value"],
                    "⭕" if result["status"] else "❌",
                ),
            )

        return status_apps

    def check_status(self, app: dict[str, any]):
        result = False
        type = app["type"]
        target = app["value"]
        callback = app["callback"]

        if type == "port":
            result = check_port(target)
        elif type == "process":
            result = check_proccess(target)
        elif type == "url":
            result = check_website(target)

        return {"status": result, "callback": callback}

    def task_monitoring(self, stop_flag, interval=5):
        while not stop_flag.is_set():
            print("Task monitoring running...")
            apps = self.load_data_table()
            for app in apps:
                status = app["status"]
                callback = app["callback"]

                if status:
                    continue
                elif not status and callback:
                    execute_callback(callback)

            if stop_flag.wait(timeout=interval):
                break
        print("Task monitoring stopped.")

    def start_monitoring(self):
        if self.monitor_thread.start(self.task_monitoring, interval=5):
            print("Monitoring started.")
        else:
            self.notif.show_info_popup("Monitoring already running.")

    def stop_monitoring(self):
        self.monitor_thread.stop()
        print("Monitoring stopped")

    def render_page(self):
        if not self.apps_data:
            label = tk.Label(self, text="No data found yet.", justify="center")
            label.pack(fill="both", expand=True)
            return

        self.create_header()
        tk.Separator(self, orient="horizontal").pack(pady=10, fill="x")
        self.create_table()
        self.start_monitoring()
