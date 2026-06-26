import os
import pathlib
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

def main():
    inpt_path = pathlib.Path("../data/veclib/raw").resolve()
    out_path = pathlib.Path("../data/veclib/md").resolve()

    out_path.mkdir(parents=True, exist_ok=True)

    print("Lade Modelle...")
    artifact_dict = create_model_dict()
    converter = PdfConverter(artifact_dict=artifact_dict)

    print("Starte Konvertierung...")
    for filename in os.listdir(inpt_path):
        if filename.endswith(".pdf"):
            pdf_path = inpt_path / filename
            filename_stem = pdf_path.stem
            if pathlib.Path(out_path, f"{filename_stem}.md").exists():
                continue
            print(f"Verarbeite: {filename}")

            try:
                rendered = converter(str(pdf_path))
                full_text, _, images = text_from_rendered(rendered)

                output_file = out_path / f"{filename_stem}.md"

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(full_text)

                img_dir = out_path / filename_stem
                if images:
                    img_dir.mkdir(parents=True, exist_ok=True)

                    for img_name, img_obj in images.items():
                        img_save_path = img_dir / img_name
                        img_obj.save(img_save_path)

                print(f"Erfolgreich konvertiert: {filename} ({len(images)} Bilder extrahiert)")

            except Exception as e:
                print(f"Fehler bei Datei {filename}: {e}")

    print("Fertig!")

if __name__ == '__main__':
    main()
