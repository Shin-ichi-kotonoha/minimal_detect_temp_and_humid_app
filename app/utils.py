from datetime import datetime
import RPi.GPIO as GPIO
import time

import dht11
from database import Database


class DateTimeConvert(object):
    """
    いちいち時刻のフォーマットを気にするのが面倒なので定義しておく
    """

    @staticmethod
    def string2datetime(string) -> datetime:
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def datetime2string(dateTime: datetime) -> str:
        return dateTime.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def string2datetimeYmdStyle(string) -> datetime:
        return datetime.strptime(string, '%Y-%m-%d')


# DHTからデータを取得してデータベースに追加する
class DetectDHT11(object):
    """
    デフォルトはGPIO14番ピン
    """
    def __init__(self, pin=14):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        self.module = dht11.DHT11(pin=pin)

    """
    DTH11から値を取得する
    """
    def get_value(self) -> dict:
        i = 0
        while i < 100:
            result = self.module.read()
            if result.is_valid():
                value = {"temperature": result.temperature,
                         "humidity": result.humidity,
                         "time": DateTimeConvert.datetime2string(datetime.now())}
                return value
            i += 1
            time.sleep(1)
        return None

    """
    データをデータベースに追加
    """
    def registData(self):
        record = self.get_value()
        if record is None:
            print("データの検知に失敗しました。")
            return
        else:
            db = Database.Instance()
            db.insert(record)
            print("データの追加が完了しました。")
            return
