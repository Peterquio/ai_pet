import customtkinter as ctk


def exibir_aviso_yolo(parent):
    janela = ctk.CTkToplevel(parent)
    janela.title("Aviso")
    janela.geometry("380x220")
    janela.resizable(False, False)
    janela.grab_set()

    container = ctk.CTkFrame(janela, corner_radius=12)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    titulo = ctk.CTkLabel(
        container,
        text="Aviso",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    titulo.pack(anchor="w", padx=12, pady=(12, 4))

    texto = ctk.CTkLabel(
        container,
        text="",
        text_color="gray70"
    )
    texto.pack(anchor="w", padx=12, pady=(0, 12))

    nao_mostrar = ctk.BooleanVar(value=False)

    check = ctk.CTkCheckBox(
        container,
        text="Não mostrar novamente",
        variable=nao_mostrar
    )
    check.pack(anchor="w", padx=12, pady=(0, 12))

    botao = ctk.CTkButton(
        container,
        text="OK",
        height=32,
        command=janela.destroy
    )
    botao.pack(fill="x", padx=12, pady=(0, 12))

    janela.wait_window()
    return nao_mostrar.get()