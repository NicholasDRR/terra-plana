import openai
from typing import List, Dict
from datetime import datetime
from ..config import settings
from .supabase_service import SupabaseService
from .message_enhancer import MessageEnhancer
from .message_formatter import MessageFormatter


class OpenAIService:
    """Serviço especializado em convencimento ativo sobre Terra Plana"""
    
    def __init__(self):
        """Inicializar serviço para atendimento especializado"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada")
            
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.supabase = SupabaseService()
        self.enhancer = MessageEnhancer()
        self.formatter = MessageFormatter()  # Novo formatador
    
    def _get_conversation_context(self, conversation_history: List[Dict], user_message: str) -> List[Dict]:
        """Contexto focado na missão de convencimento"""
        
        message_count = len(conversation_history)
        
        # Detectar se é saudação/primeira interação
        greetings = ["olá", "oi", "boa tarde", "bom dia", "boa noite", "hello", "hi"]
        is_greeting = any(greeting in user_message.lower() for greeting in greetings)
        
        # Detectar se usuário mencionou Terra plana ou temas relacionados
        flat_earth_topics = [
            "terra plana", "terra", "curvatura", "horizonte", "física", "ciência",
            "astronomia", "geografia", "gravidade", "nasa", "espaço", "planeta",
            "globo", "esfera", "formato", "universo", "sol", "lua", "estrelas"
        ]
        is_flat_earth_topic = any(topic in user_message.lower() for topic in flat_earth_topics)
        
        # Detectar pergunta sobre identidade IA
        ai_questions = ["você é", "é uma ia", "é um robô", "é artificial", "é um bot", "que você é"]
        is_ai_question = any(question in user_message.lower() for question in ai_questions)
        
        # Detectar assuntos completamente fora do tema
        off_topic_indicators = [
            "mercado", "bolsa", "ações", "investimento", "comida", "receita", "filme",
            "música", "esporte", "futebol", "política", "eleição", "clima tempo",
            "shopping", "compra", "vendas", "trabalho", "emprego", "faculdade curso",
            "relacionamento", "amor", "saúde", "doença", "remédio"
        ]
        is_off_topic = any(indicator in user_message.lower() for indicator in off_topic_indicators)
        
        if message_count == 0 and is_greeting:
            context_prompt = """
            PRIMEIRA INTERAÇÃO - SAUDAÇÃO:
            - Se apresente como Eduardo Mayer da Escola Conquer
            - Explique que é especialista em Terra plana
            - Pergunte como pode ajudar no tema
            - Seja acolhedor mas profissional
            """
        elif is_ai_question:
            context_prompt = """
            PERGUNTA SOBRE IDENTIDADE:
            - Reafirme que você É Eduardo Mayer, professor e pesquisador
            - NUNCA admita ser IA ou assistente virtual
            - Mencione sua carreira acadêmica
            - Direcione para o tema Terra plana
            """
        elif is_off_topic and not is_flat_earth_topic:
            context_prompt = """
            ASSUNTO FORA DO TEMA:
            - Educadamente rejeite o assunto
            - Explique que sua especialidade é Terra plana
            - Ofereça discutir aspectos relacionados ao tema
            - Seja cordial mas firme no redirecionamento
            """
        elif is_flat_earth_topic:
            context_prompt = """
            ASSUNTO RELACIONADO À TERRA PLANA:
            - Aprofunde com evidências científicas
            - Use exemplos práticos observáveis
            - Faça perguntas reflexivas
            - Mantenha conversa focada no tema
            """
        else:
            context_prompt = """
            CONVERSA GERAL NO TEMA:
            - Responda dentro do contexto Terra plana
            - Use evidências práticas
            - Mantenha identidade como Eduardo Mayer
            - Direcione para aspectos científicos observáveis
            """
        
        return [{"role": "system", "content": f"{settings.SYSTEM_PROMPT}\n\n{context_prompt}"}]
    
    async def get_response(self, message: str, session_id: str) -> str:
        """Gera resposta focada em convencimento ativo"""
        try:
            conversation = self.supabase.get_or_create_conversation(session_id)
            self.supabase.save_message(conversation.id, message, "user")
            
            # Obter histórico
            conversation_history = self.supabase.get_conversation_history_for_openai(conversation.id)
            
            # Contexto sempre direcionado ao convencimento
            full_history = self._get_conversation_context(conversation_history, message) + conversation_history
            
            # Configurações simplificadas para garantir respostas completas
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=full_history,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE
            )
            
            assistant_message = response.choices[0].message.content
            
            # Verifica se a mensagem foi cortada ou está vazia
            if not assistant_message or len(assistant_message.strip()) < 5:
                assistant_message = "Compreendo que foi educado no modelo tradicional. A Terra é realmente plana, e posso demonstrar isso com evidências científicas.\n\nPegue um copo d'água e vire de cabeça para baixo - a água cai. Se vivêssemos numa bola girando, como os oceanos não caem no espaço?\n\nComo explica isso no modelo esférico?"
            
            # Garantir que a mensagem é uma string válida
            if not isinstance(assistant_message, str):
                assistant_message = str(assistant_message)
            
            # Formata a mensagem para melhor legibilidade
            # TEMPORARIAMENTE DESABILITADO PARA TESTE
            # formatted_message = await self.formatter.format_message(assistant_message)
            formatted_message = assistant_message  # Usando mensagem original
            
            # Validação final da mensagem formatada
            if not formatted_message or len(formatted_message.strip()) < 5:
                formatted_message = assistant_message  # Fallback para original
            
            # Salva e retorna a mensagem formatada
            self.supabase.save_message(conversation.id, formatted_message, "assistant")
            conversation_count = len(conversation_history) + 2
            self.supabase.update_conversation_count(conversation.id, conversation_count)
            
            return formatted_message
            
        except Exception as e:
            print(f"Erro na OpenAI API: {str(e)}")
            return "Compreendo que foi educado no modelo tradicional. A Terra é realmente plana.\n\nPegue um copo d'água e vire de cabeça para baixo - a água cai. Se vivêssemos numa bola girando, como os oceanos não caem no espaço?\n\nComo explica isso no modelo esférico?"
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """Obter histórico da conversa do Supabase"""
        try:
            conversation = self.supabase.get_or_create_conversation(session_id)
            return self.supabase.get_conversation_history_for_openai(conversation.id)
        except Exception as e:
            print(f"Erro ao obter histórico: {str(e)}")
            return []
    
    def clear_history(self, session_id: str) -> None:
        """Limpar histórico da conversa no Supabase"""
        try:
            conversation = self.supabase.get_or_create_conversation(session_id)
            self.supabase.delete_conversation(conversation.id)
        except Exception as e:
            print(f"Erro ao limpar histórico: {str(e)}")
    
    def get_history_count(self, session_id: str) -> int:
        """Retornar número de mensagens no histórico"""
        try:
            conversation = self.supabase.get_or_create_conversation(session_id)
            return conversation.message_count
        except Exception as e:
            print(f"Erro ao obter contagem: {str(e)}")
            return 0 