import cv2
import time
import numpy as np
import tkinter
import fpstimer
import pygame.mixer
from screeninfo import get_monitors

window_text = {
  "width": 0,
  "height": 0
}

window_size = {
  "width": 1920,
  "height": 1080
}

for m in get_monitors():
  window_size["width"] = m.width
  window_size["height"] = m.height

root = None
text_c = None

result_array = []

cap_file = cv2.VideoCapture('badapple.mp4') #CUSTOM:動画ファイル

def tkinter_setting (width, height):

  global root

  root = tkinter.Tk()
  root.title("bad apple!")
  root.geometry("{}x{}".format(window_size["width"], window_size["height"])) # ウインドウサイズ
  root.bind('<Configure>', change_size) # 関数のバインド(連携)

def textc_setting (width, height):

  global text_c

  text_c = tkinter.Canvas( # テキストを描くキャンバスを生成
    root,
    width = window_size["width"] / 2,
    height = window_size["height"] / 2,
    background = '#ffffff'
  )
  text_c.pack(fill = tkinter.BOTH, expand=True) # ウインドウサイズをリサイズ
  window_text["width"] = width
  window_text["height"] = height

id_window_text = None

# サイズを変更した時の処理(生成時も)
def change_size(event):

  global text_c
  global window_text
  global id_window_text

  w = text_c.winfo_width() # ウインドウの幅
  h = text_c.winfo_height() # ウインドウの高さ
  window_size["width"] = w
  window_size["height"] = h
  window_text["width"] = window_size["width"] / 2
  window_text["height"] = window_size["height"] / 2
  text_c.coords(id_window_text, window_text["width"], window_text["height"]) # テキストの変更


def show_window(text):

  global text_c
  global id_window_text
  global window_text

  id_window_text = text_c.create_text(
    window_text["width"],
    window_text["height"],
    text = text,
    font = ('', 10), # CUSTOM:1文字あたりの大きさ
    fill = "#000000",
    tag="window_text"
  )
  text_c.update()

def next_message():
  pygame.mixer.init() #初期化
  print("-----------------")
  print("生成が完了しました。")
  print("残念ながら私の技量では自動でウインドウを閉じることができません。")
  print("申し訳ありませんが、再生が終わりましたら手動でウインドウを閉じてください。")
  print("また、スペックの低いパソコンだと、処理の関係上フレームがズレることがあります。")
  print("その場合は、プログラムファイル中の「CUSTOM」の部分を調整してください。")
  print("-----------------")
  input("エンターキーを押すと再生が始まります。：")
  play_movie()


def make_frame():

  global cap_file
  global result_array

  width = int(cap_file.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT))

  count = 0

  message_count = 0

  while True:

    ret, frame = cap_file.read()

    if ret == False:
      break

    frame = cv2.resize(frame , (int(width*0.38), int(height*0.38))) # CUSTOM:動画の画質×0.38(初期値)。解像度を落とす場合は値を小さくしてください
    im_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    thresh = 128
    im_bool = im_gray > thresh
    text = ""
    for y in im_bool:
      for x in y:
        if x:
          text += "□"
        else:
          text += "■"
      text += "\n"
    result_array.append(text)
  
    count += 1
  
    if round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100) % 10 == 0 and round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100) != 0 and round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100) != message_count:
      message_count = round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100)
      print("{}%完了".format(round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100)))

  next_message()

def play_music ():
  pygame.mixer.music.load('badapple.mp3') #CUSTOM:音声ファイル
  pygame.mixer.music.play()
  

def end_message():
  print("終了しました。")


def play_movie ():

  global text_c
  global root
  global cap_file
  global result_array

  width = int(cap_file.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT))
  tkinter_setting(width, height)
  textc_setting(width, height)
  
  timer = fpstimer.FPSTimer(30)

  play_music()
  for r in result_array:
    show_window(r)
    timer.sleep()
    text_c.delete("window_text")
  root.mainloop()
  end_message()

def main ():
  print("現在描画に必要なデータを生成中です...")
  print("終了まで結構時間かかりますので、その間に珈琲でもどうぞ")
  print("-----------------")
  make_frame()

if __name__ == '__main__':
  main()
