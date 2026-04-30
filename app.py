import subprocess
import sys
from pathlib import Path

import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


BASE_DIR = Path(__file__).resolve().parent


MODULOS = {
    "anotador_yolo": BASE_DIR / "anotador_yolo.py",
    "camera_monitor": BASE_DIR / "camera_monitor.py",
    "configurar_camera": BASE_DIR / "configurar_camera.py",
    "leitor_labels": BASE_DIR / "leitor_labels.py",
}


class AIPetApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AI Pet")
        self.root.geometry("760x520")
        self.root.minsize(720, 480)

        self.criar_interface()

    def criar_interface(self):
        container = ctk.CTkFrame(self.root, corner_radius=22)
        container.pack(fill="both", expand=True, padx=24, pady=24)

        titulo = ctk.CTkLabel(
            container,
            text="AI Pet",
            font=ctk.CTkFont(size=34, weight="bold")
        )
        titulo.pack(anchor="w", padx=28, pady=(28, 4))

        subtitulo = ctk.CTkLabel(
            container,
            text="Central de monitoramento, câmera e ferramentas YOLO",
            font=ctk.CTkFont(size=15),
            text_color="gray70"
        )
        subtitulo.pack(anchor="w", padx=28, pady=(0, 28))

        grid = ctk.CTkFrame(container, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        grid.grid_columnconfigure((0, 1), weight=1)
        grid.grid_rowconfigure((0, 1), weight=1)

        self.criar_card(
            grid,
            linha=0,
            coluna=0,
            titulo="Monitor da Câmera",
            descricao="Abrir transmissão da ESP32-CAM em tempo real.",
            botao="Abrir câmera",
            modulo="camera_monitor"
        )

        self.criar_card(
            grid,
            linha=0,
            coluna=1,
            titulo="Configurar Câmera",
            descricao="Alterar Wi-Fi e configurações da ESP32-CAM.",
            botao="Configurar",
            modulo="configurar_camera"
        )

        self.criar_card(
            grid,
            linha=1,
            coluna=0,
            titulo="Anotador YOLO",
            descricao="Criar ou ajustar marcações para treinamento da IA.",
            botao="Abrir anotador",
            modulo="anotador_yolo"
        )

        self.criar_card(
            grid,
            linha=1,
            coluna=1,
            titulo="Leitor de Labels",
            descricao="Visualizar imagens e arquivos .txt no padrão YOLO.",
            botao="Abrir labels",
            modulo="leitor_labels"
        )

        rodape = ctk.CTkLabel(
            container,
            text="AI Pet • ESP32-CAM • YOLO • Python",
            text_color="gray55",
            font=ctk.CTkFont(size=12)
        )
        rodape.pack(pady=(0, 18))

    def criar_card(self, parent, linha, coluna, titulo, descricao, botao, modulo):
        card = ctk.CTkFrame(parent, corner_radius=18)
        card.grid(row=linha, column=coluna, sticky="nsew", padx=10, pady=10)

        label_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        label_titulo.pack(fill="x", padx=20, pady=(20, 6))

        label_descricao = ctk.CTkLabel(
            card,
            text=descricao,
            font=ctk.CTkFont(size=13),
            text_color="gray70",
            anchor="w",
            justify="left",
            wraplength=260
        )
        label_descricao.pack(fill="x", padx=20, pady=(0, 18))

        botao_abrir = ctk.CTkButton(
            card,
            text=botao,
            height=40,
            command=lambda: self.abrir_modulo(modulo)
        )
        botao_abrir.pack(fill="x", padx=20, pady=(0, 20))

    def abrir_modulo(self, nome_modulo):
        caminho_modulo = MODULOS.get(nome_modulo)

        if caminho_modulo is None or not caminho_modulo.exists():
            self.mostrar_erro(f"Arquivo não encontrado:\n{caminho_modulo}")
            return

        try:
            subprocess.Popen([sys.executable, str(caminho_modulo)])
        except Exception as erro:
            self.mostrar_erro(f"Não foi possível abrir o módulo:\n{erro}")

    def mostrar_erro(self, mensagem):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Erro")
        janela.geometry("420x180")
        janela.resizable(False, False)
        janela.grab_set()

        label = ctk.CTkLabel(
            janela,
            text=mensagem,
            wraplength=360,
            justify="center"
        )
        label.pack(expand=True, padx=24, pady=20)

        botao = ctk.CTkButton(
            janela,
            text="Fechar",
            command=janela.destroy
        )
        botao.pack(pady=(0, 20))

    def executar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIPetApp()
    app.executar()