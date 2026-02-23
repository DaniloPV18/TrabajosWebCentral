from fastapi import FastAPI, BackgroundTasks
from schemas.log_schema import LogRequest
from services.log_services import LoggerService # Asegúrate que termine en 's'

app = FastAPI()
_service = LoggerService()

@app.post("/escribir-log")
async def escribir(request: LogRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_service.execute_logging, request)
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "online", "service": "logs-central"}