from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Qwen/Qwen3-4B-Instruct-2507",
    local_dir="../../../models/Qwen/Qwen3-4B-Instruct-2507"
)

snapshot_download(
    repo_id="intfloat/multilingual-e5-small",
    local_dir="../../../models/intfloat/multilingual-e5-small"
)