import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permite que seu site fale com a IA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    texto: str
    contexto_financeiro: float = 0.0

@app.post("/perguntar")
async def responder(dados: Pergunta):
    txt = dados.texto.lower()
    
    # Resposta inteligente baseada no lucro que o PHP enviou
    if any(w in txt for w in ["lucro", "faturamento", "ganhei", "dinheiro"]):
        return {"resposta": f"Jailson, verifiquei aqui e o seu faturamento atual no Laboratório Cinética é de R$ {dados.contexto_financeiro:.2f}. Como posso ajudar a aumentar esse valor?"}
    
    if any(w in txt for w in ["quem é você", "o que você faz", "nexus"]):
        return {"resposta": "Eu sou o Nexus, seu copiloto de inteligência artificial. Eu monitoro seu estoque, financeiro e ajudo na gestão da sua oficina!"}

    return {"resposta": "Recebi sua mensagem! Estou pronto para analisar seus dados. O que mais você gostaria de saber?"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)