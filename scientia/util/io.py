import os
import shutil
from datetime import datetime
from pathlib import Path

def copyFile(src, des):
    if os.exists(src):
        print(f"Ursprungsdatei '{src}' existiert nicht!")
        return False
    elif os.exists(des):
        print(f"Zielort für Datei '{des}', die zu kopieren ist existiert nicht!")
        return False
    else:
        try:
            shutil.copyfile(src=src, dst=des)
            return False
        except IOError:
            print("Datei konnte nicht kopiert werden! Überprüfe z.B. Zugriffsrechte.")
        return True

def removeFile(des):
    if os.path.exists(des):
        try: 
            os.remove(des)
        except IOError:
            return False
        return True
    else:
        return False

def get_file_info(path: Path) -> str:
    try:
        size_bytes = path.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        time_str = mtime.strftime("%d.%m.%Y %H:%M")
        
        extra = ""
        if path.suffix in [".md", ".json", ".jsonl", ".txt"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = sum(1 for _ in f)
            extra = f" | {lines} Zeilen"

        return f"({size_str} | {time_str}{extra})"
    except Exception:
        return "(Zugriff verweigert)"

def list_files(startpath, ignore_patterns=None):
    base_path = Path(startpath)
    patterns = ignore_patterns if ignore_patterns else []
    
    if not base_path.exists():
        print(f" can't read '{startpath}': Verzeichnis existiert nicht.")
        return

    print(f"📁 {base_path.resolve()}")

    for path in base_path.rglob("*"):
        relative_path = path.relative_to(base_path)
        
        if any(relative_path.match(p) for p in patterns):
            continue
        
        level = len(relative_path.parts) - 1
        indent = ' ' * 4 * level
        
        if path.is_dir():
            try:
                num_items = len(list(path.iterdir()))
                print(f"{indent}📂 {path.name}/ ({num_items} Objekte)")
            except Exception:
                print(f"{indent}📂 {path.name}/")
        else:
            
            info = get_file_info(path)
            emoji = "📄" if path.suffix in [".md", ".txt"] else "🖼️" if path.suffix in [".jpeg", ".png"] else "⚙️"
            if path.suffix in [".json", ".jsonl"]:
                emoji = "📊"
                
            print(f"{indent}{emoji} {path.name:<30} {info}")