from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
import os
from gtts import gTTS
import random
import time
import tempfile

# Lista expandida de palavras para praticar (sem repetição)
PALAVRAS_PRATICA = [
    # Palavras básicas
    'casa', 'bola', 'gato', 'cachorro', 'livro', 'mesa', 'cadeira', 'porta', 'janela', 'carro',
    'sol', 'lua', 'estrela', 'céu', 'nuvem', 'chuva', 'vento', 'mar', 'rio', 'lago',
    'água', 'fogo', 'terra', 'ar', 'pedra', 'areia', 'montanha', 'floresta', 'árvore', 'flor',
    
    # Emoções e sentimentos
    'amor', 'paz', 'feliz', 'alegria', 'triste', 'raiva', 'medo', 'calma', 'sonho', 'esperança',
    
    # Família
    'mãe', 'pai', 'filho', 'filha', 'bebê', 'avó', 'avô', 'irmão', 'irmã', 'família',
    
    # Cores
    'azul', 'verde', 'vermelho', 'amarelo', 'rosa', 'roxo', 'preto', 'branco', 'cinza', 'laranja',
    
    # Animais
    'pássaro', 'peixe', 'leão', 'tigre', 'elefante', 'macaco', 'cavalo', 'vaca', 'porco', 'galinha',
    'rato', 'coelho', 'urso', 'lobo', 'raposa', 'cobra', 'sapo', 'borboleta', 'abelha', 'formiga',
    
    # Comidas
    'pão', 'leite', 'arroz', 'feijão', 'carne', 'frango', 'peixe', 'ovo', 'queijo', 'manteiga',
    'maçã', 'banana', 'laranja', 'uva', 'melancia', 'morango', 'tomate', 'batata', 'cenoura', 'alface',
    
    # Objetos do dia a dia
    'telefone', 'relógio', 'sapato', 'roupa', 'camisa', 'calça', 'vestido', 'chapéu', 'bolsa', 'chave',
    'prato', 'copo', 'garfo', 'faca', 'colher', 'panela', 'fogão', 'geladeira', 'cama', 'sofá',
    
    # Ações
    'andar', 'correr', 'pular', 'dormir', 'comer', 'beber', 'falar', 'ouvir', 'ver', 'tocar',
    'ler', 'escrever', 'desenhar', 'pintar', 'cantar', 'dançar', 'jogar', 'estudar', 'trabalhar', 'brincar'
]

# Variável global para controlar palavras já usadas
palavras_usadas = []


def home(request):
    """Página inicial do projeto"""
    return render(request, 'core/home.html')


@api_view(['POST'])
def stt_view(request):
    """Speech-to-Text usando Google Speech Recognition (GRATUITO - SEM API KEY)"""
    print("=" * 50)
    print("=== INÍCIO STT (Speech-to-Text) ===")
    
    audio_file = request.FILES.get('audio')
    palavra_esperada = request.data.get('palavra_esperada', '').lower().strip()
    
    print(f"Arquivo recebido: {audio_file}")
    print(f"Palavra esperada: '{palavra_esperada}'")
    
    if not audio_file:
        print("ERRO: Nenhum arquivo de áudio enviado")
        return Response({'error': 'Nenhum arquivo de áudio enviado'}, status=400)
    
    # Usar tempfile para evitar conflitos
    temp_original = None
    temp_converted = None
    
    try:
        # Criar arquivos temporários
        temp_original = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_converted = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        
        temp_original_path = temp_original.name
        temp_converted_path = temp_converted.name
        
        # Fechar os arquivos para poder escrever neles
        temp_original.close()
        temp_converted.close()
        
        print("1. Salvando arquivo...")
        with open(temp_original_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        print(f"   Arquivo salvo: {os.path.getsize(temp_original_path)} bytes")
        
        print("2. Convertendo áudio para formato otimizado...")
        from pydub import AudioSegment
        audio = AudioSegment.from_file(temp_original_path)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        audio.export(temp_converted_path, format='wav')
        print(f"   Áudio convertido: {os.path.getsize(temp_converted_path)} bytes")
        
        print("3. Iniciando reconhecimento de voz...")
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        # Configurar reconhecedor para melhor precisão
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        
        with sr.AudioFile(temp_converted_path) as source:
            print("   Ajustando para ruído ambiente...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("   Gravando áudio...")
            audio_data = recognizer.record(source)
        
        # Aguardar para garantir que arquivo foi fechado
        time.sleep(0.2)
        
        print("   Enviando para Google Speech Recognition (gratuito)...")
        try:
            texto_completo = recognizer.recognize_google(
                audio_data, 
                language='pt-BR',
                show_all=False
            ).lower().strip()
            print(f"   ✅ Reconhecido: '{texto_completo}'")
            
        except sr.UnknownValueError:
            print("   ⚠️ Google não conseguiu entender o áudio")
            return Response({
                'transcricao': '',
                'acertou': False,
                'mensagem': '🎤 Não consegui ouvir. Fale mais alto e claramente!'
            })
            
        except sr.RequestError as e:
            print(f"   ❌ Erro de conexão: {e}")
            return Response({
                'error': 'Erro ao conectar com serviço de reconhecimento. Verifique sua internet.',
                'transcricao': '',
                'acertou': False,
                'mensagem': '📡 Sem conexão. Verifique sua internet!'
            }, status=500)
        
        print("4. Verificando resposta...")
        
        # Normalizar texto (remover acentos para comparação)
        import unicodedata
        def remover_acentos(texto):
            return ''.join(
                c for c in unicodedata.normalize('NFD', texto)
                if unicodedata.category(c) != 'Mn'
            )
        
        texto_normalizado = remover_acentos(texto_completo)
        palavra_normalizada = remover_acentos(palavra_esperada)
        
        # Verificar se acertou (com e sem acentos)
        palavras_detectadas = texto_normalizado.split()
        acertou = (
            palavra_normalizada == texto_normalizado or
            palavra_normalizada in palavras_detectadas or
            palavra_esperada == texto_completo or
            palavra_esperada in texto_completo.split()
        )
        
        print(f"   Palavra esperada: '{palavra_esperada}'")
        print(f"   Texto reconhecido: '{texto_completo}'")
        print(f"   Acertou: {acertou}")
        print("=" * 50)
        
        mensagem = '🎉 Parabéns! Você acertou!' if acertou else f'❌ Você disse "{texto_completo}". A palavra era "{palavra_esperada}". Tente novamente!'
        
        return Response({
            'transcricao': texto_completo,
            'palavra_esperada': palavra_esperada,
            'acertou': acertou,
            'mensagem': mensagem
        })
        
    except Exception as e:
        print(f"❌ ERRO FATAL: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': f'Erro ao processar áudio: {str(e)}',
            'transcricao': '',
            'acertou': False,
            'mensagem': '❌ Erro ao processar. Tente novamente!'
        }, status=500)
        
    finally:
        # Sempre limpar arquivos temporários
        print("5. Limpando arquivos temporários...")
        time.sleep(0.3)
        try:
            if temp_original_path and os.path.exists(temp_original_path):
                os.unlink(temp_original_path)
            if temp_converted_path and os.path.exists(temp_converted_path):
                os.unlink(temp_converted_path)
            print("   ✅ Arquivos temporários deletados")
        except Exception as e:
            print(f"   ⚠️ Aviso: {e}")


@api_view(['POST'])
def tts_view(request):
    """Text-to-Speech usando gTTS (GRATUITO - SEM API KEY)"""
    print("=" * 50)
    print("=== INÍCIO TTS (Text-to-Speech) ===")
    
    texto = request.data.get('texto')
    
    if not texto:
        print("ERRO: Texto não enviado")
        return Response({'error': 'Texto não enviado'}, status=400)
    
    print(f"Texto para sintetizar: '{texto}'")
    
    try:
        # Criar TTS com voz brasileira
        tts = gTTS(
            text=texto,
            lang='pt',  # Português
            slow=False,  # Velocidade normal
            tld='com.br'  # Sotaque brasileiro
        )
        
        # Usar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            audio_path = temp_audio.name
        
        print("1. Gerando áudio...")
        tts.save(audio_path)
        print(f"   Áudio gerado: {os.path.getsize(audio_path)} bytes")
        
        print("2. Lendo arquivo de áudio...")
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        print("3. Deletando arquivo temporário...")
        os.remove(audio_path)
        
        print("✅ TTS concluído com sucesso")
        print("=" * 50)
        
        return HttpResponse(audio_data, content_type='audio/mpeg')
        
    except Exception as e:
        print(f"❌ ERRO: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        return Response({'error': f'Erro ao gerar áudio: {str(e)}'}, status=500)


@api_view(['GET'])
def nova_palavra(request):
    """Retorna uma palavra aleatória SEM REPETIÇÃO"""
    global palavras_usadas
    
    # Se todas as palavras foram usadas, reinicia
    if len(palavras_usadas) >= len(PALAVRAS_PRATICA):
        print("📚 Todas as palavras foram praticadas! Reiniciando...")
        palavras_usadas = []
    
    # Seleciona apenas palavras não usadas
    palavras_disponiveis = [p for p in PALAVRAS_PRATICA if p not in palavras_usadas]
    palavra = random.choice(palavras_disponiveis)
    palavras_usadas.append(palavra)
    
    print(f"🎯 Nova palavra: '{palavra}' (Progresso: {len(palavras_usadas)}/{len(PALAVRAS_PRATICA)})")
    
    return Response({
        'palavra': palavra.upper(),  # Retorna em maiúsculo para o frontend
        'progresso': f'Palavra {len(palavras_usadas)} de {len(PALAVRAS_PRATICA)}'
    })


@api_view(['POST'])
def resetar_palavras(request):
    """Reseta o progresso de palavras"""
    global palavras_usadas
    palavras_usadas = []
    print("🔄 Progresso de palavras resetado!")
    return Response({'mensagem': 'Progresso resetado com sucesso!'})
