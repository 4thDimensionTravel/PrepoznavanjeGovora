# PrepoznavanjeGovora

Prepoznavanje Govora u Realnom Vremenu (Wav2Vec2 SR)
Ovaj projekat omogućava transkripciju govora u realnom vremenu koristeći napredni duboki model Wav2Vec2 specifično treniran za srpski jezik. Sistem automatski detektuje govor, vrši konverziju zvuka u tekst i šalje rezultate na eksterni servis.

Pregled Projekta
Sistem funkcioniše kao "uvek slušajući" (always-listening) asistent koji koristi procesiranje audio signala za detekciju aktivnosti glasa. Ključne faze rada su:

Kalibracija: Prilagođavanje ambijentalnoj buci prostorije.

VAD (Voice Activity Detection): Praćenje RMS nivoa zvuka kako bi se razdvojio govor od tišine.

Inference: Slanje audio segmenta u Wav2Vec2 model.

Backend Integration: Slanje gotove transkripcije na web servis putem HTTP POST zahteva.

Struktura Fajlova
main.py: Centralna logika aplikacije. Upravlja audio strimom (input stream), redovima čekanja (queues) i nitima (threads) za slanje podataka.

ucitavanje.py: Zadužen za rad sa HuggingFace Transformers bibliotekom. Učitava model i vrši samu transkripciju audio vrednosti u tekst.

mikrofon.py: Sadrži pomoćne funkcije za audio inženjering, uključujući izračunavanje RMS vrednosti i inicijalnu kalibraciju praga osetljivosti mikrofona.

🛠️ Tehnologije i Model
Jezik: Python

Model: classla/wav2vec2-xls-r-juznevesti-sr (Wav2Vec2 model optimizovan za srpski jezik)

Audio biblioteke: sounddevice, numpy

Deep Learning: torch (PyTorch), transformers

Networking: requests

🧠 Ključne Karakteristike
⚡ Inteligentna Kalibracija
Program na samom početku snima jednu sekundu tišine kako bi izmerio nivo pozadinske buke. Prag detekcije glasa se postavlja na 5 puta jači nivo od izmerene buke, čime se sprečava aktivacija modela na šumove.

🕒 Procesiranje u Realnom Vremenu
Dok govorite, sistem u intervalima ispisuje trenutnu transkripciju u konzolu. Kada detektuje tišinu dužu od 1.5 sekundi, sistem zaključuje da je rečenica gotova i šalje finalni tekst na servis.
