import os
import uvicorn
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permite que o seu site (PHP) fale com esta IA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CARREGANDO O CÉREBRO QUE VOCÊ TREINOU NO COLAB ---
# O joblib abre os arquivos .pkl que você subiu
try:
    vectorizer = joblib.load('vetorizador_nexus.pkl')
    model = joblib.load('modelo_nexus.pkl')
    print("✅ IA do Laboratório Cinética carregada com sucesso!")
except:
    print("❌ Erro ao carregar os arquivos .pkl. Verifique se os nomes estão corretos.")

class Pergunta(BaseModel):
    texto: str
    contexto_financeiro: float = 0.0

@app.post("/perguntar")
async def responder(dados: Pergunta):
    try:
        # 1. Transforma a pergunta do usuário em números
        pergunta_vetorizada = vectorizer.transform([dados.texto])
        
        # 2. A IA decide a melhor resposta baseada no treino
        resposta_ia = model.predict(pergunta_vetorizada)[0]
        
        return {"resposta": resposta_ia}
    except:
        return {"resposta": "Desculpe Jailson, tive um problema ao processar isso. Tente novamente!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
