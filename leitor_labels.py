import re
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image, ImageTk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


EXTENSOES_IMAGEM = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]


class LeitorLabelsApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AI Pet - Editor de Labels YOLO")
        self.root.geometry("1100x720")
        self.root.resizable(True, True)

        self.pasta_dataset = None
        self.pasta_images = None
        self.pasta_labels = None

        self.imagens = []
        self.indice_atual = 0

        self.imagem_original = None
        self.imagem_tk = None

        self.labels = []
        self.label_selecionada = None

        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

        self.desenhando = False
        self.inicio_x = 0
        self.inicio_y = 0
        self.retangulo_temp = None

        self.nome_label = ctk.StringVar(value="nuvem")
        self.ferramenta = ctk.StringVar(value="selecionar")

        self.criar_ui()

    def criar_ui(self):
        layout = ctk.CTkFrame(self.root, corner_radius=0)
        layout.pack(fill="both", expand=True)

        self.sidebar = ctk.CTkFrame(layout, width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        area = ctk.CTkFrame(layout, corner_radius=0)
        area.pack(side="right", fill="both", expand=True)

        self.criar_sidebar()
        self.criar_area_imagem(area)

    def criar_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text="Editor YOLO",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=18, pady=(18, 4))

        ctk.CTkLabel(
            self.sidebar,
            text="Visualize e corrija labels",
            text_color="gray70"
        ).pack(anchor="w", padx=18, pady=(0, 16))

        ctk.CTkButton(
            self.sidebar,
            text="Abrir pasta dataset",
            height=36,
            command=self.abrir_pasta
        ).pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkLabel(self.sidebar, text="Nome da label").pack(anchor="w", padx=18)

        ctk.CTkEntry(
            self.sidebar,
            textvariable=self.nome_label,
            height=32
        ).pack(fill="x", padx=18, pady=(4, 12))

        ctk.CTkLabel(self.sidebar, text="Ferramenta").pack(anchor="w", padx=18)

        ctk.CTkRadioButton(
            self.sidebar,
            text="Selecionar / mover",
            variable=self.ferramenta,
            value="selecionar"
        ).pack(anchor="w", padx=18, pady=4)

        ctk.CTkRadioButton(
            self.sidebar,
            text="Adicionar caixa",
            variable=self.ferramenta,
            value="adicionar"
        ).pack(anchor="w", padx=18, pady=4)

        ctk.CTkButton(
            self.sidebar,
            text="Excluir label selecionada",
            height=34,
            fg_color="#8a1f1f",
            hover_color="#a82929",
            command=self.excluir_label
        ).pack(fill="x", padx=18, pady=(16, 8))

        ctk.CTkButton(
            self.sidebar,
            text="Salvar alterações",
            height=38,
            command=self.salvar_labels
        ).pack(fill="x", padx=18, pady=(0, 14))

        self.info = ctk.CTkLabel(
            self.sidebar,
            text="Nenhum dataset aberto",
            text_color="gray70",
            justify="left"
        )
        self.info.pack(anchor="w", padx=18, pady=(4, 14))

        ctk.CTkLabel(
            self.sidebar,
            text="Labels da imagem",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=18, pady=(8, 4))

        self.lista_labels = ctk.CTkTextbox(self.sidebar, height=220)
        self.lista_labels.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def criar_area_imagem(self, parent):
        topo = ctk.CTkFrame(parent, height=52)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkButton(
            topo,
            text="◀ Anterior",
            width=110,
            command=self.imagem_anterior
        ).pack(side="left", padx=12, pady=10)

        ctk.CTkButton(
            topo,
            text="Próxima ▶",
            width=110,
            command=self.proxima_imagem
        ).pack(side="left", padx=(0, 12), pady=10)

        self.titulo_imagem = ctk.CTkLabel(
            topo,
            text="Abra uma pasta para começar",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.titulo_imagem.pack(side="left", padx=10)

        self.canvas = ctk.CTkCanvas(
            parent,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.canvas.bind("<ButtonPress-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.root.bind("<Right>", lambda e: self.proxima_imagem())
        self.root.bind("<Left>", lambda e: self.imagem_anterior())
        self.root.bind("<Delete>", lambda e: self.excluir_label())

    def abrir_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta do dataset")

        if not pasta:
            return

        self.pasta_dataset = Path(pasta)
        self.pasta_images = self.pasta_dataset / "images"
        self.pasta_labels = self.pasta_dataset / "labels"

        if not self.pasta_images.exists():
            messagebox.showerror("Erro", "A pasta selecionada não possui subpasta images.")
            return

        self.pasta_labels.mkdir(exist_ok=True)

        self.imagens = [
            img for img in sorted(self.pasta_images.iterdir())
            if img.suffix.lower() in EXTENSOES_IMAGEM
        ]

        if not self.imagens:
            messagebox.showwarning("Atenção", "Nenhuma imagem encontrada em images.")
            return

        self.carregar_nome_label_data_yaml()

        self.indice_atual = 0
        self.carregar_imagem_atual()

    def carregar_nome_label_data_yaml(self):
        data_yaml = self.pasta_dataset / "data.yaml"

        if not data_yaml.exists():
            return

        texto = data_yaml.read_text(encoding="utf-8", errors="ignore")

        resultado = re.search(r"0:\s*(.+)", texto)

        if resultado:
            self.nome_label.set(resultado.group(1).strip())

    def carregar_imagem_atual(self):
        if not self.imagens:
            return

        caminho = self.imagens[self.indice_atual]
        self.imagem_original = Image.open(caminho).convert("RGB")

        self.carregar_labels(caminho)
        self.desenhar_imagem()

        self.titulo_imagem.configure(
            text=f"{self.indice_atual + 1}/{len(self.imagens)} - {caminho.name}"
        )

        self.atualizar_info()
        self.atualizar_lista_labels()

    def carregar_labels(self, caminho_imagem):
        self.labels.clear()
        self.label_selecionada = None

        caminho_label = self.pasta_labels / f"{caminho_imagem.stem}.txt"

        if not caminho_label.exists():
            return

        linhas = caminho_label.read_text(encoding="utf-8").splitlines()

        largura, altura = self.imagem_original.size

        for linha in linhas:
            partes = linha.strip().split()

            if len(partes) != 5:
                continue

            classe, xc, yc, bw, bh = partes

            xc = float(xc) * largura
            yc = float(yc) * altura
            bw = float(bw) * largura
            bh = float(bh) * altura

            x1 = xc - bw / 2
            y1 = yc - bh / 2
            x2 = xc + bw / 2
            y2 = yc + bh / 2

            self.labels.append({
                "classe": int(classe),
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })

    def desenhar_imagem(self):
        self.canvas.delete("all")

        if self.imagem_original is None:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w <= 1 or canvas_h <= 1:
            self.root.after(100, self.desenhar_imagem)
            return

        img_w, img_h = self.imagem_original.size

        self.scale = min(canvas_w / img_w, canvas_h / img_h)

        novo_w = int(img_w * self.scale)
        novo_h = int(img_h * self.scale)

        self.offset_x = (canvas_w - novo_w) // 2
        self.offset_y = (canvas_h - novo_h) // 2

        imagem_redimensionada = self.imagem_original.resize((novo_w, novo_h))
        self.imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

        self.canvas.create_image(
            self.offset_x,
            self.offset_y,
            anchor="nw",
            image=self.imagem_tk
        )

        self.desenhar_labels()

    def desenhar_labels(self):
        for i, label in enumerate(self.labels):
            x1, y1 = self.img_para_canvas(label["x1"], label["y1"])
            x2, y2 = self.img_para_canvas(label["x2"], label["y2"])

            cor = "#00ff66" if i == self.label_selecionada else "#1f6aa5"
            largura = 3 if i == self.label_selecionada else 2

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=cor,
                width=largura,
                tags=f"label_{i}"
            )

            self.canvas.create_text(
                x1 + 4,
                y1 + 4,
                anchor="nw",
                text=self.nome_label.get(),
                fill=cor,
                font=("Arial", 12, "bold")
            )

    def img_para_canvas(self, x, y):
        return (
            self.offset_x + x * self.scale,
            self.offset_y + y * self.scale
        )

    def canvas_para_img(self, x, y):
        return (
            (x - self.offset_x) / self.scale,
            (y - self.offset_y) / self.scale
        )

    def mouse_down(self, event):
        if self.imagem_original is None:
            return

        if self.ferramenta.get() == "adicionar":
            self.desenhando = True
            self.inicio_x = event.x
            self.inicio_y = event.y

            self.retangulo_temp = self.canvas.create_rectangle(
                event.x,
                event.y,
                event.x,
                event.y,
                outline="#ffaa00",
                width=2
            )

        else:
            self.selecionar_label(event.x, event.y)

    def mouse_drag(self, event):
        if not self.desenhando or self.retangulo_temp is None:
            return

        self.canvas.coords(
            self.retangulo_temp,
            self.inicio_x,
            self.inicio_y,
            event.x,
            event.y
        )

    def mouse_up(self, event):
        if not self.desenhando:
            return

        self.desenhando = False

        if self.retangulo_temp:
            self.canvas.delete(self.retangulo_temp)
            self.retangulo_temp = None

        x1 = min(self.inicio_x, event.x)
        y1 = min(self.inicio_y, event.y)
        x2 = max(self.inicio_x, event.x)
        y2 = max(self.inicio_y, event.y)

        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            return

        ix1, iy1 = self.canvas_para_img(x1, y1)
        ix2, iy2 = self.canvas_para_img(x2, y2)

        largura, altura = self.imagem_original.size

        ix1 = max(0, min(ix1, largura))
        ix2 = max(0, min(ix2, largura))
        iy1 = max(0, min(iy1, altura))
        iy2 = max(0, min(iy2, altura))

        self.labels.append({
            "classe": 0,
            "x1": ix1,
            "y1": iy1,
            "x2": ix2,
            "y2": iy2
        })

        self.label_selecionada = len(self.labels) - 1
        self.desenhar_imagem()
        self.atualizar_lista_labels()

    def selecionar_label(self, x, y):
        ix, iy = self.canvas_para_img(x, y)

        self.label_selecionada = None

        for i, label in enumerate(self.labels):
            if label["x1"] <= ix <= label["x2"] and label["y1"] <= iy <= label["y2"]:
                self.label_selecionada = i
                break

        self.desenhar_imagem()
        self.atualizar_lista_labels()

    def excluir_label(self):
        if self.label_selecionada is None:
            messagebox.showwarning("Atenção", "Nenhuma label selecionada.")
            return

        del self.labels[self.label_selecionada]
        self.label_selecionada = None

        self.desenhar_imagem()
        self.atualizar_lista_labels()

    def salvar_labels(self):
        if self.imagem_original is None:
            return

        caminho_imagem = self.imagens[self.indice_atual]
        caminho_label = self.pasta_labels / f"{caminho_imagem.stem}.txt"

        largura, altura = self.imagem_original.size
        linhas = []

        for label in self.labels:
            x1 = label["x1"]
            y1 = label["y1"]
            x2 = label["x2"]
            y2 = label["y2"]

            xc = ((x1 + x2) / 2) / largura
            yc = ((y1 + y2) / 2) / altura
            bw = (x2 - x1) / largura
            bh = (y2 - y1) / altura

            linhas.append(f"0 {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

        caminho_label.write_text("\n".join(linhas), encoding="utf-8")
        self.salvar_data_yaml()

        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

    def salvar_data_yaml(self):
        data_yaml = self.pasta_dataset / "data.yaml"

        conteudo = f"""path: {self.pasta_dataset.as_posix()}
train: images
val: images

names:
  0: {self.nome_label.get().strip()}
"""

        data_yaml.write_text(conteudo, encoding="utf-8")

    def atualizar_lista_labels(self):
        self.lista_labels.delete("1.0", "end")

        if not self.labels:
            self.lista_labels.insert("end", "Nenhuma label nesta imagem.")
            return

        for i, label in enumerate(self.labels):
            selecionada = " ← selecionada" if i == self.label_selecionada else ""
            texto = (
                f"{i + 1}. {self.nome_label.get()}{selecionada}\n"
                f"   x1={label['x1']:.0f}, y1={label['y1']:.0f}\n"
                f"   x2={label['x2']:.0f}, y2={label['y2']:.0f}\n\n"
            )
            self.lista_labels.insert("end", texto)

    def atualizar_info(self):
        if not self.imagens:
            self.info.configure(text="Nenhum dataset aberto")
            return

        self.info.configure(
            text=(
                f"Dataset:\n{self.pasta_dataset}\n\n"
                f"Imagens: {len(self.imagens)}\n"
                f"Imagem atual: {self.indice_atual + 1}"
            )
        )

    def proxima_imagem(self):
        if not self.imagens:
            return

        self.indice_atual += 1

        if self.indice_atual >= len(self.imagens):
            self.indice_atual = 0

        self.carregar_imagem_atual()

    def imagem_anterior(self):
        if not self.imagens:
            return

        self.indice_atual -= 1

        if self.indice_atual < 0:
            self.indice_atual = len(self.imagens) - 1

        self.carregar_imagem_atual()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LeitorLabelsApp()
    app.run()