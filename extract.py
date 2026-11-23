# Script DESATIVADO: o projeto usa apenas os CSVs limpos em ./dados/clean,
# então não é necessário baixar nem descompactar os dados brutos do MmCows.
# Para reativar, remover as aspas triplas do bloco abaixo.
# O sensor_data.zip tem cerca de 18 GB.

print("extract.py desativado: usar os CSVs limpos em ./dados/clean.")

"""
import os
import zipfile

from huggingface_hub import hf_hub_download

# 1. Definir a pasta onde os dados brutos ficam
pasta_projeto = "./dados/raw"
os.makedirs(pasta_projeto, exist_ok=True)

# 2. Definir os zips do MmCows necessários
arquivos = ["behavior_labels.zip", "sensor_data.zip"]

for nome in arquivos:
    caminho_zip = os.path.join(pasta_projeto, nome)

    # 3. Baixar do Hugging Face apenas se o zip ainda não existir
    if not os.path.exists(caminho_zip):
        print(f"Baixando {nome}...")
        hf_hub_download(
            repo_id="neis-lab/mmcows",
            repo_type="dataset",
            local_dir=pasta_projeto,
            filename=nome,
        )
    else:
        print(f"{nome} já existe, pulando o download.")

    # 4. Descompactar o zip dentro da pasta de dados brutos
    print(f"Descompactando {nome}...")
    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        zip_ref.extractall(pasta_projeto)

print("Extração concluída.")
"""
