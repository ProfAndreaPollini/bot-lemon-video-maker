import re
import wikipedia
import qrcode
from gtts import gTTS
from PIL import Image

import random

import text_to_image
from moviepy.editor import *

from mutagen import mp3

from tempfile import NamedTemporaryFile


def speak(txt, lang='it'):
    tts = gTTS(text=txt, lang=lang)
    tts.save("tmp.mp3")
    # tts.write_to_fp(voice := NamedTemporaryFile("test.txt"))
    encoded_image_path = text_to_image.encode(txt, "output_image.png")

    # .write_to_fp(voice := NamedTemporaryFile())
    # playsound(voice.name)
    # voice.close()

def draw_image(txt,page):
  info = mp3.MP3("tmp.mp3").info

  title_clip = ImageClip("qr.png",transparent=False).set_start(0).set_duration(4).set_position(('center','center')).crossfadeout(0.5)
  
  offset = title_clip.duration + title_clip.start

  txt_clip =  TextClip(txt,fontsize=50,color='white').set_position('center').set_duration(info.length-2).set_start(offset+1).set_position(("center","center")).crossfadein(0.5)

  print(txt_clip.duration)
  print(txt_clip.start)

  offset = txt_clip.duration + txt_clip.start
  scrivi_risposta_clip  = TextClip("Ferma il video\n e indovina il film.\n\nScrivi nei commenti\nla risposta",fontsize=70,color='red').set_duration(3).set_start(1+offset).set_position(('center','center')).crossfadein(0.5)

  print(scrivi_risposta_clip.duration)
  print(scrivi_risposta_clip.start)

  offset = scrivi_risposta_clip.duration + scrivi_risposta_clip.start

  countdown_clips =   CompositeVideoClip([TextClip(str(x),fontsize=200,color='red').set_duration(0.75).set_start((3-x)).set_position(('center','center')).crossfadein(0.25) for x in range(3,0,-1)]).set_audio(AudioFileClip("countdown.wav")).set_start(offset).set_position(('center','center')).crossfadein(0.25)


  response_qr = qrcode.make(page.url)
  response_qr = response_qr.resize((800,800))
# qrcode.image.pil.PilImage

  formatter = {"PNG": "RGBA", "JPEG": "RGB"}
  
  rgbimg = Image.new(formatter.get(response_qr.format, 'RGB'), response_qr.size)
  rgbimg.paste(response_qr)
  rgbimg.save("qr.png", format=response_qr.format)
  # response_qr.save("qr.png")

  offset = countdown_clips.duration + countdown_clips.start

  qrcode_clip = ImageClip("qr.png",transparent=False).set_start(offset).set_duration(5).set_position(('center','center')).crossfadein(0.5)

  

  print(qrcode_clip.duration)
  print(qrcode_clip.start)

  offset = qrcode_clip.duration + qrcode_clip.start

  risposta_clip  = TextClip(page.title,fontsize=90,color='white',size=(1080,1920),method="label").set_duration(5).set_start(offset).set_position(('center','center')).crossfadein(0.5)

  offset  = risposta_clip.duration + risposta_clip.start

  bgclip = ColorClip(size=(1080,1920), color=[30,50,50]).set_duration(offset+1).set_audio(AudioFileClip("tmp.mp3")).crossfadein(0.5).crossfadeout(1)


  output = CompositeVideoClip([bgclip,title_clip, txt_clip,scrivi_risposta_clip,countdown_clips,qrcode_clip,risposta_clip])

  output.write_videofile("output.mp4", fps=30)

wikipedia.set_lang("it")
# print(wikipedia.summary("100_più_grandi_film_secondo_il_Time"))
films_page = wikipedia.page("100 più grandi film secondo il Time")

content = films_page.content
print("-"*80)

films = content.split("== Lista in ordine alfabetico ==")[1].strip().split("== Note ==")[0].strip().split("\n")

films = [x.split(",")[0].split("-")[0] for x in films]

print(f"Porcessing {len(films)} films")

film = random.choice(films).split("(")[0].strip()


def parse_film_page(page,film):
  page_content = page.content.split("== Trama ==")[1].strip().split("== Produzione ==")[0].strip()

  page_content = re.sub(r'===(.+)===', '', page_content)
  page_content = re.sub(film, '***', page_content)
  page_content = re.sub(r'\s+', ' ', page_content, flags=re.I)

  
  return page_content.split(".")

print(f"> {film}...")
film_page = wikipedia.page(film)
trama = parse_film_page(film_page,film)
print(f"{len(trama)} paragraphs")
for line in trama:
  print(line)

idx = random.randint(0,len(trama)-2)

selected_trama = " ".join([trama[idx]+".",trama[idx+1]+"."])

print(selected_trama)
speak(selected_trama)

descrizione = selected_trama.split(" ")

descrizione_list = [" ".join(descrizione[x:x+4]) for x in range(0,len(descrizione),4)]

print(descrizione_list)

draw_image("\n".join(descrizione_list),film_page)
print(film_page.__dict__)

# for n,line in enumerate(content):
#   print(n,line)