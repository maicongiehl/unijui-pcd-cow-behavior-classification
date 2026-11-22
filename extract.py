from huggingface_hub import hf_hub_download

pasta_projeto = "./dados/raw"

"""
print("Baixando rótulos de comportamento (behavior_labels.zip)...")
hf_hub_download(
    repo_id="neis-lab/mmcows",
    repo_type="dataset",
    local_dir=pasta_projeto,
    filename="behavior_labels.zip",
)

print("Baixando dados dos sensores inerciais (sensor_data.zip)...")
hf_hub_download(
    repo_id="neis-lab/mmcows",
    repo_type="dataset",
    local_dir=pasta_projeto,
    filename="sensor_data.zip",
)
"""

import zipfile
import os

# 5. Descompactar os arquivos dentro da pasta do Drive
print("Descompactando rótulos comportamentais...")
with zipfile.ZipFile(
    os.path.join(pasta_projeto, "behavior_labels.zip"), "r"
) as zip_ref:
    zip_ref.extractall(pasta_projeto)

print("Descompactando dados dos sensores...")
with zipfile.ZipFile(os.path.join(pasta_projeto, "sensor_data.zip"), "r") as zip_ref:
    zip_ref.extractall(pasta_projeto)
