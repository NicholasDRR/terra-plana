"""
API para chat com IA especializada em Terra plana
Inclui funcionalidades de texto e áudio
"""

from fastapi import APIRouter, HTTPException, Header, UploadFile, File
from fastapi.responses import FileResponse
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid
import os
from ..services.openai_service import OpenAIService
from ..services.message_formatter import MessageFormatter
from ..services.audio_service import AudioService
from ..models.chat import ChatMessage, ApiResponse

router = APIRouter(prefix="/chat", tags=["chat"])

# Instância global dos serviços
openai_service = OpenAIService()
message_formatter = MessageFormatter()
audio_service = AudioService()

# Cache temporário para arquivos de áudio gerados
audio_cache = {}


def get_session_id(x_session_id: Optional[str]) -> str:
    """Gerar ou usar session_id existente"""
    return x_session_id if x_session_id else str(uuid.uuid4())


@router.post("/format", response_model=Dict[str, Any])
async def format_message_endpoint(request: Dict[str, Any]):
    """
    Endpoint para testar formatação de mensagens
    """
    try:
        message = request.get("message", "").strip()
        
        if not message:
            raise HTTPException(
                status_code=400, 
                detail="Mensagem não pode estar vazia"
            )
        
        # Formata a mensagem
        formatted_message = await message_formatter.format_message(message)
        
        return {
            "original_message": message,
            "formatted_message": formatted_message,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno do servidor: {str(e)}"
        )


@router.post("/", response_model=Dict[str, Any])
async def send_message(
    request: Dict[str, Any],
    x_session_id: Optional[str] = Header(None)
):
    """
    Enviar mensagem para o chat e receber resposta da IA
    """
    try:
        message = request.get("message", "").strip()
        session_id = get_session_id(x_session_id)
        
        if not message:
            raise HTTPException(
                status_code=400, 
                detail="Mensagem não pode estar vazia"
            )
        
        # Obter resposta da OpenAI (sempre string simples)
        ai_response = await openai_service.get_response(message, session_id)
        
        # Sempre retorna resposta simples
        return {
            "message": ai_response,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno do servidor: {str(e)}"
        )


@router.post("/continue", response_model=Dict[str, Any])
async def continue_conversation(
    request: Dict[str, Any],
    x_session_id: Optional[str] = Header(None)
):
    """
    Continuar enviando mensagens de uma conversa múltipla
    Simula o comportamento de uma pessoa enviando várias mensagens
    """
    try:
        session_id = get_session_id(x_session_id)
        message_index = request.get("message_index", 1)
        
        # Esta é uma funcionalidade placeholder 
        # Na implementação real, você manteria as mensagens em cache/sessão
        # Por simplicidade, vou retornar uma mensagem padrão
        
        follow_up_messages = [
            "Quer que eu explique melhor algum ponto específico?",
            "Posso dar mais detalhes sobre qualquer um desses tópicos.",
            "O que mais desperta sua curiosidade?"
        ]
        
        if message_index < len(follow_up_messages):
            return {
                "message": follow_up_messages[message_index],
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "has_more": message_index < len(follow_up_messages) - 1,
                "current_index": message_index
            }
        else:
            return {
                "message": "Como posso ajudar mais?",
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "has_more": False
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao continuar conversa: {str(e)}"
        )


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_chat_history(
    x_session_id: Optional[str] = Header(None)
):
    """
    Obter histórico completo da conversa
    """
    try:
        session_id = get_session_id(x_session_id)
        history = openai_service.get_conversation_history(session_id)
        
        messages = []
        for msg in history:
            message_obj = ChatMessage(
                id=str(uuid.uuid4()),
                content=msg["content"],
                role=msg["role"],
                timestamp=datetime.now()
            )
            messages.append(message_obj.to_dict())
        
        return messages
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao recuperar histórico: {str(e)}"
        )


@router.delete("/history", response_model=Dict[str, Any])
async def clear_chat_history(
    x_session_id: Optional[str] = Header(None)
):
    """
    Limpar histórico da conversa
    """
    try:
        session_id = get_session_id(x_session_id)
        openai_service.clear_history(session_id)
        
        response = ApiResponse(
            message="Histórico limpo com sucesso",
            timestamp=datetime.now()
        )
        
        return response.to_dict()
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao limpar histórico: {str(e)}"
        ) 


@router.post("/audio", response_model=Dict[str, Any])
async def send_audio_message(
    audio_file: UploadFile = File(...),
    x_session_id: Optional[str] = Header(None)
):
    """
    Enviar mensagem de áudio, transcrever e receber resposta em texto + áudio
    """
    try:
        session_id = get_session_id(x_session_id)
        
        # Validar arquivo de áudio
        if not audio_file.filename:
            raise HTTPException(status_code=400, detail="Nome do arquivo não fornecido")
        
        # Ler arquivo e validar
        audio_content = await audio_file.read()
        audio_service.validate_audio_file(audio_file.filename, len(audio_content))
        
        # Transcrever áudio para texto
        import io
        audio_file_obj = io.BytesIO(audio_content)
        transcribed_text = await audio_service.transcribe_audio(audio_file_obj, audio_file.filename)
        
        if not transcribed_text or not transcribed_text.strip():
            raise HTTPException(status_code=400, detail="Não foi possível transcrever o áudio. Tente falar mais alto ou em um ambiente mais silencioso.")
        
        # Obter resposta do Eduardo para o texto transcrito
        ai_response = await openai_service.get_response(transcribed_text, session_id)
        
        # Gerar áudio da resposta
        response_audio = audio_service.text_to_speech(ai_response)
        
        # Salvar áudio em cache temporário
        audio_id = str(uuid.uuid4())
        audio_file_path = audio_service.save_audio_file(response_audio, audio_id)
        audio_cache[audio_id] = {
            "file_path": audio_file_path,
            "created_at": datetime.now(),
            "text": ai_response
        }
        
        return {
            "transcribed_text": transcribed_text,
            "response_text": ai_response,
            "audio_id": audio_id,
            "audio_url": f"/chat/audio/download/{audio_id}",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar áudio: {str(e)}"
        )


@router.get("/audio/download/{audio_id}")
async def download_audio(audio_id: str):
    """
    Download do áudio gerado
    """
    try:
        if audio_id not in audio_cache:
            raise HTTPException(status_code=404, detail="Áudio não encontrado")
        
        audio_info = audio_cache[audio_id]
        file_path = audio_info["file_path"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Arquivo de áudio não encontrado")
        
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=f"eduardo_response_{audio_id}.mp3"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao baixar áudio: {str(e)}"
        )


@router.get("/audio/voices", response_model=List[Dict[str, str]])
async def get_available_voices():
    """
    Listar vozes disponíveis no ElevenLabs
    """
    try:
        voices = audio_service.get_available_voices()
        return voices
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao obter vozes: {str(e)}"
        )


@router.delete("/audio/cache")
async def clear_audio_cache():
    """
    Limpar cache de áudios (para manutenção)
    """
    try:
        count = 0
        for audio_id, audio_info in list(audio_cache.items()):
            try:
                if os.path.exists(audio_info["file_path"]):
                    os.unlink(audio_info["file_path"])
                del audio_cache[audio_id]
                count += 1
            except Exception as e:
                print(f"Erro ao remover áudio {audio_id}: {e}")
        
        return {"message": f"Cache limpo. {count} arquivos removidos."}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao limpar cache: {str(e)}"
        ) 