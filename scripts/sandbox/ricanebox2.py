from pathlib import Path
import audio_metadata

ROOT_DIR = Path("E://sound bank (ricane)//#DUB")


meta = []

for track in list(ROOT_DIR.glob('**/*.mp3')):
    meta = audio_metadata.load(track)
    print(f"-------- {meta['tags']['TIT2']} --------")
    print(meta["streaminfo"])
    print(f"BPM: {meta['tags']['TBPM']}")
    try:    
        print(f"GENRE: {meta['tags']['TCON']}")
    except:
        print("no genre")
    print("\n\n")



print("Job done ... Quitting !")
