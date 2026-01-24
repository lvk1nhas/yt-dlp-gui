# LVK Media Downloader

- 🇧🇷 [Leia em Português](README.pt.md)  
- 🇪🇸 [Leia em Espanhol](README.es.md)

# 🎬 L V Media Downloader (GUI para yt-dlp)

Uma interface gráfica moderna, robusta e eficiente para baixar vídeos e transmissões ao vivo usando o `yt-dlp`. 
Ideal para quem deseja evitar o uso do terminal e automatizar downloads com uma interface de usuário profissional e responsiva.

---

## 🚀 Objetivo

> “Eu costumava baixar transmissões ao vivo e vídeos e sempre precisava abrir o terminal, digitar comandos e lidar com erros manualmente. Este programa foi criado para simplificar esse processo, passando de uma luta com a linha de comando para uma experiência visual fluida com um clique.”

---

## 🖥️ Recursos

### Nova interface interativa
- Lista de formatos inteligentes: não é mais necessário adivinhar ou digitar códigos manualmente.
- 🟦 Botão azul (Selecionar): seleciona instantaneamente o ID do vídeo/áudio.
- 🟩 Botão verde (+): anexa áudio ao vídeo de forma inteligente (por exemplo, cria automaticamente 137+140).
- Layout responsivo: usa um sistema de grade inteligente que se adapta a IDs longos (perfeito para transmissões do Instagram/TikTok/DASH).
- Sistema de painel duplo: alterna automaticamente entre a lista de seleção e o registro de downloads para garantir o máximo desempenho sem congelamento da interface do usuário.
- 🎨 Interface moderna usando `CustomTkinter`

### Funcionalidade principal
- Multithread: a interface do usuário nunca congela durante a verificação de links ou downloads.
- Menu de contexto profissional: clique com o botão direito do mouse em qualquer campo de texto para cortar, copiar, colar, excluir ou selecionar tudo.
- Parada inteligente: distingue entre uma parada manual pelo usuário (Informações) e erros reais ou finais naturais de stream (Sucesso).
- Análise limpa: filtra automaticamente ruídos (como linhas separadoras) da saída do yt-dlp.
- Carimbos de data/hora: os nomes dos arquivos incluem carimbos de data/hora para evitar a sobrescrita de arquivos.

---

## 📦 Requisitos

### ✔️ Dependências Python

Instale os seguintes pacotes com `pip`:

```bash
pip install customtkinter
```

> O tkinter padrão vem pré-instalado com o Python no Windows.
> Se você estiver usando Linux, pode instalá-lo com: 
```bash
sudo apt install python3-tk
```

### ✔️ yt-dlp (o mecanismo de download)

Você precisa ter o yt-dlp instalado e acessível a partir do terminal (CMD):

```bash 
pip install yt-dlp 
```
Dessa forma, o yt-dlp estará disponível em seu ambiente Python e poderá ser chamado diretamente pelo script, sem a necessidade de downloads manuais ou configuração de PATH.

### ✔️ FFmpeg (necessário para mesclagem)
Para usar o botão verde “+” (mesclagem de vídeo + áudio), o FFmpeg deve estar instalado no seu sistema. Sem ele, o yt-dlp não pode mesclar fluxos separados.


---

## 📁 Estrutura

```
lvkMD/
├── media/
│   └── 5D.ico       # Ícone do aplicativo
├── main.py          # Código-fonte
└── .gitignore

```

---

## ▶️ Como usar

1. Execute o aplicativo: ``python main.py`` (ou execute o ``.exe`` compilado)
2. Selecione o idioma: use o menu suspenso (canto superior direito) para escolher o idioma de sua preferência.
3. Cole a URL: compatível com YouTube, Twitch, Instagram, Kick, etc. (Dica: clique com o botão direito para colar)
4. Clique em “Verificar link”: o aplicativo listará todos os formatos disponíveis em uma grade interativa.
5. Selecione os formatos: 
  - Clique no ID (🟦) para selecionar a faixa de vídeo. 
  - Clique no + (🟩) em uma faixa de áudio para combiná-las.
6. Escolha a pasta: selecione onde salvar o arquivo.
7. Clique em “Baixar”: A tela mudará para a visualização do log, mostrando o progresso em tempo real.
8. Controle: Você pode interromper o download a qualquer momento. O aplicativo irá notificá-lo se foi uma interrupção manual ou uma conclusão bem-sucedida.

---

## 📸 Interface

> ![Captura de tela da interface do programa](media/Tela.png)

---

## 🔄 Histórico de versões


### ✅ Versão 3.0 (Atualização importante)
- Suporte a vários idiomas (EN, PT, ES).
- Arquitetura: reescrita completa para OOP (Programação Orientada a Objetos).
- Desempenho: implementação de threading para evitar problemas de “Aplicativo não responde”.
- UI/UX:
  - Lista baseada em texto substituída por botões interativos.
  - Adicionado layout em grade para melhor alinhamento de IDs complexas.
  - Adicionado menu de contexto (recursos do botão direito do mouse).

###  Versão 2.0
- Suporte para download combinado de vídeo + áudio (`137+140`)
- Melhoria na legibilidade dos formatos listados
- Atualizações visuais e estruturais do código

---

## 💡 Melhorias futuras

- Suporte para vários downloads em fila
- Histórico de downloads
- Detecção automática do melhor formato
- Interface de saída de texto aprimorada para melhor legibilidade

---

## 🛠️ Tecnologias utilizadas

- Python 3.12+🐍
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 📄 Licença

- Este projeto está licenciado sob a Licença MIT.
- Sinta-se à vontade para modificar e contribuir!
---



Traduzido com a versão gratuita do tradutor - DeepL.com