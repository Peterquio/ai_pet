import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def criar_janela():
    janela = ctk.CTk()
    janela.title("AI Pet - Monitor da Câmera")
    janela.geometry("860x640")
    janela.resizable(False, False)

    container = ctk.CTkFrame(janela, corner_radius=18)
    container.pack(fill="both", expand=True, padx=18, pady=18)

    titulo = ctk.CTkLabel(
        container,
        text="Monitor da Câmera",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.pack(anchor="w", padx=22, pady=(22, 4))

    subtitulo = ctk.CTkLabel(
        container,
        text="Visualização em tempo real da ESP32-CAM",
        font=ctk.CTkFont(size=13),
        text_color="gray70"
    )
    subtitulo.pack(anchor="w", padx=22, pady=(0, 18))

    ip_label = ctk.CTkLabel(container, text="Endereço da câmera")
    ip_label.pack(anchor="w", padx=22)

    linha_conexao = ctk.CTkFrame(container, fg_color="transparent")
    linha_conexao.pack(fill="x", padx=22, pady=(6, 14))

    entrada_ip = ctk.CTkEntry(linha_conexao, height=38)
    entrada_ip.insert(0, "http://192.168.4.1")
    entrada_ip.pack(side="left", fill="x", expand=True, padx=(0, 10))

    botao_conectar = ctk.CTkButton(
        linha_conexao,
        text="Conectar",
        width=140,
        height=38
    )
    botao_conectar.pack(side="right")

    linha_config = ctk.CTkFrame(container, fg_color="transparent")
    linha_config.pack(fill="x", padx=22, pady=(0, 12))

    label_res = ctk.CTkLabel(
        linha_config,
        text="Resolução:"
    )
    label_res.pack(side="left")

    combobox_res = ctk.CTkComboBox(
        linha_config,
        values=[
            "UXGA (1600x1200)",
            "SXGA (1280x1024)",
            "XGA (1024x768)",
            "SVGA (800x600)",
            "VGA (640x480)",
            "CIF (352x288)",
            "QVGA (320x240)"
        ],
        width=200
    )
    combobox_res.set("VGA (640x480)")
    combobox_res.pack(side="right")

    status = ctk.CTkLabel(
        container,
        text="Status: aguardando conexão...",
        text_color="gray70"
    )
    status.pack(anchor="w", padx=22, pady=(0, 14))

    frame_video = ctk.CTkFrame(
        container,
        corner_radius=16,
        fg_color="#111111"
    )
    frame_video.pack(fill="both", expand=True, padx=22, pady=(0, 22))

    label_video = ctk.CTkLabel(
        frame_video,
        text="Preview da câmera",
        text_color="gray50"
    )
    label_video.pack(fill="both", expand=True, padx=10, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()