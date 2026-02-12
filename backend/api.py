from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
from src.database import LeadManager
from src.scraper import GoogleMapsScraper
from src.sender import WhatsappSender
from src.monitor import WhatsappMonitor
from src.utils import PhoneCleaner

app = FastAPI(title="Oryon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    term: str
    limit: int = 5

class SendRequest(BaseModel):
    limit: int = 3

# Variável global para evitar abrir 2 monitores ao mesmo tempo
monitor_thread = None

@app.get("/")
def read_root():
    return {"status": "Oryon Online 🦁"}

@app.get("/leads")
def get_leads():
    db = LeadManager("data/oryon.db")
    conn = db.conn
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY id DESC")
    columns = [desc[0] for desc in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

@app.post("/scrape")
def run_scraper(request: SearchRequest):
    try:
        scraper = GoogleMapsScraper()
        scraper.search(request.term, limit=request.limit)
        return {"message": "Garimpo finalizado!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send")
def run_sender(request: SendRequest):
    try:
        sender = WhatsappSender()
        sender.enviar_fila(limite_envios=request.limit)
        return {"message": "Disparos finalizados!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NOVA ROTA DO MONITOR ---
@app.post("/monitor")
def start_monitor():
    global monitor_thread
    
    # Se já tiver um rodando, avisa (simples)
    if monitor_thread and monitor_thread.is_alive():
        return {"message": "O Monitor já está rodando em segundo plano!"}

    def run_vigilia():
        # Essa função roda isolada
        try:
            mon = WhatsappMonitor()
            mon.iniciar_vigilia()
        except Exception as e:
            print(f"Erro no monitor: {e}")

    # Cria e inicia a Thread
    monitor_thread = threading.Thread(target=run_vigilia)
    monitor_thread.daemon = True # Fecha se o programa principal fechar
    monitor_thread.start()
    
    return {"message": "Monitoramento iniciado! Aumente o volume do PC."}