
from tornado.web import RequestHandler
from datetime import datetime
from utils import DateTimeConvert
from database import Database


class Handler(RequestHandler):
    """
    HTTPのgetメソッドを使うのでgetを定義する
    これはtornadoの仕様
    """
    def get(self):

        dt = datetime.now()  # 現在の時刻を取得
        datetimeString = DateTimeConvert.datetime2string(dt)
        days = -7
        database = Database.Instance()
        dataList = database.select(datetimeString=datetimeString, days=days)

        temperatures = []
        humidities = []

        # 取得したデータを加工
        for dataDict in dataList:
            time = DateTimeConvert.string2datetime(dataDict["time"])
            temperatures.append({"x": time, "y":dataDict["temperature"]})
            humidities.append({"x": time, "y": dataDict["humidity"]})

        self.render("index.html", temperatures=temperatures, humidities=humidities)