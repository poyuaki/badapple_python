#################################
#
# 何かおかしいな？って思ったり、リポジトリとは異なるファイルを適用する際は、「CUSTOM」とコメントされている箇所を変更してみてください。
#
#################################

import cv2
import time
import numpy as np
import tkinter
import fpstimer
import pygame.mixer
import math
from screeninfo import get_monitors

# テキストの位置
window_text = {
  "width": 0,
  "height": 0
}

# ウインドウサイズ
window_size = {
  "width": 1920,
  "height": 1080
}

debug_flag = {
  "fps": False
}

for m in get_monitors(): # モニターの幅と高さを取得
  window_size["width"] = m.width
  window_size["height"] = m.height

root = None
text_c = None

result_array = []

cap_file = cv2.VideoCapture('badapple.mp4') #CUSTOM:動画ファイル

def tkinter_setting ():
  """
    tkinterの生成
  """

  global root
  global window_size

  root = tkinter.Tk()
  root.title("bad apple!")
  root.geometry("{}x{}".format(window_size["width"], window_size["height"])) # ウインドウサイズ
  root.bind('<Configure>', change_size) # 関数のバインド(連携)

def textc_setting ():
  """
    canvasの作成
  """

  global text_c
  global window_size

  text_c = tkinter.Canvas( # テキストを描くキャンバスを生成
    root,
    width = window_size["width"] / 2,
    height = window_size["height"] / 2,
    background = '#ffffff'
  )
  text_c.pack(fill = tkinter.BOTH, expand=True) # ウインドウサイズをリサイズ

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
  """
    文字列を表示する

    Parameters
      ----------
      text : str
        表示させたい文字列
  """

  global text_c
  global id_window_text
  global window_text

  id_window_text = text_c.create_text(
    window_text["width"],
    window_text["height"],
    text = text,
    font = ('', 7), # CUSTOM:1文字あたりの大きさ
    fill = "#000000",
    tag="window_text"
  )
  text_c.update()

def next_message():
  """
    フレームの生成が完了したときに表示するメッセージをまとめた関数
  """

  global debug_flag

  pygame.mixer.init() #初期化
  print("-----------------")
  print("生成が完了しました。")
  print("残念ながら私の技量では自動でウインドウを閉じることができません。")
  print("申し訳ありませんが、再生が終わりましたら手動でウインドウを閉じてください。")
  print("また、スペックの低いパソコンだと、処理の関係上フレームがズレることがあります。")
  print("その場合は、プログラムファイル中の「CUSTOM」の部分を調整してください。")
  print("-----------------")
  user_input = input("エンターキーを押すと再生が始まります。：")
  if user_input == "debug_fps":
    debug_flag["fps"] = True

  play_movie()


def make_frame():
  """
    フレームごとの画像(文字列)を作成する関数
  """

  global cap_file

  width = int(cap_file.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT))

  count = 0 # どれぐらい完了したかを計測

  message_count = 0 # 現在表示しているパーセントを記録

  dots_array = []

  while True:

    ret, frame = cap_file.read() # フレームを取得

    if ret == False: # もしフレームがなければ終了する => 動画が終わった
      break

    frame = cv2.resize(frame , (int(width*0.55), int(height*0.55))) # CUSTOM:動画の画質×0.55(初期値)。解像度を落とす場合は値を小さくしてください
    im_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    thresh = 128
    im_bool = im_gray > thresh # 2値化
    text = ""
    for y in im_bool:
      for x in y:
        if x: # もしも白い部分なら
          text += "□"
        else: # もしも黒い部分なら
          text += "■"
      text += "\n"
    dots_array.append(text)
  
    count += 1
  
    if round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100) % 10 == 0 and round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100) != 0 and round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100) != message_count:
      message_count = round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100)
      print("{}%完了".format(round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100)))
  
  return dots_array

def play_music ():
  """
    音楽を再生
  """
  pygame.mixer.music.load('badapple.mp3') #CUSTOM:音声ファイル
  pygame.mixer.music.play(start=0.5) # CUSTOM: 再生位置
  

def end_message():
  print("終了しました。")

def adjustment_fps (count, run_time, frame_count):
  """
    現在のfpsと通常のfpsを比較し、遅延している場合はそのフレーム数分だけショートカットする関数

    Parameters
    ----------
    count : int
      フレーム数(1秒間隔)
    run_time : int
      時間
    frame_count : int
      現在のフレーム数
    
    Returns
    -------
    count : int
      フレーム数(調整済)
    run_time : int
      時間(1秒経過したらリセット)
    frame_count : int
      ショートカットを考慮したフレーム数
  """
  global cap_file
  global debug_flag

  if time.time() - run_time < 1:
    frame_count += 1
    count += 1
    return count, run_time, frame_count
  else:
    fps = cap_file.get(cv2.CAP_PROP_FPS)
    shortcut = 0
    shortcut = math.floor(fps - count) # 通常のフレームとの差を取得
    if shortcut == 0: # ちょうどなら普通に進める
      frame_count += 1
    
    if debug_flag["fps"]:
      print("fps(default):{}".format(fps))
      print("fps(now):{}".format(count))
      print("shortcut:{}".format(shortcut))
    frame_count += shortcut
    return 0, time.time(), frame_count

def play_movie ():
  """
    生成したデータを画面に描画し、動画にする関数
  """

  global text_c
  global root
  global cap_file
  global result_array

  # ウインドウの生成
  tkinter_setting()
  textc_setting()
  
  timer = fpstimer.FPSTimer(30) # CUSTOM:動画のfps

  play_music()

  count = 0 # 1秒あたりのフレーム数
  run_time = time.time() # 1秒を計測
  shortcut = 0 # 必要なショートカットフレーム数

  frame_count = 0
  while frame_count < cap_file.get(cv2.CAP_PROP_FRAME_COUNT):
    r = result_array[frame_count]
    show_window(r)
    timer.sleep()
    text_c.delete("window_text")
    count, run_time, frame_count = adjustment_fps(count, run_time, frame_count)

  root.mainloop()
  end_message()

def make_dots_file (file_name):
  dots_file = make_frame()
  f = open('dots/dotslist_{}.txt'.format(file_name),'w')
  f.write(','.join(map(str, dots_file)))

def main ():
  """
    メイン処理という名の、ただ最初に表示するテキストとかをまとめた関数
  """

  global result_array

  choise_list = ["1", "2", "3", "4"]
  while True:
    print("1) 動画を読み込んでから再生")
    print("2) 動画を読み込んでファイルを生成")
    print("3) 生成したファイルから再生")
    print("4) 終了する")
    user_input = ""
    while True:
      user_input = input("番号を入力してください => ")
      if user_input in choise_list:
        break
      print("適切な値を入力してください")
    
    user_input = int(user_input)

    if user_input == 1:
      print("現在描画に必要なデータを生成中です...")
      print("終了まで結構時間かかりますので、その間に珈琲でもどうぞ")
      print("-----------------")
      result_array = make_frame()
      next_message()
    elif user_input == 2:
      print("======= 注意事項 =======")
      print("同じ階層にdotsフォルダがありますか？ないとエラーが発生するので、先に作成しておいてくださいね")
      print("普通に100MBは超えるファイルになります。容量に注意してください")
      print("=======================")
      print("dotslist_〇〇.txtの、〇〇に入る名前を入力してください。")
      print("同じ名前のファイルが存在する場合、上書きされます。")
      file_name = input("〇〇 => ")
      make_dots_file(file_name)
      continue
    elif user_input == 3:
      print("dotslist_〇〇.txtの、〇〇に入る名前を入力してください。")
      file_name = input("〇〇 => ")
      f = open('dots/dotslist_{}.txt'.format(file_name),'r')
      s = f.read()
      result_array = s.split(',')
      next_message()
    elif user_input == 4:
      print("Bye")
      break

if __name__ == '__main__':
  main()
