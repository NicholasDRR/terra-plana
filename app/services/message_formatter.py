"""
Serviço para formatação de mensagens usando OpenAI
Torna mensagens mais legíveis e organizadas
"""

import openai
from ..config import settings


class MessageFormatter:
    """Formatador de mensagens para melhor legibilidade"""
    
    def __init__(self):
        """Inicializar serviço de formatação"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada")
            
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Prompt específico para formatação
        self.formatting_prompt = """Você é um assistente especialista em formatação de texto para melhor legibilidade.

Sua tarefa é receber um texto e reformatá-lo para torná-lo mais claro, organizado e fácil de ler.

### Regras de Formatação:

1. **Organização em Parágrafos**:
   - Quebrar textos longos em parágrafos menores de 2-3 frases
   - Cada nova ideia deve começar em novo parágrafo
   - Use quebras de linha duplas (\n\n) entre parágrafos diferentes

2. **Estrutura com Tópicos**:
   - Se o texto apresenta múltiplos pontos, organize em tópicos
   - Use marcadores simples (-) para listas
   - Coloque cada item da lista em linha separada

3. **Perguntas e Reflexões**:
   - Sempre separe perguntas em seus próprios parágrafos
   - Coloque perguntas no final de seções quando possível
   - Use quebra de linha antes de perguntas importantes

4. **Exemplos Práticos**:
   - Destaque exemplos práticos em parágrafos separados
   - Use frases como "Por exemplo:" ou "Observe:"
   - Mantenha exemplos claros e diretos

5. **Fluxo de Leitura**:
   - Mantenha transições suaves entre ideias
   - Use conectores apropriados ("Além disso", "Por outro lado", etc.)
   - Preserve o tom e contexto original completamente

### Formato de Saída:
- Use quebras de linha simples (\n) dentro de parágrafos
- Use quebras de linha duplas (\n\n) entre parágrafos  
- Mantenha a linguagem exatamente igual ao original
- NÃO adicione ou remova informações
- NÃO use markdown, asteriscos ou formatação especial
- Apenas texto simples com quebras de linha

### Exemplo de Formatação:

ANTES:
"Texto longo sem quebras falando sobre várias coisas diferentes em sequência sem organização adequada para leitura."

DEPOIS:
"Primeira ideia bem organizada em parágrafo curto.

Segunda ideia em parágrafo separado com quebra de linha.

Terceira ideia também organizada de forma clara."

### O que NÃO fazer:
- NÃO altere palavras, frases ou significado
- NÃO adicione informações novas
- NÃO remova conteúdo importante
- NÃO use símbolos especiais ou markdown
- NÃO altere exemplos práticos ou dados técnicos

### Objetivo:
Retornar APENAS o texto reformatado com quebras de linha adequadas para facilitar a leitura."""

    async def format_message(self, message: str) -> str:
        """Formata mensagem para melhor legibilidade"""
        try:
            if not message or len(message.strip()) < 50:
                # Se a mensagem é muito curta, retorna sem formatação
                return message
            
            # Chama OpenAI para formatação
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.formatting_prompt},
                    {"role": "user", "content": f"Formate este texto para melhor legibilidade:\n\n{message}"}
                ],
                max_tokens=1000,
                temperature=0.3  # Baixa criatividade para manter fidelidade
            )
            
            formatted_message = response.choices[0].message.content
            
            # Verifica se a formatação foi bem-sucedida
            if formatted_message and len(formatted_message.strip()) > 10:
                return formatted_message.strip()
            else:
                # Se houve problema, retorna mensagem original
                return message
                
        except Exception as e:
            print(f"Erro na formatação: {str(e)}")
            # Em caso de erro, retorna mensagem original
            return message 