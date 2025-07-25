from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

from ..config import settings

router = APIRouter(tags=["health"])


@router.get("/", response_model=Dict[str, Any])
async def root():
    """
    Endpoint raiz da API
    
    Returns:
        Informações básicas da API
    """
    return {
        "message": f"{settings.API_TITLE} está funcionando",
        "version": settings.API_VERSION,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """
    Verificação de saúde da API
    
    Returns:
        Status da API e informações do sistema
    """
    return {
        "status": "healthy",
        "api": settings.API_TITLE,
        "version": settings.API_VERSION,
        "timestamp": datetime.now().isoformat(),
        "openai_configured": bool(settings.OPENAI_API_KEY)
    } 