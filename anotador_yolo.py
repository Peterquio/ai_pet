import shutil
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from ultralytics import YOLO

from ui.aviso_yolo import exibir_aviso_yolo


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


ANIMAIS = {
    "Pessoa": 0,
    "Pássaro": 14,
    "Gato": 15,
    "Cachorro": 16,
    "Cavalo": 17,
    "Ovelha": 18,
    "Vaca": 19,
    "Elefante": 20,
    "Urso": 21,
    "Zebra": 22,
    "Girafa": 23,
    "Todos": None
}

CLASSES_ANIMAIS = [14,15,16,17,18,19,20,21,22,23]


class App:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AI Pet - Anotador")
        self.root.geometry("620x700")

        self.pasta = ctk.StringVar()
        self.modelo = ctk.StringVar(value="yolov8n.pt")
        self.label = ctk.StringVar(value="nuvem")
        self.conf = ctk.DoubleVar(value=0.45)
        self.salvar_vazio = ctk.BooleanVar()

        self.cor_label = ctk.StringVar(value="#00ff66")
        self.animal = "Gato"
        self.nao_mostrar_aviso = False

        self.botoes = {}

        self.ui()

    def ui(self):
        c = ctk.CTkFrame(self.root, corner_radius=12)
        c.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(c, text="Anotador YOLO", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(10, 4))
        ctk.CTkLabel(c, text="Gera dataset automaticamente", text_color="gray70").pack(anchor="w", pady=(0, 12))

        self.campo_pasta(c)

        self.input(c, "Modelo YOLO", self.modelo)
        self.input(c, "Nome da label", self.label)

        ctk.CTkLabel(c, text="Cor da label").pack(anchor="w")
        ctk.CTkEntry(c, textvariable=self.cor_label, height=32).pack(fill="x", pady=(4, 8))

        ctk.CTkLabel(c, text="Confiança").pack(anchor="w")
        self.lbl_conf = ctk.CTkLabel(c, text="0.45", text_color="gray70")
        self.lbl_conf.pack(anchor="w")

        ctk.CTkSlider(c, from_=0.1, to=0.9, variable=self.conf, command=self.atualizar_conf).pack(fill="x", pady=(4, 8))

        self.grid_animais(c)

        ctk.CTkCheckBox(c, text="Salvar txt vazio", variable=self.salvar_vazio).pack(anchor="w", pady=(4, 8))

        self.log = ctk.CTkTextbox(c, height=120)
        self.log.pack(fill="both", expand=True, pady=(4, 8))

        self.lbl_prog = ctk.CTkLabel(c, text="0 / 0", text_color="gray70")
        self.lbl_prog.pack(anchor="w")

        self.barra = ctk.CTkProgressBar(c)
        self.barra.set(0)
        self.barra.pack(fill="x", pady=(4, 8))

        ctk.CTkButton(c, text="Gerar anotações YOLO", height=36, command=self.iniciar).pack(fill="x")

    def campo_pasta(self, parent):
        ctk.CTkLabel(parent, text="Pasta dataset").pack(anchor="w")

        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=(4, 8))

        ctk.CTkEntry(f, textvariable=self.pasta, height=32).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(f, text="Selecionar", width=100, height=32, command=self.sel_pasta).pack(side="right")

    def input(self, parent, txt, var):
        ctk.CTkLabel(parent, text=txt).pack(anchor="w")
        ctk.CTkEntry(parent, textvariable=var, height=32).pack(fill="x", pady=(4, 8))

    def grid_animais(self, parent):
        ctk.CTkLabel(parent, text="Detectar").pack(anchor="w")

        g = ctk.CTkFrame(parent, fg_color="transparent")
        g.pack(fill="x", pady=(4, 8))

        nomes = list(ANIMAIS.keys())

        for i, nome in enumerate(nomes):
            r = i // 4
            col = i % 4

            b = ctk.CTkButton(
                g,
                text=nome,
                height=28,
                fg_color="#1f6aa5" if nome == self.animal else "#2b2b2b",
                command=lambda n=nome: self.sel_animal(n)
            )
            b.grid(row=r, column=col, padx=4, pady=4, sticky="ew")
            g.grid_columnconfigure(col, weight=1)

            self.botoes[nome] = b

    def sel_animal(self, nome):
        self.animal = nome
        for n, b in self.botoes.items():
            b.configure(fg_color="#1f6aa5" if n == nome else "#2b2b2b")

    def atualizar_conf(self, v):
        self.lbl_conf.configure(text=f"{float(v):.2f}")

    def sel_pasta(self):
        p = filedialog.askdirectory()
        if p:
            self.pasta.set(p)

    def log_add(self, t):
        self.log.insert("end", t + "\n")
        self.log.see("end")

    def iniciar(self):
        if not self.pasta.get():
            messagebox.showwarning("Erro", "Selecione a pasta")
            return

        if not self.nao_mostrar_aviso:
            self.nao_mostrar_aviso = exibir_aviso_yolo(self.root)

        threading.Thread(target=self.processar, daemon=True).start()

    def organizar(self, base):
        img = base / "images"
        lbl = base / "labels"

        img.mkdir(exist_ok=True)
        lbl.mkdir(exist_ok=True)

        exts = [".jpg",".png",".jpeg",".bmp",".webp"]

        for f in base.iterdir():
            if f.is_file() and f.suffix.lower() in exts:
                shutil.move(str(f), str(img / f.name))

        imgs = []
        for e in exts:
            imgs.extend(img.glob(f"*{e}"))

        return img, lbl, sorted(imgs)

    def classes(self):
        c = ANIMAIS[self.animal]
        return CLASSES_ANIMAIS if c is None else [c]

    def processar(self):
        base = Path(self.pasta.get())

        img_dir, lbl_dir, imgs = self.organizar(base)

        if not imgs:
            self.log_add("Sem imagens")
            return

        model = YOLO(self.modelo.get())
        classes = self.classes()

        total = len(imgs)

        for i, im in enumerate(imgs, start=1):
            res = model(str(im), conf=self.conf.get(), verbose=False)[0]

            h, w = res.orig_shape

            linhas = []

            for box in res.boxes:
                if int(box.cls[0]) not in classes:
                    continue

                x1,y1,x2,y2 = box.xyxy[0].tolist()

                xc = ((x1+x2)/2)/w
                yc = ((y1+y2)/2)/h
                bw = (x2-x1)/w
                bh = (y2-y1)/h

                linhas.append(f"0 {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

            arq = lbl_dir / f"{im.stem}.txt"

            if linhas:
                arq.write_text("\n".join(linhas))
                self.log_add(f"OK {im.name}")
            elif self.salvar_vazio.get():
                arq.write_text("")
                self.log_add(f"VAZIO {im.name}")

            self.barra.set(i/total)
            self.lbl_prog.configure(text=f"{i} / {total}")

        (base / "data.yaml").write_text(
            f"""path: {base.as_posix()}
        train: images
        val: images

        names:
          0: {self.label.get().strip()}

        colors:
          0: "{self.cor_label.get().strip()}"
        """,
            encoding="utf-8"
        )

        messagebox.showinfo("Sucesso", f"Finalizado!\n{total} imagens processadas")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()