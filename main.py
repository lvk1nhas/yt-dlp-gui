import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys
import os
import datetime
import customtkinter as ctk
from tkinter import filedialog

# -- Variáveis Globais --
pasta_destino = ""
processo_download = None

# --- Funções ---

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, funciona com PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def atualizar_estado_widgets(status):
    """Habilita/desabilita widgets para evitar ações concorrentes."""
    if status == "ocupado":
        estado = "disabled"
        status_texto = "Verificando..."
        status_cor = "orange"
    elif status == "download":
        estado = "disabled"
        status_texto = "Download..."
        status_cor = "red"
    else: # 'pronto'
        estado = "normal"
        status_texto = "Pronto"
        status_cor = "green"

    botao_verificar.configure(state=estado)
    botao_baixar.configure(state=estado)
    botao_parar.configure(state="normal" if status == "download" else "")
    status_label.configure(text=status_texto, fg_color=status_cor)

def escolher_pasta():
    global pasta_destino
    caminho = filedialog.askdirectory(title="Escolha a pasta para salvar o download")
    if caminho:
        pasta_destino = caminho
        nome_da_pasta = os.path.basename(caminho)
        label_pasta.configure(text=f"Pasta: {nome_da_pasta}")

def verificar_link_thread(url):
    """Executa a verificação do link em uma thread para não travar a GUI."""
    try:
        flags = 0
        if sys.platform == "win32":
            flags = subprocess.CREATE_NO_WINDOW

        resultado = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True, creationflags=flags)

        saida_texto.delete(1.0, tk.END)

        if "Unsupported URL" in resultado.stdout or "ERROR" in resultado.stderr:
            saida_texto.insert(tk.END, "⚠️ Link não suportado ou fora do ar.")
        else:
            saida_texto.insert(tk.END, resultado.stdout)
            saida_texto.insert(tk.END, "\n\nVerificação concluída. Insira um código de formato e clique em Baixar.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao verificar: {str(e)}")
    finally:
        atualizar_estado_widgets("pronto")

def verificar_link():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Digite um link.")
        return

    atualizar_estado_widgets("ocupado")
    thread = threading.Thread(target=verificar_link_thread, args=(url,), daemon=True)
    thread.start()

def download_thread(url, formato):
    global processo_download
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.join(pasta_destino, f"%(title)s_{timestamp}.%(ext)s")
    
    comando = ["yt-dlp", "-f", formato, "--no-part", "-o", nome_arquivo, url]

    flags = 0
    if sys.platform == "win32":
        # Removido CREATE_NEW_PROCESS_GROUP, pois vamos matar pelo PID com taskkill
        flags = subprocess.CREATE_NO_WINDOW

    processo_download = subprocess.Popen(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        creationflags=flags
    )

    saida_texto.delete(1.0, tk.END)
    saida_texto.insert(tk.END, "Iniciando download...\n\n")
    saida_texto.see(tk.END)

    for linha in processo_download.stdout:
        saida_texto.insert(tk.END, linha)
        saida_texto.see(tk.END)

    ret_code = processo_download.wait()

    if processo_download and processo_download.poll() is not None and ret_code == 0:
        saida_texto.insert(tk.END, "\n\n✅ Download finalizado com sucesso!\n")
    else:
        saida_texto.insert(tk.END, "\n\n❌ Download interrompido ou falhou.\n")

    processo_download = None
    atualizar_estado_widgets("pronto")

def baixar_video():
    url = entrada_url.get().strip()
    formato = entrada_formato.get().strip()

    if not pasta_destino:
        messagebox.showwarning("Aviso", "Por favor, escolha uma pasta de destino primeiro.")
        return
    if not url or not formato:
        messagebox.showwarning("Aviso", "Digite o link e o código do formato.")
        return

    atualizar_estado_widgets("download")
    thread = threading.Thread(target=download_thread, args=(url, formato), daemon=True)
    thread.start()

# --- LÓGICA DE PARADA DEFINITIVA ---
def parar_download():
    """Usa o comando 'taskkill' do Windows para forçar o encerramento do processo e de seus filhos."""
    global processo_download
    if processo_download and processo_download.poll() is None:
        try:
            saida_texto.insert(tk.END, "\n\n>> Usando taskkill para forçar o encerramento do processo...\n")
            status_label.configure(text="Parando...", fg_color="orange")

            pid = processo_download.pid
            comando_kill = ["taskkill", "/F", "/PID", str(pid), "/T"]
            
            subprocess.run(comando_kill, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar taskkill: {str(e)}")
            atualizar_estado_widgets("pronto")
    else:
        messagebox.showinfo("Info", "Nenhum download em andamento.")
# --- FIM DA LÓGICA DE PARADA ---

def add_paste_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Colar", command=lambda: widget.insert(tk.END, widget.clipboard_get()))

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu)

# --- Interface ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

janela = ctk.CTk()
janela.title("")
janela.geometry("1000x650")
janela.minsize(1000, 650)
try:
    icone_path = resource_path("media/5D.ico")
    janela.iconbitmap(icone_path)
except Exception:
    print("Ícone não encontrado, continuando sem ele.")

FONT_BOLD = ("Segoe UI", 12, "bold")

# ... (o resto da sua UI continua exatamente o mesmo) ...
frame_top = ctk.CTkFrame(janela)
frame_top.pack(fill=tk.X, padx=15, pady=(15, 5))
label_url = ctk.CTkLabel(frame_top, text="URL:", font=FONT_BOLD)
label_url.pack(side=tk.LEFT, padx=(10, 5))
entrada_url = ctk.CTkEntry(frame_top, font=FONT_BOLD)
entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
add_paste_menu(entrada_url)
botao_verificar = ctk.CTkButton(frame_top, text="Verificar Link", width=130, font=FONT_BOLD, command=verificar_link)
botao_verificar.pack(side=tk.LEFT, padx=5)
status_label = ctk.CTkLabel(frame_top, text="Pronto", text_color="white", width=120, height=30, corner_radius=6, font=FONT_BOLD, fg_color="green")
status_label.pack(side=tk.RIGHT, padx=(5, 10))

frame_meio = ctk.CTkFrame(janela)
frame_meio.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
saida_texto = ctk.CTkTextbox(frame_meio, wrap=tk.WORD, font=("Consolas", 12))
saida_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_baixar = ctk.CTkFrame(janela)
frame_baixar.pack(fill=tk.X, padx=15, pady=(5, 15))
label_formato = ctk.CTkLabel(frame_baixar, text="Código do formato:", font=FONT_BOLD)
label_formato.pack(side=tk.LEFT, padx=(10, 5))
entrada_formato = ctk.CTkEntry(frame_baixar, width=80, font=FONT_BOLD)
entrada_formato.pack(side=tk.LEFT, padx=5)
add_paste_menu(entrada_formato)
botao_escolher_pasta = ctk.CTkButton(frame_baixar, text="Escolher Pasta", font=FONT_BOLD, command=escolher_pasta)
botao_escolher_pasta.pack(side=tk.LEFT, padx=10)
label_pasta = ctk.CTkLabel(frame_baixar, text="Pasta NÃO escolhida!", font=FONT_BOLD)
label_pasta.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
botao_baixar = ctk.CTkButton(frame_baixar, text="Baixar", width=120, font=FONT_BOLD, command=baixar_video)
botao_baixar.pack(side=tk.LEFT, padx=5)
botao_parar = ctk.CTkButton(frame_baixar, text="Parar Download", width=120, font=FONT_BOLD, fg_color="#D9534F", hover_color="#C9302C", command=parar_download)
botao_parar.pack(side=tk.LEFT, padx=(5, 10))

janela.mainloop()