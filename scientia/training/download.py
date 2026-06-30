from huggingface_hub import snapshot_download
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent

def start(id, dst):
    if(not (id and dst)):
        print(f"Start download under location 'https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507'. Save under path {script_dir / "../../../models/Qwen/Qwen3-4B-Instruct-2507"}. Please wait...")
        snapshot_download(
            repo_id="Qwen/Qwen3-4B-Instruct-2507",
            local_dir= script_dir / "../../../models/Qwen/Qwen3-4B-Instruct-2507"
        )

        print(f"Start download under location 'https://huggingface.co/intfloat/multilingual-e5-small'. Save under path {script_dir / "../../../models/intfloat/multilingual-e5-small"}. Please wait...")
        snapshot_download(
            repo_id="intfloat/multilingual-e5-small",
            local_dir= script_dir / "../../../models/intfloat/multilingual-e5-small"
        )
    else:
        print(f"Start download under location 'https://huggingface.co/{id}'. Save under path {dst}. Please wait...")
        
        snapshot_download(
            repo_id=id,
            local_dir=Path(dst)
        )