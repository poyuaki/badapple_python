# bad apple!!

<img src="https://github.com/poyuaki/badapple_python/blob/image/sukusyo.png" alt="bad apple!のスクショ" height="400">

# 内容

このプログラムは、bad apple!(feat. nomico)のPVをPythonを用いて再現しよう！という内容です。
実はYoutube並びにGithub上に似たようなプログラムがあったしなんならそっちの方が結構良かったりするんですが、一応公開しますw

# 使い方

- このプログラムをダウンロードします。上部の「Code」という緑のボタンから「Download ZIP」を選択、その後解凍します

- まず、badapple.pyと同じ階層に、badapple.mp3とbadapple.mp4を置きます(既に用意はしてますが、著作権とかの問題があり次第削除します)

- badapple.pyを普通に動作させます

- データ生成が完了したらエンターキーを押して、楽しみます

# Q&A

1. サイズが収まらない<br>
  申し訳ありませんが、badapple.py内の「CUSTOM」というコメントがある箇所の数値を調整してください

2. 音とズレる<br>
  1番と同様、badapple.py内の「CUSTOM」というコメントがある箇所の数値を調整してください。<br>
  原因は多分、描画するときの処理時間があるからだと思いますので、描画するときの文字数を減らすなどの対策を行うと良いかもしれません

3. ウインドウが自動的に閉じない<br>
  ウインドウを閉じる方法がよくわからなかったので、申し訳ありませんが手動でウインドウを閉じてください

4. エラー吐きまくってる<br>
  ライブラリのインストールをしていないのかもしれません。<br>
  この作品では、

  - openCV
  - pygame
  - fpstimer
  - tkinter
  - screeninfo

  が必要です。

5. 特にない<br>
  bad apple!!を楽しんでください

# 感想

小さい頃から、bad apple!!のPVのアレンジ(?)をめちゃくちゃ見てて、「うわぁ、こういうのやりたいなぁ」と思ってたので、どんな形であれ自分の手でアレンジができたのは本当に嬉しいです。もちろん、改善すべき点なんてあげればキリがないんですが、今はもうちょっとだけ幻想入りさせてもらいます。。。

## そもそも、「bad apple!!」とは？

元々は、東方旧作の弾幕STGシリーズ、「東方幻想郷」の3面ステージの道中BGM。<br>
それをnomicoがカバーした「bad apple!! feat. nomico」と、そのPVが爆発的人気を誇り、今や東方projectの顔とも呼べる曲となった。<br>
また、PVが影絵なので、二値化できる作品であり、それを利用して今回のプログラムの他にも様々なオリジナリティのあるアレンジが公開されている。このプログラムでも、PythonのopenCVを用いて動画を二値化しているが、その処理を施しても違和感のない仕上がりとなっている。

実は、PVに関しては絵コンテから、神様が影絵へと変化させたのだが、影絵の元である絵コンテでは、最後に出てくる霊夢、魔理沙は旧作のキャラクターとなっている。
