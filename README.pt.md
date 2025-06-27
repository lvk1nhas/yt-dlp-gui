# 🎬 LVK Media Downloader (GUI para yt-dlp)

Uma interface gráfica simples, moderna e eficiente para baixar vídeos e transmissões ao vivo usando `yt-dlp`.  
Ideal para quem quer evitar o uso do terminal e automatizar o processo de download com apenas alguns cliques.

---

## 🚀 Objetivo

> "Eu baixava lives e vídeos e sempre precisava abrir o terminal, digitar comandos e lidar com erros manualmente. Este programa foi criado para facilitar esse processo — com uma interface visual simples e funcional."

---

## 🖥️ Funcionalidades

- 🔍 Verifica os formatos disponíveis de vídeos ao colar o link
- 🎯 Suporta seleção de **vídeo + áudio juntos** (ex: `137+140`)
- 📁 Permite escolher a pasta de destino para o arquivo baixado
- ⏬ Mostra o progresso do download em tempo real (via `yt-dlp`)
- 🟥 Possibilidade de **parar o download** manualmente
- 🎨 Interface moderna com `CustomTkinter`
- 🧠 Nome de arquivos com timestamp para evitar sobrescrita

---

## 📦 Requisitos

### ✔️ Dependências Python

Instale os seguintes pacotes com `pip`:

```bash
pip install customtkinter
```

> O `tkinter` padrão já vem com o Python em sistemas Windows.  
> Se estiver usando Linux, você pode instalar com:
```bash
 sudo apt install python3-tk
```

### ✔️ yt-dlp (o motor de download)

Você precisa ter o `yt-dlp` instalado e acessível pelo terminal (CMD).

Recomendamos instalar o yt-dlp via pip para facilitar a instalação e atualizações:

```bash
pip install yt-dlp
```
Assim, o yt-dlp ficará disponível no seu ambiente Python e pode ser usado diretamente pelo script, sem necessidade de download manual ou configuração de PATH.

---

## 📁 Estrutura

```
lvkMD/
├── media/
│   └── 5D.ico
└── main.py

```

---

## ▶️ Como usar

1. Execute o script Python:  
   `python main.py`
2. Cole o link de uma transmissão ou vídeo.
3. Clique em **Verificar Link** para listar os formatos disponíveis.
4. Escolha o código do formato (ex: `137+140` para vídeo+áudio).
5. Clique em **Escolher Pasta** e selecione onde quer salvar.
6. Clique em **Baixar** e acompanhe o progresso.
7. Acompanhe o progresso ou clique em **Parar Download**

---

## 📌 Observações

- O programa funciona com qualquer link suportado pelo `yt-dlp`: YouTube, Twitch, Facebook, etc.
- O campo de formato aceita combinações como `137+140` para baixar vídeo e áudio juntos.
- O nome do arquivo salvo inclui um timestamp para evitar sobrescrever vídeos com o mesmo nome. 

---

## 📸 Interface

> ![Um print da tela do programa](media/Tela.png)

---

## 🔄 Histórico de versões

### ✅ Versão 2.0 (atual)
- Suporte ao download de vídeo+áudio combinados (`137+140`)
- Melhor legibilidade dos formatos listados
- Atualizações visuais e estruturais no código

---

## 💡 Futuras melhorias

- Suporte a múltiplos downloads em fila
- Histórico de vídeos baixados
- Detecção automática do melhor formato
- Conversão da tela do texto para melhor entendimento

---

## 🛠️ Tecnologias usadas

- Python 🐍
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 📄 Licença

Este projeto está sob a licença MIT.  
Sinta-se à vontade para modificar e contribuir!

---
