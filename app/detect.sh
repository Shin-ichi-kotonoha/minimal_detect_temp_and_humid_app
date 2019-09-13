#!bin/sh
#cronで定期実行してデータを蓄積するためのシェルスクリプト

#本プロジェクトのappディレクトリに移動
#以下のディレクトリをご自身の環境に合わせてください。
#わからないようならRaspberry piのターミナルでappディレクトリに移動しpwdというコマンドを打つと出てきます。
cd /home/pi/testpi/detectTempAndHumid/detectTempAndHumid/app

#検知用のpythonプログラムを実行
python3 ./detect.py