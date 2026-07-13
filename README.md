# 💻 CYBER COMMAND CENTER 

> ⚠️ **STATUS: IN DEVELOPMENT (WIP)** > *Dieses Projekt befindet sich aktuell in der aktiven Entwicklung. Core-Systeme können sich jederzeit ändern, und neue Module werden regelmäßig hinzugefügt.*

Ein modulares, ressourcenschonendes und hochgradig visuelles Terminal-Dashboard für Linux. Geschrieben in Python, optimiert für moderne Terminal-Emulatoren (wie Kitty, Alacritty) und entworfen, um dir das absolute Hacker-Feeling direkt auf den Desktop zu bringen.

Entwickelt von [@inzekt0r](https://github.com/inzekt0r).

---

## ⚡ Features

Das Dashboard ist nicht nur Spielerei, sondern eine echte Kommandozentrale für dein System:

* **Omni Surveillance:** Echtzeit-Überwachung von CPU, RAM und Festplattenspeicher (visualisiert durch dynamische Unicode-Kreisgraphen).
* **Network Uplink:** Automatische Erkennung der lokalen und öffentlichen IP-Adresse sowie Live-Anzeige des TX/RX-Netzwerktraffics.
* **Process Tracker:** Live-Ansicht der ressourcenintensivsten Prozesse.
* **Performance Optimiert:** Extrem ressourcenschonend dank asynchronem Tick-Throttling (UI läuft mit 2 FPS, schwere Abfragen wie Festplatte und Prozesse laufen gedrosselt im Hintergrund).
* **Interaktives Boot-Menü:** Wähle beim Start aus 5 integrierten Farbschemata (Matrix, Cyberpunk, Ocean, Fire, Mono).
* **Hacker Immersion:** Beinhaltet einen `[ NEUROMANCER STREAM ]` (Matrix Rain) und einen simulierten Hacker-Feed `[ TERMINAL DEMO ]` für die perfekte Optik.

---

## 🛠️ Installation & Voraussetzungen

Das System benötigt **Python 3** sowie zwei externe Bibliotheken für die Systemauslesung und das Terminal-Rendering.

1. **Repository klonen:**
   ```bash
   git clone [https://github.com/inzekt0r/cyber-command-center.git](https://github.com/inzekt0r/cyber-command-center.git)
   cd cyber-command-center


   Abhängigkeiten installieren:

Bash
pip install rich psutil
(Tipp: Je nach Linux-Distribution musst du pip3 verwenden oder eine virtuelle Umgebung / venv anlegen).

Skript ausführbar machen:

Bash
chmod +x cyber_cmd.py
🚀 Nutzung
Starte das Command Center direkt im Terminal. Für das beste Erlebnis nutze den Vollbildmodus oder teile deinen Bildschirm (z.B. mit Kitty oder tmux).

Bash
./cyber_cmd.py
Beim Start wirst du von einer interaktiven Boot-Sequenz begrüßt, in der du das gewünschte Theme über die Zifferntasten (1-5) auswählen kannst.

🚧 Roadmap / Geplante Features
Da sich das Projekt in der Entwicklung befindet, stehen folgende Punkte noch auf dem Plan:

[ ] Implementierung eines Logging-Systems für kritische Hardware-Warnungen.

[ ] GPU-Auslastungsmodul (NVML / AMD).

[ ] Modul für externe Ping/Latenz-Überwachung.

[ ] Konfigurationsdatei (.json oder .yaml) für eigene Farbschemata.

🤝 Contribution
Feedback, Bug-Reports oder Pull Requests sind jederzeit willkommen! Öffne einfach ein Issue im Repository.

Stay safe, stay connected.
