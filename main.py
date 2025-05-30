import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import signal
import time
import os
import datetime
import customtkinter as ctk
from tkinter import filedialog


pasta_destino = ""
processo_download = None  # global

def escolher_pasta():
    global pasta_destino
    caminho = filedialog.askdirectory(title="Escolha a pasta para salvar o download")
    if caminho:
        pasta_destino = caminho
        label_pasta.configure(text=f"Pasta de download: {pasta_destino}")

def verificar_link():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Digite um link.")
        return

    try:
        resultado = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True)

        saida_texto.delete(1.0, tk.END)

        if "Unsupported URL" in resultado.stdout or "ERROR" in resultado.stderr:
            saida_texto.insert(tk.END, "⚠️ Link não suportado ou fora do ar.")
        else:
            saida_texto.insert(tk.END, resultado.stdout)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def download_thread(url, formato):
    global processo_download
    status_label.configure(text="Download em andamento...", fg_color="red")
    
    # Gerar timestamp detalhado para nome único
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Define o template de saída com timestamp para evitar sobrescrever
    nome_arquivo = os.path.join(pasta_destino, f"%(title)s_{timestamp}.%(ext)s")
    

    comando = ["yt-dlp", "-f", formato, "-o", nome_arquivo, url]

    # criação do processo em novo grupo para receber CTRL+C
    processo_download = subprocess.Popen(
        comando, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    saida_texto.insert(tk.END, "\nIniciando download...\n")
    saida_texto.see(tk.END)

    for linha in processo_download.stdout:
        saida_texto.insert(tk.END, linha)
        saida_texto.see(tk.END)

    processo_download.wait()

    if processo_download.returncode == 0:
        saida_texto.insert(tk.END, "\nDownload finalizado.\n")
    else:
        saida_texto.insert(tk.END, "\nDownload interrompido.\n")

    processo_download = None
    status_label.configure(text="Pronto", fg_color="green")

def baixar_video():
    url = entrada_url.get().strip()
    formato = entrada_formato.get().strip()

    if not url or not formato:
        messagebox.showwarning("Aviso", "Digite o link e o código do formato.")
        return

    thread = threading.Thread(target=download_thread, args=(url, formato), daemon=True)
    thread.start()

def parar_download():
    global processo_download
    if processo_download:
        try:
            # Envia CTRL+C para o grupo de processos do yt-dlp
            processo_download.send_signal(signal.CTRL_BREAK_EVENT)  
            saida_texto.insert(tk.END, "\nTentando parar o download...\n")
            status_label.configure(text="Parando download...", fg_color="orange")
            time.sleep(1)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar parar: {str(e)}")
    else:
        messagebox.showinfo("Info", "Nenhum download em andamento.")

# --- Interface ---


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

janela = ctk.CTk()
janela.title("LVK Media Downloader")
janela.geometry("1000x650") # largura x altura
janela.minsize(1000, 650)
janela.iconbitmap(r"D:/Minhas pastas/Projetos/Meus projetos/lvkMD/media/5D.ico") # se for ico

# Fonte personalizada para labels, botões e entradas, negrito
FONT_BOLD = ("Segoe UI", 12, "bold")

frame_top = ctk.CTkFrame(janela, fg_color="#222222", corner_radius=10)
frame_top.pack(fill=tk.X, padx=15, pady=(15, 5))


status_label = ctk.CTkLabel(
    frame_top,
    text="Pronto",
    fg_color="green",
    text_color="white",
    width=170,
    height=30,
    corner_radius=6,
    font=FONT_BOLD
)
status_label.pack(side=tk.RIGHT, padx=10)

label_url = ctk.CTkLabel(frame_top, text="URL da transmissão ou vídeo:", font=FONT_BOLD)
label_url.pack(side=tk.LEFT, padx=10)

entrada_url = ctk.CTkEntry(frame_top, font=FONT_BOLD)
entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

botao_verificar = ctk.CTkButton(
    frame_top,
    text="Verificar Link",
    width=130,
    font=FONT_BOLD,
    fg_color="#0078D7",
    hover_color="#005A9E",
    border_width=2,
    border_color="#004578",
    command=verificar_link
)
botao_verificar.pack(side=tk.LEFT, padx=10)

frame_meio = ctk.CTkFrame(janela, fg_color="#222222", corner_radius=10)
frame_meio.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

saida_texto = scrolledtext.ScrolledText(frame_meio, wrap=tk.WORD, font=FONT_BOLD)
saida_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_baixar = ctk.CTkFrame(janela, fg_color="#222222", corner_radius=10)
frame_baixar.pack(fill=tk.X, padx=15, pady=(5, 15))

label_formato = ctk.CTkLabel(frame_baixar, text="Código do formato (ex: 22, 137, 140):", font=FONT_BOLD)
label_formato.pack(side=tk.LEFT, padx=10)

entrada_formato = ctk.CTkEntry(frame_baixar, width=80, font=FONT_BOLD)
entrada_formato.pack(side=tk.LEFT, padx=10)

botao_escolher_pasta = ctk.CTkButton(
    frame_baixar,
    text="Escolher Pasta",
    width=140,
    height=35,
    corner_radius=8,
    fg_color="#0078D7",
    hover_color="#005A9E",
    border_width=2,
    border_color="#004578",
    font=FONT_BOLD,
    command=escolher_pasta
)
botao_escolher_pasta.pack(side=tk.LEFT, padx=10)

label_pasta = ctk.CTkLabel(
    frame_baixar,
    text="Pasta de download: Não definida",
    font=FONT_BOLD
)
label_pasta.pack(side=tk.LEFT, padx=10)

botao_baixar = ctk.CTkButton(
    frame_baixar,
    text="Baixar",
    width=140,
    height=35,
    corner_radius=8,
    fg_color="#4CAF50",
    hover_color="#45A049",
    border_width=2,
    border_color="#357a38",
    font=FONT_BOLD,
    command=baixar_video
)
botao_baixar.pack(side=tk.LEFT, padx=10)

botao_parar = ctk.CTkButton(
    frame_baixar,
    text="Parar Download",
    width=140,
    height=35,
    corner_radius=8,
    fg_color="#D9534F",
    hover_color="#C9302C",
    border_width=2,
    border_color="#7b2e27",
    font=FONT_BOLD,
    command=parar_download
)
botao_parar.pack(side=tk.LEFT, padx=10)

# Ajuste responsivo
janela.grid_rowconfigure(1, weight=1)
janela.grid_columnconfigure(0, weight=1)

janela.mainloop()
