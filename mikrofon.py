import numpy as np
import sounddevice as sd

def izracunaj_rms(audio_chunk):

    # sqrt(mean(x^2))
    return np.sqrt(np.mean(audio_chunk**2)) 

def kalibrisi_tisinu(sample_rate):


    print(" Molim tišinu 1 sekundu za kalibraciju mikrofona...")
    try:
        # Snimamo 1 sekundu (blocking=True znači da program stane dok ne snimi)
        recording = sd.rec(int(sample_rate * 1), samplerate=sample_rate, channels=1, blocking=True)
        recording = recording.flatten()
        
        noise_rms = izracunaj_rms(recording) 
        
        # Prag je 5 puta jači od buke, ali ne manji od 0.005
        novi_prag = max(noise_rms * 5, 0.005) 
        
        print(f"Kalibrisano! Nivo buke: {noise_rms:.5f} -> Postavljen prag: {novi_prag:.5f}")
        print("-" * 50)
        return novi_prag
    except Exception as e:
        print(f" Greška pri kalibraciji: {e}. Koristim podrazumevani prag.")
        return 0.02