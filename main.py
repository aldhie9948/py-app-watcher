from tkinter import ttk as tk, PhotoImage
from src.components.notification import Notification
import threading
from src.components.sidebar import Sidebar
from src.components.content import ContentArea
from ttkthemes import ThemedTk
import pystray
from PIL import Image, ImageDraw
from src.helpers.utils import resource_path

BASE_WINDOW = 360
MIN_WINDOW_WIDTH = BASE_WINDOW * 3
MIN_WINDOW_HEIGHT = BASE_WINDOW * 1

SIDEBAR_WIDTH = 200
WRAP_LENGTH_OFFSET = 50
WRAP_LENGTH = MIN_WINDOW_WIDTH - SIDEBAR_WIDTH - WRAP_LENGTH_OFFSET


class MyApp(ThemedTk):
    def __init__(self):
        super().__init__()
        self.icon_path = resource_path("icon.png")
        self.first_minimize = True
        self.setup_window()
        self.setup_ui()
        self.setup_systray()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        x = round((self.winfo_screenwidth() // 5))
        y = round((self.winfo_screenheight() // 5))
        self.title("MMS App Monitoring")
        self.geometry(f"{MIN_WINDOW_WIDTH}x{MIN_WINDOW_HEIGHT}+{x}+{y}")
        self.notification = Notification(self)

    def on_close(self):
        if self.first_minimize:
            self.notification.show_info_popup(
                "Aplikasi akan berjalan di background.\n\nKlik icon di system tray untuk membuka kembali."
            )
            self.first_minimize = False

        self.hide_window()

    def setup_ui(self):
        # atur icon app
        app_icon_image = PhotoImage(file=self.icon_path)
        self.iconphoto(True, app_icon_image)

        style = tk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#f0f0f0",
            foreground="black",
            rowheight=25,
            fieldbackground="#f0f0f0",
            borderwidth=1,
            bordercolor="gray",
            relief="solid",
        )

        style.configure(
            "Treeview.Heading",
            background="#4caf50",
            foreground="black",
            borderwidth=2,
            relief="raised",  # Atau "solid" untuk flat
            font=("Arial", 10, "bold"),
        )

        style.configure(
            "Treeview",
            fieldbackground="#f0f0f0",
            background="#d0d0d0",  # Warna border antar row
        )

        style.map(
            "Treeview",
            background=[("selected", "#0078d4")],
            foreground=[("selected", "white")],
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#45a049")],
            foreground=[("active", "white")],
            relief=[("active", "sunken")],
        )

        main_frm = tk.Frame(self, padding=20)
        main_frm.pack(fill="both", expand=True)

        # sidebar
        self.sidebar = Sidebar(main_frm, on_menu_click=self.handle_menu)
        self.sidebar.pack(side="left", fill="y")

        # content
        self.content = ContentArea(main_frm)
        self.content.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # default page
        self.content.show_dashboard()

    def setup_systray(self):
        try:
            icon_image = Image.open(self.icon_path)
        except:
            # buat icon sederhana
            icon_image = self.create_icon()

        # menu systray
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window, default=True),
            pystray.MenuItem("Hide", self.hide_window),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.quit_app),
        )

        # buat systray icon
        self.tray_icon = pystray.Icon(
            "MMS Monitor", icon_image, "MMS App Monitoring", menu
        )

        # jalankan systray di thread terpisah
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_icon(self):
        # Buat icon sederhana (lingkaran biru)
        width = 64
        height = 64
        image = Image.new("RGB", (width, height), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.ellipse([10, 10, 54, 54], fill=(0, 120, 215))
        return image

    def show_window(self, icon=None, item=None):
        self.after(0, self._show_window)

    def _show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide_window(self):
        self.withdraw()

    def quit_app(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.quit()

    def handle_menu(self, menu: str):
        value = menu.lower()
        if value == "dashboard":
            self.content.show_dashboard()
        elif value == "apps":
            self.content.show_apps()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
