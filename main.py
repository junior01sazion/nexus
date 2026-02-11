import os
import uvicorn
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tenta carregar o cérebro que você fez no Colab
try:
    vectorizer = joblib.load('vetorizador_nexus.pkl')
    model = joblib.load('modelo_nexus.pkl')
    model_ready = True
except Exception as e:
    print(f"Erro ao carregar modelo: {e}")
    model_ready = False

class Pergunta(BaseModel):
    texto: str
    contexto_financeiro: float = 0.0

@app.post("/perguntar")
async def responder(dados: Pergunta):
    txt = dados.texto.lower()
    
    # Se o modelo do Colab estiver carregado, usamos ele!
    if model_ready:
        try:
            vetor = vectorizer.transform([txt])
            previsao = model.predict(vetor)[0]
            return {"resposta": previsao}
        except:
            return {"resposta": "Erro ao processar sua pergunta técnica."}
    
    # Resposta de emergência caso o arquivo .pkl falhe
    return {"resposta": "Estou online, mas não encontrei meu treinamento de motores. Verifique os arquivos .pkl!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
