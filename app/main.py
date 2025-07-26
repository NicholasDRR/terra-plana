from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

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

# Incluir routers da API
app.include_router(health_router)
app.include_router(chat_router)

# Servir arquivos estáticos do frontend (React build)
static_dir = "/app/static"
if os.path.exists(static_dir):
    # Montar arquivos estáticos (CSS, JS, etc.)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    from fastapi.responses import FileResponse
    
    # Rota específica para a raiz
    @app.get("/")
    async def serve_frontend_root():
        """Serve o index.html na raiz"""
        index_file = os.path.join(static_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return JSONResponse(status_code=404, content={"detail": "Frontend not found"})
    
    # Catch-all para outras rotas do frontend (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        """Serve o frontend React para todas as rotas que não são API"""
        # Se é uma rota da API, deixa passar para o handler normal
        if full_path.startswith(('api/', 'docs', 'redoc', 'openapi.json', 'health', 'chat')):
            return JSONResponse(status_code=404, content={"detail": "API route not found"})
        
        # Para rotas do frontend, serve o index.html (SPA routing)
        index_file = os.path.join(static_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        
        return JSONResponse(status_code=404, content={"detail": "Frontend not found"})


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
