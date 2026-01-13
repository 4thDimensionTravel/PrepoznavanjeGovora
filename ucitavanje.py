import sys
import torch
from transformers import AutoProcessor, AutoModelForCTC

MODEL_ID = "classla/wav2vec2-xls-r-juznevesti-sr"

def ucitaj_model():

    print(f"\n Učitavam Wav2Vec2 model ({MODEL_ID})...")
    try:
        processor = AutoProcessor.from_pretrained(MODEL_ID)
        model = AutoModelForCTC.from_pretrained(MODEL_ID)
        print(" Model uspešno učitan!\n")
        return processor, model
    except Exception as e:
        print(f" Greška pri učitavanju modela: {e}")
        sys.exit(1)

def transkribuj_segment(audio_values, processor, model, sample_rate=16000):

    if len(audio_values) == 0:
        return "" 
    inputs = processor(audio_values, sampling_rate=sample_rate, return_tensors="pt", padding=True)
    

    with torch.no_grad():
        
        
        logits = model(inputs.input_values).logits 


    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    
    return transcription