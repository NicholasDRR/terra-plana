-- Script para configurar tabelas no Supabase
-- Execute este script no SQL Editor do Supabase

-- Tabela de conversas
CREATE TABLE IF NOT EXISTS conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    message_count INTEGER DEFAULT 0
);

-- Tabela de mensagens
CREATE TABLE IF NOT EXISTS messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at
CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON conversations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Políticas de segurança (RLS - Row Level Security)
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (para desenvolvimento)
-- Em produção, você deve implementar autenticação adequada
CREATE POLICY "Allow all operations on conversations" ON conversations
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on messages" ON messages
    FOR ALL USING (true);

-- Comentários para documentação
COMMENT ON TABLE conversations IS 'Tabela para armazenar conversas por sessão';
COMMENT ON TABLE messages IS 'Tabela para armazenar mensagens das conversas';
COMMENT ON COLUMN conversations.session_id IS 'ID único da sessão do usuário';
COMMENT ON COLUMN messages.role IS 'Role da mensagem: user, assistant, ou system'; 