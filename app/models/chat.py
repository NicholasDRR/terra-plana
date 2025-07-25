from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class MessageRequest:
    """Modelo para requisição de mensagem"""
    message: str


@dataclass
class ChatMessage:
    """Modelo para mensagem do chat"""
    id: str
    content: str
    role: str  # "user" ou "assistant"
    timestamp: datetime
    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ChatResponse:
    """Modelo para resposta do chat"""
    message: str
    timestamp: datetime
    
    def to_dict(self):
        return {
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ApiResponse:
    """Modelo para resposta genérica da API"""
    message: str
    timestamp: datetime
    status: str = "success"
    
    def to_dict(self):
        return {
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status
        }


@dataclass
class Conversation:
    """Modelo para conversa persistente"""
    id: Optional[str] = None
    session_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    message_count: int = 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "message_count": self.message_count
        }


@dataclass
class StoredMessage:
    """Modelo para mensagem armazenada no Supabase"""
    id: Optional[str] = None
    conversation_id: Optional[str] = None
    content: str = ""
    role: str = ""
    timestamp: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        } 