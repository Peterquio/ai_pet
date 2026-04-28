import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

janela = tk.Tk()
janela.title("AI Pet - Monitor da Câmera")
janela.geometry("800x600")
janela.configure(bg="#1e1e1e")

# Campo superior
frame_topo = tk.Frame(janela, bg="#1e1e1e")
frame_topo.pack(fill="x", padx=16, pady=12)

label_ip = tk.Label(
    frame_topo,
    text="IP da câmera:",
    bg="#1e1e1e",
    fg="white"
)
label_ip.pack(side="left")

entrada_ip = tk.Entry(frame_topo, width=35)
entrada_ip.insert(0, "http://192.168.4.1")
entrada_ip.pack(side="left", padx=8)

botao_conectar = tk.Button(frame_topo, text="Conectar")
botao_conectar.pack(side="left")

# Status
label_status = tk.Label(
    janela,
    text="Status: Desconectado",
    bg="#1e1e1e",
    fg="#ffcc66",
    anchor="w"
)
label_status.pack(fill="x", padx=16)

# Área da câmera
label_video = tk.Label(
    janela,
    text="Imagem da câmera aparecerá aqui",
    bg="#111111",
    fg="#777777"
)
label_video.pack(fill="both", expand=True, padx=16, pady=16)

janela.mainloop()