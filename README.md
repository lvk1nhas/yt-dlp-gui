# LVK Media Downloader

- 🇧🇷 [Leia em Português](README.pt.md)  

# 🎬 LVK Media Downloader (GUI para yt-dlp)

A simple, modern, and efficient graphical interface to download videos and livestreams using `yt-dlp`.  
Ideal for those who want to avoid terminal use and automate the download process with just a few clicks.

---

## 🚀 Objetivo

> "I used to download livestreams and videos and always had to open the terminal, type commands, and deal with errors manually. This program was created to simplify that process — with a simple and functional visual interface."

---

## 🖥️ Features

- 🔍 Checks available video formats when you paste a link
- 🎯 Supports selection of **video + audio combined** (e.g., `137+140`)
- 📁 Allows choosing the destination folder for the downloaded file
- ⏬ Shows download progress in real time (via `yt-dlp`)
- 🟥 Ability to **manually stop the download**
- 🎨 Modern interface using `CustomTkinter`
- 🧠 Filenames include timestamps to avoid overwriting

---

## 📦 Requirements

### ✔️ Python Dependencies

Install the following packages with `pip`:

```bash
pip install customtkinter
```

> The standard tkinter comes pre-installed with Python on Windows.
> If you’re using Linux, you can install it with: 
> ```bashsudo apt install python3-tk```

### ✔️ yt-dlp (the download engine)

You need to have yt-dlp installed and accessible from the terminal (CMD):

1. [Download yt-dlp here](https://github.com/yt-dlp/yt-dlp/releases/latest)
2. Rename the executable to `yt-dlp.exe`
3. Place it in a folder and add that folder to your system’s PATH environment variable, or put yt-dlp.exe in the same folder as your script.

---

## 📁 Structure

```
lvkMD/
├── media/
│   └── 5D.ico
└── main.py

```


## ▶️ How to use

1. Run the Python script:
   `python main.py`
2. Paste the link of a livestream or video.
3. Click Check Link to list available formats.
4. Choose the format code (e.g., 137+140 for video+audio).
5. Click Choose Folder and select where to save.
6. Click Download and follow the progress.
7. Monitor progress or click Stop Download to cancel.

---

## 📌 Observações

- The program works with any link supported by `yt-dlp`: YouTube, Twitch, Facebook, etc.
- The format field accepts combinations like `137+140` to download video and audio together.
- The saved filename includes a timestamp to avoid overwriting videos with the same name.

---

## 📸 Interface

> ![Screenshot of the program interface](media/Tela.png)

---

## 🔄 Version History

### ✅ Version 2.0 (current)
- Support for downloading combined video+audio (`137+140`)
- Improved readability of listed formats
- Visual and structural code updates

---

## 💡 Future improvements

- Support for multiple downloads in queue
- Download history
- Automatic best format detection
- Enhanced text output interface for better readability

---

## 🛠️ Technologies used

- Python 🐍
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 📄 License

This project is licensed under the MIT License.
Feel free to modify and contribute!
---

