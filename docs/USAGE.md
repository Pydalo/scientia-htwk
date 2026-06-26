# *scientia-base* - **Leitfaden zur Weiterentwicklung**

## Struktureller Dateiaufbau

plotterraum
Folgendes zeigt den Dateiaufbau des Repositories:
```dirs
.
├── .git
├── .idea
├── data
│   └── veclib
│       └── md
├── docs
│   ├── ChatbotPlanung.odt
│   ├── ChatbotPlanung.pdf
│   ├── PlanPraktikum.odt
│   ├── PlanPraktikum.pdf
│   └── USAGE.md
├── README.md
├── scientia
│   ├── .idea
│   │   ├── .gitignore
│   │   ├── inspectionProfiles
│   │   │   └── profiles_settings.xml
│   │   ├── misc.xml
│   │   ├── modules.xml
│   │   ├── runConfigurations
│   │   │   └── Backend.xml
│   │   ├── Scientia.iml
│   │   └── vcs.xml
│   ├── .venv
│   │   └── .gitignore
│   ├── data
│   │   ├── all.jsonl
│   │   ├── train.jsonl
│   │   ├── val.jsonl
│   │   └── veclib
│   │       ├── md
│   │       ├── raw
│   │       ├── text_chunks.pkl
│   │       └── vektorbase.index
│   ├── requirements.txt
│   ├── run
│   │   ├── backend.py
│   │   └── run.py
│   ├── test.py
│   ├── training
│   │   ├── download.py
│   │   ├── finetune.py
│   │   └── split.py
│   └── veclib
│       ├── convmarkdown.py
│       ├── convmarkdownsingle.py
│       └── genvectorlib.py
└── server
    ├── config.js
    ├── node_modules
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── animation.js
    │   ├── assets
    │   │   ├── background.png
    │   │   └── faviconv2.png
    │   ├── index.html
    │   ├── main.js
    │   └── style.css
    ├── server.js
    └── start.bat
```

## Projekt Fraktionen Überblick

Das gesamte Projekt lässt sich in zwei Fraktionen unterteilen

### ./server - Serverapplikationen

Hier liegt der NodeJS-Server und die Nutzerwebsite und alle dazu gehörigen Applikationen.
Fogende Unterordner bzw Unterdateien sind in dem Ordner zu finden und wichtig zu erwähnen:

- **/public** - Hier liegt die Website für den Nutzer
- **server.js** - Hier liegt die Servapplikiation für den Nodejs-Server
- **config.js** - Hier kann der Nodejs-Server konfiguriert werden, folgende Optionen stehen zur Auswahl:
  - `config.port` - Der Port auf dem der Nodejs-Server läuft (Integer)
  - `config.host` - Der Host unter dem der Nodejs-Server aufrufbar ist (String)
  - `config.windows` - Ist `true` wenn der Nodejs-Server auf WindowsOS läuft, jeder andere Wert bedeutet, dass der Server auf Linux oder iOS (ist vom Kernel dasselbe) läuft (Boolean)
  - `config.debuglevel` - Teilt den Nodejs-Server mit wie viel er an Debug-Nachrichten ausgeben soll. Dabei bedeuten folgende Werte folgendes für den Nodejs-Server:
    - `-1` - Der Nodejs Server gibt **keine** Debug-Nachricht aus (außer Fehlermeldungen auf dem Server selbst)
    - `0` - Der Nodejs Server gibt **jede** Debug-Nachricht aus
    - `1` - Der Nodejs Server gibt jede Debug-Nachricht aus, bis auf **Netzwerkkommunikations-Debug-Nachrichten** zwischen Client und Nodejs Server

- **package.json** - Enthält **alle benötigten Abhängigkeiten bzw Bibliotheken** zum Nodejs-Server-Betrieb im JSON-Format. Beim erstemaligen Start des Nodejs-Servers werden alle Abhängigkeiten **automatisch installiert** (solange die richtige Nodejs-Version `v24.11.0` benutz wird).

### ./scientia - Der eigentliche Chatbot

Hier liegen alle Bibliotheken und ein gesamtes Python-Virtual-Enviroment.
Ziel hierbei ist die Bereitstellungen des Chatbots, also das Laden, Ausführen, Trainieren und Bilden einer Datenbasis des Chatbots. Damit der Nutzer mit den Chatbot interagieren kann gibt es in der `backend.py` eine API (zum Austausch). 