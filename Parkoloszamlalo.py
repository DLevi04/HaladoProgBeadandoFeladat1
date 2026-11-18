import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO

SOROK_SZAMA = 9
OSZLOPOK_SZAMA = 2

JARMU_OSZTALYOK = {
    2: "Auto",
    3: "Motor",
    5: "Busz",
    7: "Teherauto"
}

parkolohelyek = []
huzas_folyamatban = False
kezdo_x, kezdo_y = -1, -1
aktualis_x, aktualis_y = -1, -1


def kep_valasztasa():
    root = tk.Tk()
    root.withdraw()
    utvonal = filedialog.askopenfilename(
        title="Valassz ki egy kepet a parkolorol!",
        filetypes=[("Kepek", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    root.destroy()
    return utvonal


def eger_esemeny(event, x, y, flags, param):
    global huzas_folyamatban, kezdo_x, kezdo_y, aktualis_x, aktualis_y, parkolohelyek

    if event == cv2.EVENT_LBUTTONDOWN:
        huzas_folyamatban = True
        kezdo_x, kezdo_y = x, y
        aktualis_x, aktualis_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if huzas_folyamatban:
            aktualis_x, aktualis_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        huzas_folyamatban = False
        x1, x2 = min(kezdo_x, x), max(kezdo_x, x)
        y1, y2 = min(kezdo_y, y), max(kezdo_y, y)

        if (x2 - x1) > 20 and (y2 - y1) > 20:
            szelesseg = (x2 - x1) / OSZLOPOK_SZAMA
            magassag = (y2 - y1) / SOROK_SZAMA
            for r in range(SOROK_SZAMA):
                for c in range(OSZLOPOK_SZAMA):
                    hx1 = int(x1 + c * szelesseg)
                    hy1 = int(y1 + r * magassag)
                    hx2 = int(x1 + (c + 1) * szelesseg)
                    hy2 = int(y1 + (r + 1) * magassag)
                    parkolohelyek.append((hx1, hy1, hx2, hy2))

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(parkolohelyek) >= SOROK_SZAMA * OSZLOPOK_SZAMA:
            del parkolohelyek[-(SOROK_SZAMA * OSZLOPOK_SZAMA):]


