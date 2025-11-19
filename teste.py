import speech_recognition as sr

# Testa se está instalado
print("SpeechRecognition instalado:", sr.__version__)

# Testa reconhecimento básico
recognizer = sr.Recognizer()
print("Recognizer criado com sucesso!")
