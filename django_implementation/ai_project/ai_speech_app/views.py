from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import speech_recognition as sr
import uuid
import random

# Create your views here.
def index_michael(request):
    return render(request, 'index.html')

def index(request):
     # Preset topics
    topics = ["Farming", "Computer Technology", "Psychology"]
    random_topic = random.choice(topics)
    
    if request.method == "POST":
        uploaded_file = request.FILES.get('audio_file')
        if not uploaded_file:
            return render(request, "index.html", {"error": "No audio file uploaded!"})

        # Save the uploaded file
        file_name = f"audio_{uuid.uuid4().hex}.wav"
        file_path = os.path.join(settings.MEDIA_ROOT, "uploaded_audio", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Process the audio file
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)  # Read the audio file
                transcription = recognizer.recognize_google(audio)
                return render(request, "index.html", {"transcription": transcription})
        except sr.UnknownValueError:
            os.remove(file_path)
            return JsonResponse({"error": "Speech not recognized"}, status=400)
        except Exception as e:
            os.remove(file_path)
            return JsonResponse({"error": str(e)}, status=500)
            # return render(request, "index.html", {"error": str(e)})

    return render(request, "index.html",  {"random_topic": random_topic})