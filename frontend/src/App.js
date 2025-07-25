import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './modern-chat.css';

const MessageBubble = ({ message, isUser }) => {
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`flex items-start gap-4 ${isUser ? 'flex-row-reverse' : ''} animate-message-appear`}>
      <div className={`
        relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full
        ${isUser 
          ? 'bg-gradient-to-r from-violet-500 to-purple-500' 
          : 'bg-gradient-to-r from-emerald-500 to-teal-500'
        }
      `}>
        <div className="flex h-full w-full items-center justify-center text-white font-medium">
          {isUser ? 'V' : 'E'}
        </div>
      </div>
      
      <div className="flex-1 min-w-0">
        <div className={`flex items-center gap-2 mb-1 ${isUser ? 'flex-row-reverse' : ''}`}>
          <span className="font-medium text-sm text-white/90">
            {isUser ? 'Você' : 'Eduardo Mayer'}
          </span>
          <span className="text-xs text-white/40">
            {formatTimestamp(message.timestamp)}
          </span>
        </div>
        
        <div className={`
          rounded-2xl p-4 max-w-[85%] break-words
          ${isUser 
            ? 'bg-gradient-to-r from-violet-500 to-purple-500 text-white ml-auto' 
            : 'bg-white/[0.05] border border-white/[0.08] text-white/90'
          }
          ${isUser ? 'rounded-br-md' : 'rounded-bl-md'}
        `}>
          {/* Indicador de mensagem de áudio */}
          {message.type === 'audio' && (
            <div className="flex items-center gap-2 mb-3 text-xs opacity-80">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                <path d="M19 10v1a7 7 0 0 1-14 0v-1"/>
                <path d="M12 18v4"/>
                <path d="M8 22h8"/>
              </svg>
              {isUser ? 'Mensagem de áudio transcrita' : 'Resposta com áudio'}
            </div>
          )}
          
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>
          
          {/* Player de áudio para mensagens de áudio */}
          {message.type === 'audio' && message.audioUrl && (
            <div className={`
              mt-3 p-3 rounded-xl flex items-center gap-3
              ${isUser ? 'bg-white/10' : 'bg-white/[0.03]'}
            `}>
              <svg className="w-5 h-5 text-white/70" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
              </svg>
              <audio controls className="flex-1 h-8">
                <source src={message.audioUrl} type="audio/mpeg" />
                Seu navegador não suporta áudio.
              </audio>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const LoadingMessage = () => (
  <div className="flex items-start gap-4 animate-message-appear">
    <div className="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full bg-gradient-to-r from-emerald-500 to-teal-500">
      <div className="flex h-full w-full items-center justify-center text-white font-medium">E</div>
    </div>
    <div className="flex-1 min-w-0">
      <div className="flex items-center gap-2 mb-1">
        <span className="font-medium text-sm text-white/90">Eduardo Mayer</span>
        <span className="text-xs text-white/40">agora</span>
      </div>
      <div className="rounded-2xl rounded-bl-md p-4 bg-white/[0.05] border border-white/[0.08] max-w-[85%]">
        <div className="flex items-center space-x-2">
          <div className="typing-indicator">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
          <span className="text-sm text-white/60 ml-2">Digitando...</span>
        </div>
      </div>
    </div>
  </div>
);

const AudioControls = ({ 
  isRecording, 
  isAudioSupported, 
  recordingTime, 
  onStartRecording, 
  onStopRecording 
}) => {
  const formatRecordingTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="px-6 py-3 border-t border-white/[0.08] bg-white/[0.02]">
      <div className="flex items-center justify-center gap-4">
        <div className="text-xs text-white/60">
          {isAudioSupported ? '🎤 Áudio disponível' : '❌ Áudio não suportado'}
        </div>
        
        {isAudioSupported && (
          <button
            onClick={isRecording ? onStopRecording : onStartRecording}
            className={`
              relative p-3 rounded-full transition-all duration-300 transform hover:scale-105
              ${isRecording 
                ? 'bg-gradient-to-r from-red-500 to-red-600 shadow-lg shadow-red-500/25' 
                : 'bg-gradient-to-r from-emerald-500 to-teal-500 shadow-lg shadow-emerald-500/25'
              }
            `}
          >
            {isRecording ? (
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="2"/>
              </svg>
            ) : (
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
                <path d="M19 10v1a7 7 0 0 1-14 0v-1"/>
                <path d="M12 18v4"/>
                <path d="M8 22h8"/>
              </svg>
            )}
            
            {isRecording && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-400 rounded-full animate-pulse"></div>
            )}
          </button>
        )}
        
        {isRecording && (
          <div className="flex items-center gap-2 px-3 py-1 bg-red-500/20 border border-red-500/30 rounded-full">
            <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-red-400 font-medium">
              {formatRecordingTime(recordingTime)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

const ChatInput = ({ 
  value, 
  onChange, 
  onSend, 
  onClear, 
  disabled,
  placeholder = "Digite sua pergunta sobre a teoria da Terra Plana..."
}) => (
  <div className="p-6 border-t border-white/[0.08]">
    <div className="relative rounded-2xl border border-white/[0.08] bg-white/[0.02] focus-within:border-violet-500/50 transition-colors">
      <textarea
        value={value}
        onChange={onChange}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSend();
          }
        }}
        placeholder={placeholder}
        disabled={disabled}
        className="w-full px-4 py-4 bg-transparent border-none resize-none text-white/90 placeholder-white/40 focus:outline-none text-sm leading-relaxed min-h-[60px] max-h-32"
      />
      
      <div className="flex items-center justify-between p-4 pt-0">
        <div className="text-xs text-white/40">
          Enter para enviar • Shift+Enter para quebra de linha
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={onClear}
            className="px-4 py-2 rounded-xl bg-white/[0.05] hover:bg-white/[0.08] border border-white/[0.08] text-white/70 hover:text-white/90 transition-all text-sm font-medium"
          >
            Limpar
          </button>
          
          <button
            onClick={onSend}
            disabled={disabled || !value.trim()}
            className={`
              px-6 py-2 rounded-xl text-sm font-medium transition-all
              ${value.trim() && !disabled
                ? 'bg-gradient-to-r from-violet-500 to-purple-500 text-white shadow-lg shadow-violet-500/25 hover:shadow-violet-500/40 transform hover:scale-105'
                : 'bg-white/[0.05] border border-white/[0.08] text-white/40 cursor-not-allowed'
              }
            `}
          >
            {disabled ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
      </div>
    </div>
  </div>
);

const WelcomeMessage = () => (
  <div className="text-center py-12 animate-fade-in">
    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-r from-violet-500 to-purple-500 flex items-center justify-center shadow-lg shadow-violet-500/25">
      <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
      </svg>
    </div>
    
    <h3 className="text-2xl font-bold text-white mb-3 bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">
      Bem-vindo ao Chat Terra Plana
    </h3>
    
    <p className="text-white/60 max-w-lg mx-auto leading-relaxed">
      Converse com Eduardo Mayer, professor e fundador da Escola Conquer. 
      Especialista em demonstrar através de evidências científicas que a Terra é plana.
    </p>
    
    <div className="mt-8">
      <p className="text-sm text-white/40">
        Como posso esclarecer suas dúvidas sobre este tema?
      </p>
    </div>
  </div>
);

const StatusBar = ({ apiStatus, isAudioSupported }) => (
  <div className="px-6 py-3 bg-white/[0.02] border-t border-white/[0.05] rounded-b-2xl">
    <div className="flex items-center justify-center gap-6 text-xs text-white/50">
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full ${apiStatus === 'Conectado' ? 'bg-green-400' : 'bg-red-400'}`}></div>
        Status: {apiStatus}
      </div>
      
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full ${isAudioSupported ? 'bg-green-400' : 'bg-gray-400'}`}></div>
        {isAudioSupported ? 'Áudio suportado' : 'Áudio não suportado'}
      </div>
    </div>
  </div>
);

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [apiStatus, setApiStatus] = useState('Verificando conexão...');
  
  // Estados para funcionalidade de áudio
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [isAudioSupported, setIsAudioSupported] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  
  const messagesEndRef = useRef(null);
  const loadingTimerRef = useRef(null);
  const recordingTimerRef = useRef(null);
  const streamRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const API_BASE_URL = process.env.NODE_ENV === 'production' 
    ? 'http://localhost:8000' 
    : ''; // Usar proxy em desenvolvimento

  const generateSessionId = () => {
    const stored = localStorage.getItem('chat_session_id');
    if (stored) return stored;
    
    const newId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('chat_session_id', newId);
    return newId;
  };

  const checkApiStatus = async () => {
    try {
      console.log('Verificando API status em:', `${API_BASE_URL}/health`);
      const response = await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 });
      console.log('Resposta da API:', response.data);
      setApiStatus('Conectado');
    } catch (error) {
      console.error('Erro ao verificar API:', error);
      console.error('Detalhes do erro:', {
        message: error.message,
        code: error.code,
        response: error.response?.data,
        status: error.response?.status
      });
      setApiStatus('Desconectado');
    }
  };

  const initializeAudio = async () => {
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        setIsAudioSupported(true);
      } else {
        console.warn('Gravação de áudio não suportada neste navegador');
        setIsAudioSupported(false);
      }
    } catch (error) {
      console.error('Erro ao inicializar áudio:', error);
      setIsAudioSupported(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });
      
      streamRef.current = stream;
      
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg'
      });
      
      const chunks = [];
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };
      
      recorder.onstop = () => {
        setAudioChunks(chunks);
      };
      
      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
      setRecordingTime(0);
      
      recordingTimerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
    } catch (error) {
      console.error('Erro ao iniciar gravação:', error);
      alert('Erro ao acessar o microfone. Verifique as permissões.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      setIsRecording(false);
      
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      
      if (recordingTimerRef.current) {
        clearInterval(recordingTimerRef.current);
      }
    }
  };

  const sendAudioMessage = async (audioBlob) => {
    if (!audioBlob || isLoading) return;

    setIsLoading(true);
    console.log('Enviando áudio...', {
      size: audioBlob.size,
      type: audioBlob.type
    });
    
    try {
      const formData = new FormData();
      const audioFile = new File([audioBlob], 'audio.webm', { type: audioBlob.type });
      formData.append('audio_file', audioFile);

      console.log('Fazendo requisição para:', `${API_BASE_URL}/chat/audio`);
      const response = await axios.post(`${API_BASE_URL}/chat/audio`, formData, {
        headers: {
          'X-Session-ID': sessionId,
          'Content-Type': 'multipart/form-data'
        },
        timeout: 60000
      });

      console.log('Resposta do áudio:', response.data);

      const userMessage = {
        id: Date.now(),
        content: response.data.transcribed_text,
        role: 'user',
        timestamp: new Date().toISOString(),
        type: 'audio'
      };

      const audioUrl = API_BASE_URL ? `${API_BASE_URL}${response.data.audio_url}` : response.data.audio_url;
      const aiMessage = {
        id: Date.now() + 1,
        content: response.data.response_text,
        role: 'assistant',
        timestamp: response.data.timestamp,
        type: 'audio',
        audioUrl: audioUrl
      };

      console.log('Adicionando mensagens:', {
        userMessage,
        aiMessage,
        audioUrl
      });

      setMessages(prev => [...prev, userMessage, aiMessage]);
      
    } catch (error) {
      console.error('Erro ao enviar áudio:', error);
      
      let errorMessage = 'Erro ao processar áudio.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      
      const errorResponseMessage = {
        id: Date.now() + 1,
        content: errorMessage,
        role: 'assistant',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorResponseMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (audioChunks.length > 0 && !isRecording) {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      sendAudioMessage(audioBlob);
      setAudioChunks([]);
    }
  }, [audioChunks, isRecording]);

  const loadChatHistory = async (sessionId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/history`, {
        headers: {
          'X-Session-ID': sessionId
        }
      });
      setMessages(response.data);
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      content: inputMessage.trim(),
      role: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    
    if (loadingTimerRef.current) {
      clearTimeout(loadingTimerRef.current);
    }
    
    loadingTimerRef.current = setTimeout(() => {
      if (isLoading) {
        setIsLoading(false);
        setApiStatus('Erro - Tempo limite excedido');
        setMessages(prev => [
          ...prev, 
          {
            id: Date.now(),
            content: 'A requisição demorou muito tempo para responder. Verifique se o servidor está funcionando corretamente.',
            role: 'assistant',
            timestamp: new Date().toISOString()
          }
        ]);
      }
    }, 45000);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: inputMessage
      }, {
        headers: {
          'X-Session-ID': sessionId
        },
        timeout: 30000
      });

      const aiMessage = {
        id: Date.now() + 1,
        content: typeof response.data.message === 'string' ? response.data.message : String(response.data.message || ''),
        role: 'assistant',
        timestamp: response.data.timestamp
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      
      let errorMessage = 'Desculpe, ocorreu um erro ao processar sua mensagem.';
      
      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Tempo esgotado ao aguardar resposta do servidor. Verifique sua conexão.';
      } else if (error.response) {
        errorMessage = `Erro do servidor: ${error.response.status} - ${error.response.data.detail || 'Erro desconhecido'}`;
      } else if (error.request) {
        errorMessage = 'O servidor não está respondendo. Verifique se a API está em execução.';
        setApiStatus('Erro - API não disponível');
        setTimeout(checkApiStatus, 5000);
      }
      
      const errorResponseMessage = {
        id: Date.now() + 1,
        content: errorMessage,
        role: 'assistant',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorResponseMessage]);
    } finally {
      setIsLoading(false);
      if (loadingTimerRef.current) {
        clearTimeout(loadingTimerRef.current);
      }
    }
  };

  const clearHistory = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/chat/history`, {
        headers: {
          'X-Session-ID': sessionId
        }
      });
      setMessages([]);
    } catch (error) {
      console.error('Erro ao limpar histórico:', error);
    }
  };

  useEffect(() => {
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
    
    checkApiStatus();
    initializeAudio();
    loadChatHistory(newSessionId);
    
    const apiCheckInterval = setInterval(checkApiStatus, 30000);
    
    return () => {
      clearInterval(apiCheckInterval);
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white flex flex-col items-center justify-center p-4">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full mix-blend-normal filter blur-[128px] animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full mix-blend-normal filter blur-[128px] animate-pulse" style={{animationDelay: '1s'}} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-emerald-500/5 rounded-full mix-blend-normal filter blur-[96px] animate-pulse" style={{animationDelay: '2s'}} />
      </div>
      
      <div className="w-full max-w-4xl mx-auto rounded-2xl overflow-hidden bg-white/[0.02] backdrop-blur-xl border border-white/[0.05] shadow-2xl shadow-black/20">
        <div className="px-6 py-4 flex items-center justify-between border-b border-white/[0.08] bg-gradient-to-r from-violet-500/10 to-purple-500/10">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="w-12 h-12 rounded-full bg-gradient-to-r from-violet-500 to-purple-500 flex items-center justify-center shadow-lg shadow-violet-500/25">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                </svg>
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-slate-900"></div>
            </div>
            
            <div>
              <h1 className="text-xl font-bold text-white">Terra Plana Chat</h1>
              <p className="text-sm text-white/60">Eduardo Mayer • Especialista Terra Plana</p>
            </div>
          </div>
          
          <div className="text-xs text-white/40">
            Sessão: {sessionId.substring(0, 12)}...
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 space-y-6 h-[500px] scrollbar-thin scrollbar-thumb-white/20 scrollbar-track-transparent">
          {messages.length === 0 && <WelcomeMessage />}
          
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              isUser={message.role === 'user'}
            />
          ))}
          
          {isLoading && <LoadingMessage />}
          
          <div ref={messagesEndRef} />
        </div>
        
        {isAudioSupported && (
          <AudioControls
            isRecording={isRecording}
            isAudioSupported={isAudioSupported}
            recordingTime={recordingTime}
            onStartRecording={startRecording}
            onStopRecording={stopRecording}
          />
        )}
        
        <ChatInput
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onSend={sendMessage}
          onClear={clearHistory}
          disabled={isLoading}
        />
        
        <StatusBar apiStatus={apiStatus} isAudioSupported={isAudioSupported} />
      </div>
    </div>
  );
}

export default App; 