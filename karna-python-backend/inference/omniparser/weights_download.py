from huggingface_hub import snapshot_download

# Define repository and local directory
repo_id = "microsoft/OmniParser-v2.0"  # HF repo
local_dir = "weights"  # Target local directory

# Download the repository
snapshot_download(repo_id, local_dir=local_dir)

print(f"Repository {repo_id} downloaded to {local_dir}")
