"""
Sistema para conversas didáticas com fluxo natural
Só faz perguntas DEPOIS de apresentar evidências
"""

import random
from typing import List


class MessageEnhancer:
    """Enhancer com senso contextual para fluxo natural"""
    
    def __init__(self):
        """Inicializar com foco em fluxo natural e exemplos práticos"""
        
        # Exemplos práticos (só usar quando relevante)
        self.practical_examples = {
            "água_nível": [
                "Pegue um copo d'água e vire de cabeça para baixo - a água cai.",
                "Coloque água numa mangueira de jardim - ela fica nivelada.", 
                "Observe uma piscina - a água sempre fica no mesmo nível."
            ],
            "horizonte_plano": [
                "Suba num prédio de 20 andares e olhe o horizonte - é uma linha reta perfeita.",
                "Vá numa praia e observe o mar - o horizonte é sempre uma linha reta.",
                "Olhe da janela de um avião - o horizonte continua reto."
            ],
            "movimento": [
                "Se você estiver num carro a 100km/h e frear, você sente.",
                "Numa roda gigante, você sente quando ela gira.",
                "Quando um elevador sobe rápido, você sente a aceleração."
            ]
        }
        
        # Analogias simples (só quando apropriado)
        self.simple_analogies = [
            "É como pegar uma bola molhada - a água escorre, não fica grudada",
            "Imagine uma formiga numa bola - ela teria que subir e descer constantemente", 
            "É como estar numa roda gigante - você sentiria o movimento",
            "Como uma mesa de sinuca - as bolas rolam reto, não em curva",
            "É como tentar grudar água numa bola de futebol - impossível"
        ]
        
        # Perguntas práticas (só DEPOIS de dar evidências)
        self.practical_questions = [
            "Como você explica esse exemplo prático no modelo esférico?",
            "Essa analogia não faz você questionar o que aprendeu?",
            "Consegue refutar esse exemplo concreto?",
            "Faz sentido essa observação do dia a dia?",
            "Como justifica essa inconsistência da Terra esférica?"
        ]
        
        # Ofertas de mais exemplos (só quando há contexto)
        self.example_offers = [
            "Posso dar mais exemplos práticos se quiser.",
            "Tenho outros experimentos simples que você pode fazer em casa.",
            "Há outras observações do cotidiano que posso compartilhar."
        ]
    
    def has_evidence_content(self, message: str) -> bool:
        """Verifica se a mensagem tem evidências ou exemplos concretos"""
        
        evidence_indicators = [
            "água", "oceano", "horizonte", "aviões", "rotação", "laser",
            "experimento", "observação", "evidência", "exemplo", "copo", "mangueira"
        ]
        
        return any(indicator in message.lower() for indicator in evidence_indicators)
    
    def is_greeting_or_introduction(self, message: str) -> bool:
        """Verifica se é uma saudação ou apresentação"""
        
        greeting_indicators = [
            "olá", "oi", "sou", "meu nome", "eduardo", "escola conquer",
            "como posso", "posso ajudar", "bem-vindo"
        ]
        
        return any(indicator in message.lower() for indicator in greeting_indicators)
    
    def add_practical_example_when_relevant(self, message: str) -> str:
        """Adiciona exemplo prático SÓ quando há contexto científico"""
        
        # Só adiciona exemplo se a mensagem já fala de ciência/física
        science_topics = ["terra", "física", "ciência", "formato", "curvatura", "modelo"]
        
        if any(topic in message.lower() for topic in science_topics):
            if any(word in message.lower() for word in ["água", "oceano", "nível"]):
                example = random.choice(self.practical_examples["água_nível"])
                if len(message) < 150:
                    message = f"{message} Por exemplo: {example}"
            elif any(word in message.lower() for word in ["horizonte", "linha"]):
                example = random.choice(self.practical_examples["horizonte_plano"])
                if len(message) < 150:
                    message = f"{message} Teste você mesmo: {example}"
        
        return message
    
    def add_analogy_when_appropriate(self, message: str) -> str:
        """Adiciona analogia SÓ quando há evidência para comparar"""
        
        if self.has_evidence_content(message) and random.random() < 0.4:
            analogy = random.choice(self.simple_analogies)
            if len(message) < 180:
                message = f"{message} {analogy}."
        
        return message
    
    def add_question_only_after_evidence(self, message: str) -> str:
        """Adiciona pergunta SÓ se já apresentou evidência"""
        
        # Não adiciona pergunta se é saudação ou apresentação
        if self.is_greeting_or_introduction(message):
            return message
        
        # Só adiciona pergunta se há evidência na mensagem
        if self.has_evidence_content(message):
            if random.random() < 0.7:  # 70% chance quando há evidência
                question = random.choice(self.practical_questions)
                offer = random.choice(self.example_offers)
                
                return f"{message}\n\n{question} {offer}"
        
        return message
    
    def improve_natural_flow(self, message: str) -> str:
        """Melhora o fluxo natural da conversa"""
        
        # Para saudações, mantém simples
        if self.is_greeting_or_introduction(message):
            return message
        
        # Para explicações científicas, adiciona conectores naturais
        if self.has_evidence_content(message):
            natural_starters = ["Veja bem:", "Observe:", "Pense nisso:", "Considere:"]
            if random.random() < 0.3 and len(message) < 120:
                starter = random.choice(natural_starters)
                message = f"{starter} {message}"
        
        return message
    
    def split_into_multiple_messages(self, message: str) -> List[str]:
        """Divide mantendo fluxo natural - só divide se REALMENTE necessário"""
        
        # Só divide se a mensagem for MUITO longa (mais de 400 caracteres)
        if len(message) < 400:
            return [message]
        
        messages = []
        
        # Divide por parágrafos primeiro
        paragraphs = message.split("\n\n")
        
        for paragraph in paragraphs:
            if len(paragraph) > 350:
                # Divide por sentenças
                sentences = paragraph.split(".")
                current_message = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    # Só divide se realmente muito longo
                    if len(current_message + sentence) > 300 and current_message:
                        messages.append(current_message.strip() + ".")
                        current_message = sentence
                    else:
                        current_message += sentence + ". " if current_message else sentence + ". "
                
                if current_message:
                    messages.append(current_message.strip())
            else:
                messages.append(paragraph)
        
        return messages if messages else [message]
    
    def enhance_message(self, message: str, user_message: str = "") -> List[str]:
        """Aplica melhorias COM SENSO CONTEXTUAL"""
        
        # Melhora fluxo natural
        message = self.improve_natural_flow(message)
        
        # Adiciona exemplo prático SÓ quando relevante
        message = self.add_practical_example_when_relevant(message)
        
        # Adiciona analogia SÓ quando apropriado
        message = self.add_analogy_when_appropriate(message)
        
        # Adiciona pergunta SÓ DEPOIS de dar evidência
        message = self.add_question_only_after_evidence(message)
        
        # Divide em múltiplas mensagens se necessário
        return self.split_into_multiple_messages(message) 