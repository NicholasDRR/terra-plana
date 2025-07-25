import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from supabase import create_client, Client

from ..config import settings
from ..models import Conversation, StoredMessage


class SupabaseService:
    """Serviço para integração com Supabase"""
    
    def __init__(self):
        """Inicializar cliente Supabase"""
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("Configurações do Supabase não encontradas")
            
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    def create_conversation(self, session_id: str) -> Conversation:
        """
        Criar nova conversa
        
        Args:
            session_id: ID da sessão do usuário
            
        Returns:
            Conversa criada
        """
        try:
            conversation_data = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message_count": 0
            }
            
            result = self.client.table("conversations").insert(conversation_data).execute()
            
            if result.data:
                data = result.data[0]
                return Conversation(
                    id=data["id"],
                    session_id=data["session_id"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    updated_at=datetime.fromisoformat(data["updated_at"]),
                    message_count=data["message_count"]
                )
            
            raise Exception("Falha ao criar conversa")
            
        except Exception as e:
            print(f"Erro ao criar conversa: {str(e)}")
            raise
    
    def get_or_create_conversation(self, session_id: str) -> Conversation:
        """
        Obter conversa existente ou criar nova
        
        Args:
            session_id: ID da sessão do usuário
            
        Returns:
            Conversa existente ou nova
        """
        try:
            # Tentar buscar conversa existente
            result = self.client.table("conversations").select("*").eq("session_id", session_id).execute()
            
            if result.data:
                data = result.data[0]
                return Conversation(
                    id=data["id"],
                    session_id=data["session_id"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    updated_at=datetime.fromisoformat(data["updated_at"]),
                    message_count=data["message_count"]
                )
            
            # Criar nova conversa se não existir
            return self.create_conversation(session_id)
            
        except Exception as e:
            print(f"Erro ao obter/criar conversa: {str(e)}")
            raise
    
    def save_message(self, conversation_id: str, content: str, role: str) -> StoredMessage:
        """
        Salvar mensagem no banco
        
        Args:
            conversation_id: ID da conversa
            content: Conteúdo da mensagem
            role: Role da mensagem (user/assistant)
            
        Returns:
            Mensagem salva
        """
        try:
            message_data = {
                "conversation_id": conversation_id,
                "content": content,
                "role": role,
                "timestamp": datetime.now().isoformat()
            }
            
            result = self.client.table("messages").insert(message_data).execute()
            
            if result.data:
                data = result.data[0]
                return StoredMessage(
                    id=data["id"],
                    conversation_id=data["conversation_id"],
                    content=data["content"],
                    role=data["role"],
                    timestamp=datetime.fromisoformat(data["timestamp"])
                )
            
            raise Exception("Falha ao salvar mensagem")
            
        except Exception as e:
            print(f"Erro ao salvar mensagem: {str(e)}")
            raise
    
    def get_conversation_messages(self, conversation_id: str) -> List[StoredMessage]:
        """
        Obter todas as mensagens de uma conversa
        
        Args:
            conversation_id: ID da conversa
            
        Returns:
            Lista de mensagens ordenadas por timestamp
        """
        try:
            result = self.client.table("messages").select("*").eq("conversation_id", conversation_id).order("timestamp").execute()
            
            messages = []
            for data in result.data:
                message = StoredMessage(
                    id=data["id"],
                    conversation_id=data["conversation_id"],
                    content=data["content"],
                    role=data["role"],
                    timestamp=datetime.fromisoformat(data["timestamp"])
                )
                messages.append(message)
            
            return messages
            
        except Exception as e:
            print(f"Erro ao obter mensagens: {str(e)}")
            return []
    
    def update_conversation_count(self, conversation_id: str, count: int) -> None:
        """
        Atualizar contador de mensagens da conversa
        
        Args:
            conversation_id: ID da conversa
            count: Novo número de mensagens
        """
        try:
            self.client.table("conversations").update({
                "message_count": count,
                "updated_at": datetime.now().isoformat()
            }).eq("id", conversation_id).execute()
            
        except Exception as e:
            print(f"Erro ao atualizar conversa: {str(e)}")
    
    def delete_conversation(self, conversation_id: str) -> None:
        """
        Deletar conversa e todas suas mensagens
        
        Args:
            conversation_id: ID da conversa
        """
        try:
            # Deletar mensagens primeiro
            self.client.table("messages").delete().eq("conversation_id", conversation_id).execute()
            
            # Deletar conversa
            self.client.table("conversations").delete().eq("id", conversation_id).execute()
            
        except Exception as e:
            print(f"Erro ao deletar conversa: {str(e)}")
            raise
    
    def get_conversation_history_for_openai(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Obter histórico formatado para OpenAI API
        
        Args:
            conversation_id: ID da conversa
            
        Returns:
            Lista de mensagens no formato OpenAI
        """
        messages = self.get_conversation_messages(conversation_id)
        
        # Converter para formato OpenAI
        openai_messages = []
        for message in messages:
            openai_messages.append({
                "role": message.role,
                "content": message.content
            })
        
        return openai_messages 