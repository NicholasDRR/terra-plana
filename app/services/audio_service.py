"""
Serviço para processamento de áudio
Transcrição com OpenAI Whisper e síntese de voz com ElevenLabs
"""

import io
import os
import tempfile
from typing import BinaryIO, Optional
import openai
from elevenlabs import voices, generate, set_api_key
from ..config import settings


class AudioService:
    """Serviço para transcrição e síntese de voz"""
    
    def __init__(self):
        """Inicializar serviços de áudio"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        if not settings.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY não configurada")
            
        # Configurar clientes
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        set_api_key(settings.ELEVENLABS_API_KEY)
        
        self.voice_id = settings.ELEVENLABS_VOICE_ID
    
    async def transcribe_audio(self, audio_file: BinaryIO, filename: str) -> str:
        """
        Transcreve áudio para texto usando OpenAI Whisper
        
        Args:
            audio_file: Arquivo de áudio em bytes
            filename: Nome do arquivo para identificar formato
            
        Returns:
            Texto transcrito
        """
        temp_file_path = None
        try:
            # Cria arquivo temporário para o Whisper
            file_extension = filename.split('.')[-1] if '.' in filename else 'webm'
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}")
            temp_file_path = temp_file.name
            
            # Escreve o conteúdo do áudio no arquivo temporário
            audio_file.seek(0)
            temp_file.write(audio_file.read())
            temp_file.close()  # Fecha o arquivo antes de usar com Whisper
            
            # Transcrição com Whisper
            with open(temp_file_path, "rb") as f:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language="pt"  # Português
                )
            
            return transcript.text.strip()
                
        except Exception as e:
            print(f"Erro na transcrição: {str(e)}")
            raise Exception(f"Erro ao transcrever áudio: {str(e)}")
        finally:
            # Remove arquivo temporário de forma segura
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except PermissionError:
                    # Se não conseguir deletar agora, agenda para mais tarde
                    print(f"Arquivo temporário será removido pelo sistema: {temp_file_path}")
                except Exception as cleanup_error:
                    print(f"Erro ao remover arquivo temporário: {cleanup_error}")
    
    def text_to_speech(self, text: str) -> bytes:
        """
        Converte texto em áudio usando ElevenLabs
        
        Args:
            text: Texto para converter em voz
            
        Returns:
            Áudio em bytes (formato MP3)
        """
        try:
            # Gera áudio com ElevenLabs
            audio = generate(
                text=text,
                voice=self.voice_id,
                model="eleven_multilingual_v2"  # Modelo multilíngue para português
            )
            
            return audio
            
        except Exception as e:
            print(f"Erro na síntese de voz: {str(e)}")
            raise Exception(f"Erro ao gerar áudio: {str(e)}")
    
    def get_available_voices(self) -> list:
        """
        Retorna lista de vozes disponíveis no ElevenLabs
        
        Returns:
            Lista de vozes com ID, nome e descrição
        """
        try:
            voice_list = voices()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category if hasattr(voice, 'category') else 'unknown'
                }
                for voice in voice_list
            ]
        except Exception as e:
            print(f"Erro ao obter vozes: {str(e)}")
            return []
    
    def validate_audio_file(self, filename: str, file_size: int) -> None:
        """
        Valida arquivo de áudio
        
        Args:
            filename: Nome do arquivo
            file_size: Tamanho do arquivo em bytes
            
        Raises:
            ValueError: Se arquivo inválido
        """
        # Verifica tamanho
        if file_size > settings.MAX_AUDIO_SIZE:
            raise ValueError(f"Arquivo muito grande. Máximo: {settings.MAX_AUDIO_SIZE / (1024*1024):.1f}MB")
        
        # Verifica formato
        file_extension = filename.lower().split('.')[-1]
        if file_extension not in settings.SUPPORTED_AUDIO_FORMATS:
            raise ValueError(f"Formato não suportado. Use: {', '.join(settings.SUPPORTED_AUDIO_FORMATS)}")
    
    def save_audio_file(self, audio_data: bytes, filename: str) -> str:
        """
        Salva áudio em arquivo temporário e retorna o caminho
        
        Args:
            audio_data: Dados do áudio em bytes
            filename: Nome base para o arquivo
            
        Returns:
            Caminho do arquivo salvo
        """
        try:
            # Cria arquivo temporário
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=f"_{filename}.mp3",
                prefix="audio_response_"
            )
            
            temp_file.write(audio_data)
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"Erro ao salvar áudio: {str(e)}")
            raise Exception(f"Erro ao salvar arquivo de áudio: {str(e)}") 