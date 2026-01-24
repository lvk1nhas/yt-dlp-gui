import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import threading
import sys
import os
import datetime
import customtkinter as ctk

# --- Configurações de Sistema ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

WIN_FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

# --- DICIONÁRIO DE IDIOMAS ---
TRADUCOES = {
    "pt": {
        "url_label": "URL:",
        "btn_verify": "Verificar Link",
        "status_ready": "Pronto",
        "status_busy": "Verificando...",
        "status_download": "Baixando...",
        "list_title": "Formatos Disponíveis",
        "list_hint": "Insira o link e clique em verificar.",
        "code_label": "Código:",
        "code_placeholder": "Ex: 137",
        "btn_folder": "Escolher Pasta",
        "folder_none": "Pasta NÃO escolhida!",
        "folder_selected": "Pasta: ",
        "btn_download": "Baixar",
        "btn_stop": "Parar",
        "ctx_copy": "Copiar",
        "ctx_paste": "Colar",
        "ctx_cut": "Recortar",
        "ctx_del": "Apagar",
        "ctx_all": "Selecionar Tudo",
        "msg_warn_link": "Digite um link.",
        "msg_warn_folder": "Escolha uma pasta.",
        "msg_warn_code": "Preencha URL e Código.",
        "msg_info_stop": "Download interrompido por você.",
        "msg_success": "Download Finalizado!",
        "msg_error": "Ocorreu uma falha no download.",
        "header_loading": "Carregando formatos...",
        "header_error": "Erro ao buscar formatos.",
        "msg_nothing": "Nada baixando no momento.", 
    },
    "en": {
        "url_label": "URL:",
        "btn_verify": "Check Link",
        "status_ready": "Ready",
        "status_busy": "Checking...",
        "status_download": "Downloading...",
        "list_title": "Available Formats",
        "list_hint": "Paste link and click check.",
        "code_label": "Code:",
        "code_placeholder": "Ex: 137",
        "btn_folder": "Choose Folder",
        "folder_none": "NO folder selected!",
        "folder_selected": "Folder: ",
        "btn_download": "Download",
        "btn_stop": "Stop",
        "ctx_copy": "Copy",
        "ctx_paste": "Paste",
        "ctx_cut": "Cut",
        "ctx_del": "Delete",
        "ctx_all": "Select All",
        "msg_warn_link": "Enter a link.",
        "msg_warn_folder": "Choose a folder.",
        "msg_warn_code": "Fill in URL and Code.",
        "msg_info_stop": "Download stopped by user.",
        "msg_success": "Download Finished!",
        "msg_error": "Download failed.",
        "header_loading": "Loading formats...",
        "header_error": "Error fetching formats.",
        "msg_nothing": "Nothing is downloading.", 
    },
    "es": {
        "url_label": "URL:",
        "btn_verify": "Verificar Enlace",
        "status_ready": "Listo",
        "status_busy": "Verificando...",
        "status_download": "Descargando...",
        "list_title": "Formatos Disponibles",
        "list_hint": "Pegue el enlace y verifique.",
        "code_label": "Código:",
        "code_placeholder": "Ej: 137",
        "btn_folder": "Elegir Carpeta",
        "folder_none": "¡Carpeta NO elegida!",
        "folder_selected": "Carpeta: ",
        "btn_download": "Descargar",
        "btn_stop": "Detener",
        "ctx_copy": "Copiar",
        "ctx_paste": "Pegar",
        "ctx_cut": "Cortar",
        "ctx_del": "Borrar",
        "ctx_all": "Seleccionar Todo",
        "msg_warn_link": "Ingrese un enlace.",
        "msg_warn_folder": "Elija una carpeta.",
        "msg_warn_code": "Complete URL y Código.",
        "msg_info_stop": "Descarga detenida por usuario.",
        "msg_success": "¡Descarga Finalizada!",
        "msg_error": "La descarga falló.",
        "header_loading": "Cargando formatos...",
        "header_error": "Error al buscar formatos.",
        "msg_nothing": "Nada descargando.",
    }
}

class LVMediaDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela
        self.title("L V - Media Downloader")
        self.geometry("1000x700")
        self.minsize(1000, 650)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        try: self.iconbitmap(resource_path("media/5D.ico"))
        except: pass

        # Variáveis
        self.pasta_destino = ""
        self.processo_download = None
        self.parou_manual = False
        self.ultimo_resultado = None 
        self.font_bold = ("Segoe UI", 12, "bold")
        self.font_mono = ("Consolas", 11)
        
        # Controle de Estado e Idioma
        self.status_atual_key = "status_ready" # Guarda a chave do status atual
        self.idioma = "pt"
        self.mapa_idiomas = {"Português": "pt", "English": "en", "Español": "es"}

        self.setup_ui()
        self.atualizar_textos()

    def t(self, key):
        return TRADUCOES[self.idioma].get(key, key)

    def setup_ui(self):
        # --- Topo (URL e Idioma) ---
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(fill=tk.X, padx=15, pady=(15, 5))

        self.lbl_url = ctk.CTkLabel(frame_top, text="", font=self.font_bold)
        self.lbl_url.pack(side=tk.LEFT, padx=(10, 5))
        
        self.url_var = tk.StringVar()
        self.url_var.trace("w", lambda *a: self.url_var.set(self.url_var.get()[:400]) if len(self.url_var.get()) > 400 else None)
        
        self.entrada_url = ctk.CTkEntry(frame_top, font=self.font_bold, textvariable=self.url_var)
        self.entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.criar_menu_contexto(self.entrada_url)

        self.btn_verificar = ctk.CTkButton(frame_top, text="", width=130, font=self.font_bold, command=self.verificar_link)
        self.btn_verificar.pack(side=tk.LEFT, padx=5)
        
        self.combo_idioma = ctk.CTkOptionMenu(
            frame_top, 
            values=list(self.mapa_idiomas.keys()), 
            width=100,
            command=self.mudar_idioma
        )
        self.combo_idioma.set("Português")
        self.combo_idioma.pack(side=tk.RIGHT, padx=5)

        self.status_label = ctk.CTkLabel(frame_top, text="", text_color="white", width=120, height=30, corner_radius=6, font=self.font_bold, fg_color="green")
        self.status_label.pack(side=tk.RIGHT, padx=(5, 10))

        # --- MEIO ---
        self.frame_central = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_central.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.frame_lista = ctk.CTkScrollableFrame(self.frame_central, label_text="")
        self.frame_lista.pack(fill=tk.BOTH, expand=True)
        
        self.lbl_aviso = ctk.CTkLabel(self.frame_lista, text="", font=self.font_bold, text_color="gray")
        self.lbl_aviso.pack(pady=20)

        self.caixa_log = ctk.CTkTextbox(self.frame_central, wrap=tk.WORD, font=self.font_mono)
        self.criar_menu_contexto(self.caixa_log, readonly=True)

        # --- Base ---
        frame_baixar = ctk.CTkFrame(self)
        frame_baixar.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.lbl_codigo = ctk.CTkLabel(frame_baixar, text="", font=self.font_bold)
        self.lbl_codigo.pack(side=tk.LEFT, padx=(10, 5))
        
        self.entrada_formato = ctk.CTkEntry(frame_baixar, width=100, font=self.font_bold, placeholder_text="")
        self.entrada_formato.pack(side=tk.LEFT, padx=5)
        self.criar_menu_contexto(self.entrada_formato)

        self.btn_pasta = ctk.CTkButton(frame_baixar, text="", font=self.font_bold, command=self.escolher_pasta)
        self.btn_pasta.pack(side=tk.LEFT, padx=10)
        
        self.label_pasta = ctk.CTkLabel(frame_baixar, text="", font=self.font_bold)
        self.label_pasta.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.btn_baixar = ctk.CTkButton(frame_baixar, text="", width=120, font=self.font_bold, command=self.baixar_video)
        self.btn_baixar.pack(side=tk.LEFT, padx=5)
        
        self.btn_parar = ctk.CTkButton(frame_baixar, text="", width=100, font=self.font_bold, fg_color="#D9534F", hover_color="#C9302C", command=self.parar_download)
        self.btn_parar.pack(side=tk.LEFT, padx=(5, 10))

    # --- Lógica de Idioma ---
    def mudar_idioma(self, escolha):
        self.idioma = self.mapa_idiomas[escolha]
        self.atualizar_textos()

    def atualizar_textos(self):
        # Textos Gerais
        self.lbl_url.configure(text=self.t("url_label"))
        self.btn_verificar.configure(text=self.t("btn_verify"))
        
        # Atualiza o status baseado no estado atual (não força "Pronto")
        self.status_label.configure(text=self.t(self.status_atual_key))
        
        self.frame_lista.configure(label_text=self.t("list_title"))
        try: self.lbl_aviso.configure(text=self.t("list_hint"))
        except: pass 

        self.lbl_codigo.configure(text=self.t("code_label"))
        self.entrada_formato.configure(placeholder_text=self.t("code_placeholder"))
        
        self.btn_pasta.configure(text=self.t("btn_folder"))
        self.btn_baixar.configure(text=self.t("btn_download"))
        self.btn_parar.configure(text=self.t("btn_stop"))
        
        if not self.pasta_destino:
            self.label_pasta.configure(text=self.t("folder_none"))
        else:
            self.label_pasta.configure(text=f"{self.t('folder_selected')}{os.path.basename(self.pasta_destino)}")

        if self.ultimo_resultado:
            self._processar_output_lista(self.ultimo_resultado)

    # --- Lógica de Interface ---
    def mostrar_painel(self, qual):
        if qual == "lista":
            self.caixa_log.pack_forget()
            self.frame_lista.pack(fill=tk.BOTH, expand=True)
        elif qual == "log":
            self.frame_lista.pack_forget()
            self.caixa_log.pack(fill=tk.BOTH, expand=True)

    def criar_menu_contexto(self, widget, readonly=False):
        menu = tk.Menu(widget, tearoff=0)
        
        def recortar():
            try:
                if readonly: return
                texto = widget.selection_get()
                widget.clipboard_clear()
                widget.clipboard_append(texto)
                widget.update()
                widget.delete("sel.first", "sel.last")
            except: pass
        def colar():
            try:
                if readonly: return
                texto = widget.clipboard_get()
                try: widget.delete("sel.first", "sel.last")
                except: pass
                widget.insert("insert", texto)
            except: pass
        def copiar():
            try:
                texto = widget.get("sel.first", "sel.last") if readonly else widget.selection_get()
                if texto:
                    widget.clipboard_clear()
                    widget.clipboard_append(texto)
                    widget.update()
            except: pass
        def selecionar_tudo():
            widget.select_range(0, 'end')
            widget.icursor('end')
        def apagar():
            try:
                if readonly: return
                widget.delete("sel.first", "sel.last")
            except: pass

        def mostrar(e):
            menu.delete(0, tk.END)
            if not readonly:
                menu.add_command(label=self.t("ctx_cut"), command=recortar)
            menu.add_command(label=self.t("ctx_copy"), command=copiar)
            if not readonly:
                menu.add_command(label=self.t("ctx_paste"), command=colar)
                menu.add_command(label=self.t("ctx_del"), command=apagar)
            menu.add_separator()
            menu.add_command(label=self.t("ctx_all"), command=selecionar_tudo)
            menu.tk_popup(e.x_root, e.y_root)

        widget.bind("<Button-3>", mostrar)

    def atualizar_estado(self, status):
        # Mapeamento
        mapa = {
            "ocupado": ("disabled", "status_busy", "orange"),
            "download": ("disabled", "status_download", "red"),
            "pronto": ("normal", "status_ready", "green")
        }
        # Pega a configuração
        estado, key_texto, cor = mapa.get(status, ("normal", "status_ready", "green"))
        
        # Salva a chave atual para o caso de mudança de idioma
        self.status_atual_key = key_texto
        
        self.btn_verificar.configure(state=estado)
        self.btn_baixar.configure(state=estado)
        self.status_label.configure(text=self.t(key_texto), fg_color=cor)

    def escolher_pasta(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.pasta_destino = caminho
            self.label_pasta.configure(text=f"{self.t('folder_selected')}{os.path.basename(caminho)}")

    def selecionar_codigo(self, codigo):
        self.entrada_formato.delete(0, tk.END)
        self.entrada_formato.insert(0, codigo)

    def adicionar_codigo(self, codigo):
        texto_atual = self.entrada_formato.get().strip()
        if not texto_atual:
            self.entrada_formato.insert(0, codigo)
        else:
            self.entrada_formato.insert(tk.END, f"+{codigo}")

    # --- Verificação ---
    def verificar_link(self):
        url = self.entrada_url.get().strip()
        if not url: return messagebox.showwarning("Aviso", self.t("msg_warn_link"))
        
        self.mostrar_painel("lista")
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.frame_lista, text=self.t("header_loading"), font=self.font_bold).pack(pady=20)
        self.atualizar_estado("ocupado")
        threading.Thread(target=self._verificar_thread, args=(url,), daemon=True).start()

    def _verificar_thread(self, url):
        try:
            res = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True, creationflags=WIN_FLAGS)
            self.ultimo_resultado = res
            self.after(0, lambda: self._processar_output_lista(res))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erro", str(e)))
        finally:
            self.after(0, lambda: self.atualizar_estado("pronto"))

    def _processar_output_lista(self, res):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if "ERROR" in res.stderr:
            ctk.CTkLabel(self.frame_lista, text=self.t("header_error"), text_color="red").pack(pady=20)
            return

        self.frame_lista.grid_columnconfigure(0, weight=0) 
        self.frame_lista.grid_columnconfigure(1, weight=0)
        self.frame_lista.grid_columnconfigure(2, weight=1)

        linhas = res.stdout.splitlines()
        row_idx = 0 
        cabecalho_passou = False
        
        for linha in linhas:
            linha = linha.strip()
            if not linha: continue
            
            if "ID" in linha and "EXT" in linha and "RESOLUTION" in linha:
                cabecalho_passou = True
                # --- HEADERS FIXOS (SEM TRADUÇÃO) ---
                ctk.CTkLabel(self.frame_lista, text="ID", font=self.font_bold, text_color="#AAAAAA").grid(row=row_idx, column=0, padx=5, pady=5, sticky="ew")
                ctk.CTkLabel(self.frame_lista, text="Add", font=self.font_bold, text_color="#AAAAAA").grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
                
                texto_resto = linha.replace("ID", "  ", 1).strip()
                ctk.CTkLabel(self.frame_lista, text=texto_resto, font=self.font_mono, text_color="#AAAAAA", anchor="w").grid(row=row_idx, column=2, padx=5, pady=5, sticky="w")
                row_idx += 1
                continue
            
            if not cabecalho_passou: continue 

            partes = linha.split()
            if not partes: continue
            codigo = partes[0]
            if codigo.startswith("["): continue
            if "---" in codigo: continue

            ctk.CTkButton(
                self.frame_lista, text=codigo, height=25,
                fg_color="#2B2B2B", border_width=1, border_color="#1F6AA5",
                hover_color="#1F6AA5", font=self.font_bold,
                command=lambda c=codigo: self.selecionar_codigo(c) 
            ).grid(row=row_idx, column=0, padx=2, pady=2, sticky="ew")

            ctk.CTkButton(
                self.frame_lista, text="+", width=30, height=25,
                fg_color="#3A3A3A", border_width=1, border_color="#28A745",
                hover_color="#28A745", font=self.font_bold,
                command=lambda c=codigo: self.adicionar_codigo(c) 
            ).grid(row=row_idx, column=1, padx=2, pady=2, sticky="ew")

            descricao = linha[len(codigo):].strip()
            ctk.CTkLabel(self.frame_lista, text=descricao, font=self.font_mono, anchor="w").grid(row=row_idx, column=2, padx=5, pady=2, sticky="w")
            row_idx += 1

    # --- Download ---
    def baixar_video(self):
        url = self.entrada_url.get().strip()
        formato = self.entrada_formato.get().strip()
        if not self.pasta_destino: return messagebox.showwarning("Aviso", self.t("msg_warn_folder"))
        if not url or not formato: return messagebox.showwarning("Aviso", self.t("msg_warn_code"))

        self.mostrar_painel("log")
        self.caixa_log.delete(1.0, tk.END)
        # LOG FIXO EM INGLÊS
        self.caixa_log.insert(tk.END, ">> Starting download...\n") 

        self.parou_manual = False
        self.atualizar_estado("download")
        threading.Thread(target=self._download_thread, args=(url, formato), daemon=True).start()

    def _download_thread(self, url, formato):
        nome = os.path.join(self.pasta_destino, f"%(title)s_{datetime.datetime.now():%Y%m%d_%H%M%S}.%(ext)s")
        cmd = ["yt-dlp", "-f", formato, "--no-part", "-o", nome, url]
        
        self.processo_download = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            text=True, encoding='utf-8', errors='replace', creationflags=WIN_FLAGS
        )

        for linha in self.processo_download.stdout:
            self.after(0, lambda l=linha: self._log_texto(l))

        ret_code = self.processo_download.wait()

        if self.parou_manual:
             self.after(0, lambda: messagebox.showinfo("Info", self.t("msg_info_stop")))
        elif ret_code == 0:
             self.after(0, lambda: messagebox.showinfo("Sucesso", self.t("msg_success")))
        else:
             self.after(0, lambda: messagebox.showerror("Erro", self.t("msg_error")))
        
        self.processo_download = None
        self.after(0, lambda: self.atualizar_estado("pronto"))

    def _log_texto(self, texto):
        self.caixa_log.insert(tk.END, texto)
        self.caixa_log.see(tk.END)

    def parar_download(self):
        if self.processo_download:
            try:
                self.parou_manual = True
                subprocess.run(["taskkill", "/F", "/PID", str(self.processo_download.pid), "/T"], 
                               capture_output=True, creationflags=WIN_FLAGS)
                # LOG FIXO EM INGLÊS
                self.caixa_log.insert(tk.END, "\n>> PROCESS STOPPED BY USER.\n") 
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showinfo("Info", self.t("msg_nothing")) 

if __name__ == "__main__":
    app = LVMediaDownloader()
    app.mainloop()