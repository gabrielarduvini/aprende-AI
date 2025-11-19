# 🤖 Aprende AI - Alfabetização com Inteligência Artificial

Sistema de alfabetização que utiliza reconhecimento de voz (Speech-to-Text) e síntese de voz (Text-to-Speech) para auxiliar no aprendizado de palavras através de inteligência artificial.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2.8-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Funcionalidades

- 🔊 **Text-to-Speech (TTS)**: Ouça a pronúncia correta das palavras
- 🎤 **Speech-to-Text (STT)**: Grave sua pronúncia e receba validação automática
- ✅ **Validação em tempo real**: Feedback imediato se você acertou
- 📊 **Sistema de progresso**: Mais de 100 palavras sem repetição
- 🎯 **Interface intuitiva**: Fácil de usar para todas as idades

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.8** - Framework web Python
- **Django REST Framework** - API REST
- **SpeechRecognition** - Reconhecimento de voz via Google
- **gTTS** - Síntese de voz
- **pydub** - Processamento de áudio

### Frontend
- **HTML5 + CSS3**
- **JavaScript (Vanilla)**
- **RecordRTC** - Gravação de áudio no navegador

### Infraestrutura
- **FFmpeg** - Conversão e processamento de áudio

## 📦 Pré-requisitos

- Python 3.11 ou 3.12 (recomendado)
- FFmpeg instalado no sistema
- Conexão com internet (para reconhecimento de voz)

## 🚀 Instalação

### 1. Clone o repositório

git clone https://github.com/Andreretsu/aprende-AI.git
cd aprende-AI
git checkout feature/tts-stt



### 2. Crie e ative o ambiente virtual

**Windows:**
python -m venv venv
.\venv\Scripts\activate

**Linux/macOS:**
python3 -m venv venv
source venv/bin/activate


### 3. Instale as dependências

pip install --upgrade pip
pip install -r requirements.txt
pip install SpeechRecognition pydub


### 4. Instale o FFmpeg

**Windows:**
1. Baixe: [FFmpeg Essentials](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
2. Extraia para `C:\ffmpeg`
3. Adicione `C:\ffmpeg\bin` ao PATH do sistema
4. Reinicie o terminal


**Ubuntu/Debian:**
sudo apt-get update
sudo apt-get install ffmpeg

**macOS:**
brew install ffmpeg

### 5. Configure o banco de dados

python manage.py migrate

## ▶️ Executando o Projeto

### Inicie o servidor de desenvolvimento

python manage.py runserver


### Acesse a aplicação

Abra seu navegador em:

http://127.0.0.1:8000/


## 📖 Como Usar

1. **Ouça a palavra**: Clique em "🔊 Ouvir Palavra" para escutar a pronúncia
2. **Grave sua voz**: Clique em "🎤 Começar a Gravar"
3. **Fale a palavra**: Pronuncie claramente a palavra mostrada
4. **Receba feedback**: O sistema valida automaticamente se você acertou
5. **Próxima palavra**: Avance para uma nova palavra automaticamente

## 🌐 API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Página inicial da aplicação |
| `/api/nova-palavra/` | GET | Retorna uma palavra aleatória |
| `/api/tts/` | POST | Converte texto em áudio |
| `/api/stt/` | POST | Reconhece áudio e valida palavra |
| `/api/resetar-palavras/` | POST | Reseta o progresso de palavras |

### Exemplo de uso da API

**Nova Palavra:**

curl http://localhost:8000/api/nova-palavra/

**Text-to-Speech:**


curl -X POST http://localhost:8000/api/tts/
-H "Content-Type: application/json"
-d '{"texto": "casa"}'


## 📁 Estrutura do Projeto

aprende-AI/
├── config/ # Configurações do Django
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── core/ # App principal
│ ├── templates/
│ │ └── core/
│ │ └── home.html # Interface principal
│ ├── views.py # Lógica de IA (STT/TTS)
│ ├── urls.py # Rotas da API
│ └── models.py
├── venv/ # Ambiente virtual
├── manage.py
├── requirements.txt
└── README.md


## 🔧 Solução de Problemas

### "Couldn't find ffmpeg"
- **Causa**: FFmpeg não está instalado ou não está no PATH
- **Solução**: Instale o FFmpeg e adicione ao PATH do sistema. Reinicie o terminal.

### "Google não entendeu o áudio"
- **Causa**: Áudio muito baixo, ruído ou sem conexão
- **Solução**: 
  - Fale mais alto e claramente
  - Verifique sua conexão com internet
  - Use fone de ouvido com microfone

### "ModuleNotFoundError"
- **Causa**: Dependências não instaladas
- **Solução**: 

pip install -r requirements.txt
pip install SpeechRecognition pydub


### Python 3.13 com problemas
- **Causa**: Algumas bibliotecas ainda não têm suporte completo
- **Solução**: Use Python 3.11 ou 3.12

## 🔄 Migração para Outro Frontend

O backend está preparado para ser consumido por qualquer framework frontend moderno.

**Exemplo com React:**

const response = await fetch('http://localhost:8000/api/stt/', {
method: 'POST',
body: formData
});
const data = await response.json();

**Configuração CORS necessária:**

config/settings.py
CORS_ALLOWED_ORIGINS = [
"http://localhost:3000",
]


## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Gabriel** - [@Andreretsu](https://github.com/Andreretsu)

## 🙏 Agradecimentos

- Google Speech Recognition API
- Comunidade Django
- Biblioteca RecordRTC
- Vosk Speech Recognition

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
