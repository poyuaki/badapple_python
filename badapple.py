#################################
#
# 何かおかしいな？って思ったり、リポジトリとは異なるファイルを適用する際は、「CUSTOM」とコメントされている箇所を変更してみてください。
#
#################################
from unittest import result
import cv2
import time
import numpy as np
import tkinter
import fpstimer
import pygame.mixer
import math
from screeninfo import get_monitors
import random
import json
import copy

from badapple_convert import make_frame_c

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
  print("{}x{}".format(m.width, m.height))

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
  global window_size

  gyo_su = len(text.split('\n'))

  id_window_text = text_c.create_text(
    window_text["width"],
    window_text["height"],
    text = text,
    font = ('',math.floor(window_size["height"] / gyo_su)), # CUSTOM:1文字あたりの大きさ(初期値：自動的に生成)
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
  debug_flag["fps"] = False
  if user_input == "debug_fps":
    debug_flag["fps"] = True

  play_movie()


def choice_block ():
  print("-----------------")
  print("バグモードを使用しますか？")
  print("このモードを使用すると生成にめちゃくちゃ時間がかかります。")
  print("ただし、結構エモくなるのでオススメだったりします")
  user_ans = ""
  while True:
    user_ans = input("バグモードを使用しますか？(y / n) => ")
    if user_ans != "y" and user_ans != "n":
      print("正しく入力してください。")
    else:
      break
  if user_ans == "y":
    return True, []
  else:
    print("ここからは、白い部分と黒い部分を表現するテキストを入力します。")
    print("<<全角>>にしないとヤベェことになるので、<<全角>>で入力してください。")
    print("空白のまま入力するとデフォルトになります。")
    white_char = input("白い部分を入力してください => ")
    black_char = input("黒い部分を入力してください => ")
    if not white_char:
      white_char = "□"
    if not black_char:
      black_char = "■"
    return False, [white_char, black_char]

def make_frame():
  """
    フレームごとの画像(文字列)を作成する関数
  """

  global cap_file

  return make_frame_c(cap_file)

def play_music ():
  """
    音楽を再生
  """
  pygame.mixer.music.load('badapple.mp3') #CUSTOM:音声ファイル
  pygame.mixer.music.play(start=0.55) # CUSTOM: 再生位置
  

def end_message():
  print("終了しました。")
  pygame.mixer.music.stop()

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

now_str_array = []

def get_str_by_now_str_array ():
  global now_str_array
  return '\n'.join(map(str, now_str_array))

def make_str (frame_count):
  global result_array
  global now_str_array
  y_len = result_array[0][len(result_array[0]) - 1][1] # 高さ
  x_len = result_array[0][len(result_array[0]) - 1][0] # 幅

  def make_str_mark (val):
    if val == 1:
      return "□"
    else:
      return "■"

  if len(now_str_array) == 0: # now_str_arrayの初期化
    for y in range(y_len):
      append_str = ''
      for x in range(x_len):
        for c in result_array[0]:
          if c[0] == x and c[1] == y:
            append_str = append_str + make_str_mark(c[2])
            break
      now_str_array.append(str(append_str))

  def is_here (x, y, arr):
    for a in arr:
      if a[0] == x and a[1] == y:
        return a[2]
    return "none"

  for y in range(y_len):
    text = ""
    for x in range(x_len):
      res_judge = is_here(x, y, result_array[frame_count])
      if res_judge != "none":
        text = text + make_str_mark(res_judge)
      else:
        split_array = copy.copy(now_str_array)
        text = text + split_array[y][x: x + 1]
    now_str_array[y] = text

      

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
    make_str(frame_count)
    r = get_str_by_now_str_array()
    show_window(r)
    timer.sleep()
    text_c.delete("window_text")
    count, run_time, frame_count = adjustment_fps(count, run_time, frame_count)
  root.destroy()
  end_message()

def make_dots_file (file_name):
  """
    dotファイルを作成する関数

      Parameters
      ----------
      file_name : str
        dotsファイルを作成する際のファイル名
  """

  dots_file = make_frame()
  f = open('dots/dotslist_{}.txt'.format(file_name),'w')
  f.write('??'.join(map(str, dots_file)))

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
      result_array = s.split('??')
      for i in range(len(result_array)):
        result_array[i] = eval(result_array[i])
      next_message()
      print("エラーが発生しました。")
      print("もしかしたらファイル名が間違っているかもしれません。")
    elif user_input == 4:
      print("Bye")
      break

if __name__ == '__main__':
  main()
