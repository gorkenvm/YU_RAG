import os
import pandas as pd
import json
from YU_functions import get_embeddings, export_to_json
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]  = os.getenv("GEMINI_API_KEY")

# Load the data
with open(r'data\duyurular_aiicerik.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# 'Özet:' kelimesini 'aiicerik' sütunundan kaldır
data = [
    {**duyuru, 'aiicerik': duyuru['aiicerik'].replace('Özet:', '', 1).strip()}
    if 'Özet:' in duyuru['aiicerik'] else duyuru
    for duyuru in data
]

embeddings = []

for idx, duyuru in enumerate(data, start=1):
    print(f"Processing: {duyuru['baslik']}")
    baslik_embedding = get_embeddings(duyuru['baslik'],tech='GPT')
    aiicerik_embedding = get_embeddings(duyuru['aiicerik'], tech='GPT')
    embeddings.append({
        'id': idx,
        'baslik_embedding': baslik_embedding,
        'aiicerik_embedding': aiicerik_embedding,
        'tarih': duyuru['tarih'],
        'link': duyuru['link'],
        'baslik': duyuru['baslik'],
        'aiicerik': duyuru['aiicerik'],
    })



export_to_json(embeddings, r'data/vectorDatasetDuyurular.json')





    







