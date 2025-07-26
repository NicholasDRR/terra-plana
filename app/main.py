from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import os
from pathlib import Path

from .config import settings
from .routers import chat_router, health_router

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Middleware de debug
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Requisição recebida: {request.method} {request.url}")
    logging.info(f"Headers: {dict(request.headers)}")
    logging.info(f"Origin: {request.headers.get('origin', 'N/A')}")
    
    response = await call_next(request)
    
    logging.info(f"Resposta: {response.status_code}")
    return response

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Incluir routers
app.include_router(health_router)
app.include_router(chat_router)

# Servir arquivos estáticos do React (se existirem)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Servir index.html para rotas do React
    @app.get("/")
    async def serve_react_app():
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"message": "React app not found"}
    
    @app.get("/{full_path:path}")
    async def serve_react_routes(full_path: str):
        # Se não for uma rota da API, servir index.html (SPA routing)
        if not full_path.startswith(("api", "chat", "health", "docs", "openapi", "static")):
            index_path = static_dir / "index.html"
            if index_path.exists():
                return FileResponse(str(index_path))
        return {"message": "Route not found"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global para exceções não tratadas"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Erro interno do servidor: {str(exc)}",
            "type": "internal_server_error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=True
    )
