import sounddevice as sd
import requests
import numpy as np
import queue
import threading
import sys
import time
import ucitavanje
import mikrofon

SAMPLE_RATE = 16000
BLOCK_SIZE = 4096
SILENCE_LIMIT_SEC = 1.5
SERVICE_URL = "https://httpbin.org/post"

q = queue.Queue()

def audio_callback(indata, frames, time, status): 
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

#TO DO 
def slanje_u_pozadini(tekst):  
    """ Funkcija za thread """
    try:
        requests.post(SERVICE_URL, json={"transkripcija": tekst}, timeout=3)
    except Exception:
        pass
#TO DO 
def posalji_na_servis(tekst):
    t = threading.Thread(target=slanje_u_pozadini, args=(tekst,))
    t.daemon = True
    t.start()

def main():
    processor, model = ucitavanje.ucitaj_model()
    threshold = mikrofon.kalibrisi_tisinu(SAMPLE_RATE)
    
    audio_buffer = []
    blocks_of_silence = 0
    block_duration = BLOCK_SIZE / SAMPLE_RATE
    silence_limit_blocks = int(SILENCE_LIMIT_SEC / block_duration)
    is_speaking = False
     
    
    print(f"Slušam... (Govori u mikrofon)")
    print("Pritisni Ctrl+C za prekid.")

    frames_since_last_print = 0
    PRINT_INTERVAL_BLOCKS = int(1.0 / block_duration)

    with sd.InputStream(callback=audio_callback, channels=1, 
                        samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE): 
        while True:
            indata = q.get()
            audio_chunk = indata.flatten()
            
            rms = mikrofon.izracunaj_rms(audio_chunk)
            
            if rms > threshold:
                is_speaking = True
                blocks_of_silence = 0
                audio_buffer.append(audio_chunk)
                frames_since_last_print += 1
                
                if frames_since_last_print >= PRINT_INTERVAL_BLOCKS:
                    temp_audio = np.concatenate(audio_buffer)
                    
                    tekst = ucitavanje.transkribuj_segment(temp_audio, processor, model, SAMPLE_RATE)
                    
                    sys.stdout.write(f"\rTrenutno: {tekst}")
                    sys.stdout.flush()
                    
                    frames_since_last_print = 0
            else: 
                
                if is_speaking:
                    blocks_of_silence += 1
                    audio_buffer.append(audio_chunk)
                    
                    if blocks_of_silence > silence_limit_blocks:
                        # Spajamo chunkove i šaljemo u modul ucitavanje
                        full_audio = np.concatenate(audio_buffer)

                        tekst = ucitavanje.transkribuj_segment(full_audio, processor, model, SAMPLE_RATE)
                        
                        if tekst and len(tekst.strip()) > 1:
                            print(f"\rPrepoznato: {tekst}")
                            print("Slušam...")
                            posalji_na_servis(tekst)
                            
                        

                        audio_buffer = []
                        is_speaking = False
                        blocks_of_silence = 0
                        frames_since_last_print = 0
                        
            # Sigurnosni limit (RAM zaštita)
            if len(audio_buffer) > (30 / block_duration):
                 audio_buffer = []
                 is_speaking = False
           


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Program zaustavljen.")