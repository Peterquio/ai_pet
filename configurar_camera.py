import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def criar_card_rede(parent, ssid, rssi, protegida=False, selecionada=False):
    cor_card = "#1f6aa5" if selecionada else "#2b2b2b"

    card = ctk.CTkFrame(parent, corner_radius=14, fg_color=cor_card)
    card.pack(fill="x", padx=8, pady=6)

    linha = ctk.CTkFrame(card, fg_color="transparent")
    linha.pack(fill="x", padx=14, pady=12)

    nivel = calcular_nivel_sinal(rssi)

    icone = ctk.CTkLabel(
        linha,
        text=montar_icone_wifi(nivel),
        font=ctk.CTkFont(size=22)
    )
    icone.pack(side="left", padx=(0, 12))

    bloco_texto = ctk.CTkFrame(linha, fg_color="transparent")
    bloco_texto.pack(side="left", fill="x", expand=True)

    nome = ctk.CTkLabel(
        bloco_texto,
        text=ssid,
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    )
    nome.pack(anchor="w")

    detalhe = "Rede protegida" if protegida else "Rede aberta"

    info = ctk.CTkLabel(
        bloco_texto,
        text=f"{detalhe} • {rssi} dBm",
        font=ctk.CTkFont(size=12),
        text_color="gray75",
        anchor="w"
    )
    info.pack(anchor="w", pady=(2, 0))

    cadeado = "🔒" if protegida else "🔓"

    seguranca = ctk.CTkLabel(
        linha,
        text=cadeado,
        font=ctk.CTkFont(size=18)
    )
    seguranca.pack(side="right")

    return card

def calcular_nivel_sinal(rssi):
    if rssi >= -55:
        return 4
    elif rssi >= -67:
        return 3
    elif rssi >= -75:
        return 2
    else:
        return 1

def montar_icone_wifi(nivel):
    if nivel == 4:
        return "▂▄▆█"
    elif nivel == 3:
        return "▂▄▆_"
    elif nivel == 2:
        return "▂▄__"
    else:
        return "▂___"

def criar_janela():
    janela = ctk.CTk()
    janela.title("AI Pet - Configurar Câmera")
    janela.geometry("460x620")
    janela.resizable(False, False)

    container = ctk.CTkFrame(janela, corner_radius=18)
    container.pack(fill="both", expand=True, padx=18, pady=18)

    titulo = ctk.CTkLabel(
        container,
        text="Configurar Wi-Fi",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.pack(anchor="w", padx=22, pady=(22, 4))

    subtitulo = ctk.CTkLabel(
        container,
        text="Escolha a rede que a ESP32-CAM deve usar",
        font=ctk.CTkFont(size=13),
        text_color="gray70"
    )
    subtitulo.pack(anchor="w", padx=22, pady=(0, 18))

    ip_label = ctk.CTkLabel(container, text="IP da câmera em modo configuração")
    ip_label.pack(anchor="w", padx=22)

    entrada_ip = ctk.CTkEntry(container, height=38)
    entrada_ip.insert(0, "192.168.4.1")
    entrada_ip.pack(fill="x", padx=22, pady=(6, 14))

    botao_buscar = ctk.CTkButton(
        container,
        text="Buscar redes próximas",
        height=42
    )
    botao_buscar.pack(fill="x", padx=22, pady=(0, 16))

    lista_redes = ctk.CTkScrollableFrame(
        container,
        height=260,
        corner_radius=14
    )
    lista_redes.pack(fill="both", expand=False, padx=22, pady=(0, 16))

    #criar_card_rede(lista_redes, "MinhaCasa_5G", -48, True)
    #criar_card_rede(lista_redes, "AI_PET_CONFIG", -52, False, selecionada=True)
    #criar_card_rede(lista_redes, "Vivo-1234", -70, True)
    #criar_card_rede(lista_redes, "Rede_Fraca", -82, True)

    senha_label = ctk.CTkLabel(container, text="Senha da rede selecionada")
    senha_label.pack(anchor="w", padx=22)

    entrada_senha = ctk.CTkEntry(container, height=38, show="*")
    entrada_senha.pack(fill="x", padx=22, pady=(6, 14))

    botao_conectar = ctk.CTkButton(
        container,
        text="Conectar câmera",
        height=44
    )
    botao_conectar.pack(fill="x", padx=22, pady=(0, 12))

    status = ctk.CTkLabel(
        container,
        text="Aguardando busca de redes...",
        text_color="gray70"
    )
    status.pack(anchor="w", padx=22, pady=(0, 14))

    janela.mainloop()


if __name__ == "__main__":
    criar_janela()