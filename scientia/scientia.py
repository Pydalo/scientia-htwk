import argparse
from pathlib import Path
import sys

from util import io
from run import config

script_path = Path(__file__).resolve().parent.absolute()
sys.path.append(str(script_path))

parser = argparse.ArgumentParser(
    description="Laufzeit- und Trainingsumgebung für Scientia Chatbot", 
    prog="SCE (Scientia Chatbot Environment)", 
    epilog="Wenn das Ihnen nicht hilft... tja ╰（‵□′）╯"
)

parser.add_argument("-v", "--verbose", action="store_true", help="Erweiterte Log-Ausgaben aktivieren")

subparsers = parser.add_subparsers(dest="command", required=True, help="Verfügbare Modi")

# scientia server
parser_server = subparsers.add_parser("server", help="Den AI-Python-Backend-Server starten")
# scientia train [-i|--inputmodel] [-o|--outputmodel] [-v|--vectormodel] [-d|--traindata] [-l|--veclib]
parser_train = subparsers.add_parser("train", help="Das Chatbot-Modell finetunen")
train_subparsers = parser_train.add_subparsers(dest="train_command", required=True, help="Verfügbare Modi")
parser_train_finetune = train_subparsers.add_parser("finetune", help="Finetune das KI-Modell")
parser_train_finetune.add_argument("-i", "--inputmodel", help="Der Pfad zum Inputmodell", default= str(Path(config.__file__).resolve().parent.absolute() / config.LLM_PATH))
parser_train_finetune.add_argument("-o", "--outputmodel", help="Der Pfad zum Outputmodell", default= str(Path(config.__file__).resolve().parent.absolute() / config.LLM_NEW_PATH))
parser_train_finetune.add_argument("-v", "--vectormodel", help="Der Pfad zum Vektorbibliothekenmodel", default= str(Path(config.__file__).resolve().parent.absolute() / config.EMB_PATH))
parser_train_finetune.add_argument("-d", "--traindata", help="Der Pfad zu den Ordner mit der train.json und val.json", default= str(script_path / "./data"), type=str)
parser_train_finetune.add_argument("-l", "--veclib", help="Der Pfad zur Vektorbibliothek", default= str(script_path / "./data/veclib"), type=str)
# scientia split [(--file|-f)=<filepath>]
parser_train_split = train_subparsers.add_parser("split", help="Teile die Trainingsdaten in train.json und val.json auf")
parser_train_split.add_argument("-f", "--file", help="Die all.json", default= str(script_path / "./data/all.jsonl"), type=str)
parser_train_split.add_argument("-d", "--dst", help="Das outputdirectory", default= str(script_path / "./data/"), type=str)

parser_veclib = subparsers.add_parser("lib", help="Die Vektorbiliothek bearbeiten")
veclib_subparsers = parser_veclib.add_subparsers(dest="lib_command", required=True, help="Verfügbare Modi")
# scientia lib add <file> [--raw|-r]
parser_veclib_add = veclib_subparsers.add_parser("add", help="Füge eine neue Markdowndatei zu den Trainingsdaten hinzu")
parser_veclib_add.add_argument("file", help="Die Markdowndatei", type=str)
parser_veclib_add.add_argument("-r", "--raw", action="store_true", help="Kopiere in den RAW-Ordner './data/veclib/raw'. Dient zum speichern Roher Trainingsdaten")
# scientia lib list
parser_veclib_list = veclib_subparsers.add_parser("list", help="Liste alle Trainingsdaten auf")
parser_veclib_list.add_argument("-r", "--raw", action="store_true", help="List alle Dateien im Raw Ordner auf")
parser_veclib_list.add_argument(
    "-i", "--ignore", 
    nargs="+", 
    help="Ein oder mehrere Glob-Patterns für Dateien/Ordner zum Ignorieren..."
)
# scientia lib remove <file>
parser_veclib_remove = veclib_subparsers.add_parser("remove", help="Entferne eine Trainingsdatei")
parser_veclib_remove.add_argument("file", help="Der Dateinamen, den Sie entfernen wollen", type=str)
parser_veclib_remove.add_argument("-r", "--raw", action="store_true", help="Lösche in den RAW-Ordner './data/veclib/raw'.")
# scientia lib build [(--src|-s)=sourcemds] [(--output|-o)=outputdir]
parser_veclib_build = veclib_subparsers.add_parser("build", help="Baue eine Vektorbibliothek")
parser_veclib_build.add_argument("-s", "--src", type=str, default= str(script_path / "./data/veclib/md"), help="Der Pfad zu dem Ordner mit den Inputdateien, ausdem die Vektorbib gebaut wird.")
parser_veclib_build.add_argument("-d", "--dst", help="Das Outputverzeichnis wo die 'text_chunks.pkl' und 'vektorbase.index' hinkopiert werden.", type=str, default= script_path / "./data/veclib/")
# scientia lib conver [(--src|-s)=sourcepdfs] [(--output|-o)=outputmddir]
parser_veclib_covert = veclib_subparsers.add_parser("convert", help="Konvertiere eine PDF zu Markdown und füge sie zu den Trainingsdaten hinzu")
parser_veclib_covert.add_argument("-s", "--src", type=str, default= str(script_path / "./data/veclib/raw"), help="Übersetze das Verzeichnis oder die angegebene Datei in Markdown")
parser_veclib_covert.add_argument("-d", "--dst", type=str, default= str(script_path / "./data/veclib/md"), help="Das Verzeichnis in das kopiert wird")
# scientia download [(--model|-m)=model_id] [(--path|-p)=localpath]
parser_download = subparsers.add_parser("download", help="Ein KI-Modell von Huggingface (https://huggingface.co) herunterladen. Bei keinen Argumenten werden die Standardmodelle heruntergeladen.")
parser_download.add_argument("-m", "--model", type=str, help="Die huggingface-ID von dem gewünschten KI-Modell")
parser_download.add_argument("-p", "--path", type=str, help="Der lokale Pfad, unter dem das KI-Modell gespeichert werden soll")
# scientia test
parser_test = subparsers.add_parser("test", help="Führt das Modell in der CLI (aka Konsole) aus. Zum testen")

args = parser.parse_args()
match args.command:
    case "server":
        from run import backend
        backend.start()
    case "lib":
        match args.lib_command:
            case "add":
                target_destination = "data/veclib/raw" if args.raw else "data/veclib/md"
                if io.copyFile(args.file, str(script_path / target_destination)):
                    print(f"Datei '{args.file}' wurde erfolgreich nach '{script_path / target_destination}'")
            case "list":
                target_destination = "data/veclib/raw" if args.raw else "data/veclib/md"
                io.list_files(str(script_path / target_destination), args.ignore)
            case "remove":
                target_destination = "data/veclib/raw" if args.raw else "data/veclib/md"
                if not io.removeFile(target_destination / args.file):
                    raise IOError("Datei konnte nicht gelöscht werden!")
                else:
                    print("Datei konnte erfolgreich gelöscht werden!")
            case "build":
                from veclib import gen
                gen.start(args.src, args.dst)
            case "convert":
                from veclib.convmarkdown import start
                start(Path(args.src), Path(args.dst))
    case "download":
        from training.download import start
        start(args.model, args.path)
    case "test":
        from run.run import start
        start()
    case "train":
        match args.train_command:
            case "finetune":
                from training.finetune import start
                start(args.inputmodel, args.outputmodel, args.vectormodel, args.veclib, args.traindata)
            case "split":
                from training.split import start
                start(args.file, args.dst)