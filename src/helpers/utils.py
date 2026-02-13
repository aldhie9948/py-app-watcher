import sys, os


def groupby(data: list, key: str):
    from collections import defaultdict

    grouped = defaultdict(list)
    for item in data:
        grouped[item[key]].append(item)
    return dict(grouped)


def resource_path(relative_path):
    """Dapatkan path absolut, baik saat dijalankan biasa atau via PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "src", "static", relative_path)
    return os.path.join(os.path.abspath("."), "src", "static", relative_path)
