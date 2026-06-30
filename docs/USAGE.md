# *scientia-base* - **Leitfaden zur Weiterentwicklung**

## Struktureller Dateiaufbau

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

Bevor Sie irgendetwas tun, überprüfen Sie, ob Python, Nodejs und npm installiert sind. Die Befehle dafür finden Sie in der mittleren Spalte, falls dabei aber nicht die Version in der linken Spalte zu sehen sind, nutzen Sie den Befehl aus der Rechten Spalte um die Abhängigkeit **GLOBAL** zu installieren, falls Sie windows nutzen, müssen Sie die letzte Spalte nutzen, um die Abhängigkeit manuell über den Browser zu installieren:

|Version          |Prüfbefehl        |Installation (Linux/iOS)                        |Installation (Windows über Browser)                        |
|-----------------|------------------|------------------------------------------------|-------------------------------------------------------------|
|*nodejs v24.11.0*|`node -v`         |`curl -o- https://githubusercontent.com \| bash && source ~/.bashrc && nvm install 24.11.0 && nvm use 24.11.0`| [Node.js v24 Release Archiv](https://nodejs.org) |
|*npm v11.16.0*   |`npm -v`          |`npm install -g npm@11.16.0`                    |*Wird automatisch mit Node.js installiert*                   |
|*python v3.13.14*|`python --version`|`curl https://pyenv.run \| bash && exec $SHELL && pyenv install 3.13.14 && pyenv global 3.13.14`              | [Python 3.13 offizielle Downloads](https://python.org) |

Das gesamte Projekt lässt sich in zwei Fraktionen unterteilen:

### ./server - Serverapplikationen

Hier liegt der NodeJS-Server und die Nutzerwebsite und alle dazu gehörigen Applikationen.
Folgende Unterordner bzw Unterdateien sind in dem Ordner zu finden und wichtig zu erwähnen:

- **/public** - Hier liegt die Website für den Nutzer
- **server.js** - Hier liegt die Servapplikiation für den Nodejs-Server. Es ist wichtig, dass Sie
  vor dem ersten Start alle Abhängigkeiten installieren, was mit einem Zum Starten des Servers geben sie aus dem Root-Directory (Hauptordner des Projektes) folgenden Befehl ein:
  
  ```shell
  cd ./server | node server.js
  ```

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
Folgende Unterordner bzw Unterdateien sind in dem Ordner zu finden und wichtig zu erwähnen:

- **/.venv** - Enthält die Python-Virtual-Enviroment also die Runtime für das AI-Python-Backend. Der Ordner **muss mittels eines Befehls von Python erstellt werden**, da dieser Ordner betriebssystemspezifische Dateien enthält. Hiermit kann ein Virtual-Enviroment erstellt werden:

  ```shell
  python -m venv ./.venv
  ```

  Beachten Sie, dass Python 3.11 erforderlich ist, da das AI-Backend dafür ausgelegt ist und Sie sich im richtigen Ordner befinden, was für alle folgenden, `./scientia`-betreffenden Befehlen sehr wichtig ist, dafür navoigieren Sie in den Ordner `./scientia`, was sie aus dem Root-Directory (Der Hauptordner des Projektes) mit folgenden Befehl tun:
  
  ```shell
  cd ./scienta
  ```
  
  . **Um mit `pip` das Projekt konfigurieren wollen, müssen Sie folgenden Befehl eintippen, um immer im Virtual-Enviroment zu sein:**
  für Linux:
  
  ```shell
  source ./.venv/bin/activate
  ```

  und für Windows nur:

  ```shell
  ./.venv/Scripts/activate
  ```

- **requirements.txt** - Diese Datei enthält (ähnlich wie die [package.json](#server---serverapplikationen)) alle Abhängigkeiten, die für das AI-Backend erforderlich sind. Um diese Abhängigkeiten für das spezifische Betriebssystem in das `/.venv` herunterzuladen muss folgender Befehl eingetippt werden, beachten Sie dieses mal auch, dass pip3.11 installiert sein muss: 

  ```shell
  pip install -r ./requierments.txt
  ```

  und Sie sich im Root-Directory befinden müssen. Falls Sie währen der Entwicklung neue Bibliotheken mit:

  ```shell
  pip install package-name
  ```

  installieren, müssen Sie die `requierments.txt` updaten, was Sie mit folgenden Befehl tun:

  ```shell
  pip freeze > ./requierments.txt
  ```

- **run/backend.py** - Diese Datei enhält die Applikation für den AI-Backend-Server. Beim starten (was automatisch durch den Nodejs-Server passiert) wird ein flask-Server gestartet und das/die KI-Modell(e) geladen.

- **run/config.py** - Hier kann der AI-Backend-Server konfiguriert werden. Folgende Konfigurationsmöglichkeiten stehen zur auswahl:
  
  - `config.LLM_PATH` - Der Pfad zum LLM-Modell (large language model) (String)
  - `config.EMB_PATH` - Der Pfad zum Embedding-Modell (String)
  - `config.INDEX_FILE`- Der Pfad zu der Index-Datei der Vektorbibliothek (String)
  - `config.CHUNKS_FILE` - Der Pfad zu der Pfad zu den rohen Chunks der Vektorbibliothek
  - `config.HOST` - Der Host, auf dem der AI-Backend-Server läuft und für Nodejs-Server zugänglich ist (String)
  - `config.PORT` - Der Port auf dem der AI-Backend-Server läuft und für Nodejs-Server zugänglich ist (Integer)
  - `config.THREADS` - Die Anzahl an Threads, die der AI-Backend-Server zum parallelen Verarbeiten zur verfügung hat (Integer)
  - `config.SYSTEM_PROMPT` - Der Systemprompt für die Nutzeranfragen für das LLM (String)
  - `config.EXTENDED_CONTEXT(context_text, user_query)` - Das Format für die Zusatzinformationen aus der Vektorbibliothek und der Nutzerfrage. `context_text` ist die Zusatzinformation aus der Vekorbibliothek und `user_query` ist die Nutzerfrage (Function)

- **run/run.py** - Eine Testdatei um ein KI-Modell zutesten, das KI-Modell ist liegt unter dem Pfad unter `config.LLM_PATH` in der `run/config.py`.

- **training/download** - Diese Datei lädt ein KI-Modell von [Huggingface](https://huggingface.co/) herunter. Dabei können zwei Argumente an die Datei übergeben werden, wie hierfolgt dargestellt:

  ```shell
  python ./training/download "hugginface_modell_pfad" "lokaler_pfad_relativ_zum_current_dir"
  ```

  Falls keine Parameter angegeben werden, werden folgende zwei Modelle installiert:
  
  - `Qwen/Qwen3-4B-Instruct-2507` unter den Dateipfad (rel. zum Root): `../models/Qwen/Qwen3-4B-Instruct-2507` - das Hauptmodell
  - `intfloat/multilingual-e5-small` unter den Dateipfad (rel. zum Root): `../models/intfloat/multilingual-e5-small` - Das Vektorbibliotheken Modell


- **training/split.py** - Diese Datei teilt einen Trainingsdatensatz in einer `all.json` in zwei weitere Dateien auf nähmlich die `train.json` und `val.json`, die für das Training essentiell sind. Unter der Bedingung, dass man sich im Virtual-Enviroment befinet (siehe oben unter */.venv*) kann die Datei mit folgenden Befehl genutz werden:

```shell
python train/split.py "pfad_zur_all.json" "pfad_zur_train.json" "pfad_zur_val.json"
```
