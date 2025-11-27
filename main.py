from fastapi import FastAPI
from app.controllers import rh_controller, geo_controller, evento_controller, inscricao_controller, campus_controller, curso_controller, curso_campus_controller

app = FastAPI(
    title="Vainobus API",
    version="1.0.0",
    description="API para gerenciamento de eventos de transporte de alunos"
)

app.include_router(rh_controller.router)
app.include_router(geo_controller.router)
app.include_router(evento_controller.router)
app.include_router(inscricao_controller.router)
app.include_router(campus_controller.router)
app.include_router(curso_controller.router)
app.include_router(curso_campus_controller.router)


@app.get("/")
def root():
    return {"message": "API Vainobus - Gerenciamento de Eventos de Transporte"}
