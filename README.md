# LVK Media Downloader

- 🇧🇷 [Leia em Português](README.pt.md)  
- 🇪🇸 [Leia em Espanhol](README.es.md) 

# 🎬 L V Media Downloader (GUI para yt-dlp)

A modern, robust, and efficient graphical interface to download videos and livestreams using `yt-dlp`. 
Ideal for those who want to avoid terminal usage and automate downloads with a professional, responsive user interface.

---

## 🚀 Objective

> "I used to download livestreams and videos and always had to open the terminal, type commands, and deal with errors manually. This program was created to simplify that process, moving from a command-line struggle to a fluid, one-click visual experience."

---

## 🖥️ Features

### New Interactive Interface
- Smart Format List: No more guessing or typing codes manually.
- 🟦 Blue Button (Select): Instantly selects the video/audio ID.
- 🟩 Green Button (+): Smartly appends audio to video (e.g., automatically creates 137+140).
- Responsive Layout: Uses a smart Grid system that adapts to long IDs (perfect for Instagram/TikTok/DASH streams).
- Dual-Pane System: Automatically switches between the Selection List and the Download Log to ensure maximum performance without UI freezing.
- 🎨 Modern interface using `CustomTkinter`

### Core Functionality
- Multi-Threaded: The UI never freezes while verifying links or downloading.
- Context Menu Pro: Right-click on any text field to Cut, Copy, Paste, Delete, or Select All.
- Smart Stop: Distinguishes between a manual stop by the user (Info) and actual errors or natural stream endings (Success).
- Clean Parsing: Automatically filters out noise (like separator lines) from yt-dlp output.
- Timestamps: Filenames include timestamps to avoid overwriting files.

---

## 📦 Requirements

### ✔️ Python Dependencies

Install the following packages with `pip`:

```bash
pip install customtkinter
```

> The standard tkinter comes pre-installed with Python on Windows.
> If you’re using Linux, you can install it with: 
```bash
sudo apt install python3-tk
```

### ✔️ yt-dlp (the download engine)

You need to have yt-dlp installed and accessible from the terminal (CMD):

```bash 
pip install yt-dlp 
```
This way, yt-dlp will be available in your Python environment and can be called directly by the script without needing manual downloads or PATH configuration.

### ✔️ FFmpeg (Required for merging)
To use the Green "+" Button (Video + Audio merge), FFmpeg must be installed on your system. Without it, yt-dlp cannot merge separate streams.


---

## 📁 Structure

```
lvkMD/
├── media/
│   └── 5D.ico       # App Icon
├── main.py          # Source Code
└── .gitignore

```

---

## ▶️ How to use

1. Run the application: ``python main.py`` (or run the compiled ``.exe``)
2. Select Language: Use the dropdown menu (top-right) to choose your preferred language.
3. Paste the URL: Supports YouTube, Twitch, Instagram, Kick, etc. (Tip: Right-click to paste)
4. Click "Check Link": The app will list all available formats in an interactive grid.
5. Select Formats: 
  - Click the ID (🟦) to select the video track. 
  - Click the + (🟩) on an audio track to combine them.
6. Choose Folder: Select where to save the file.
7. Click "Download": The screen will switch to the log view showing real-time progress.
8. Control: You can stop the download anytime. The app will notify you if it was a manual stop or a successful completion.

---

## 📸 Interface

> ![Screenshot of the program interface](media/Tela.png)

---

## 🔄 Version History


### ✅ Version 3.0 (Major Update)
- Multi-Language Support (EN, PT, ES).
- Architecture: Complete rewrite to OOP (Object Oriented Programming).
- Performance: Implemented Threading to prevent "Application Not Responding" issues.
- UI/UX:
  - Replaced text-based list with Interactive Buttons.
  - Added Grid Layout for better alignment of complex IDs.
  - Added Context Menu (Right-click capabilities).

###  Version 2.0 
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

- Python 3.12+🐍
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 📄 License

- This project is licensed under the MIT License.
- Feel free to modify and contribute!
---

