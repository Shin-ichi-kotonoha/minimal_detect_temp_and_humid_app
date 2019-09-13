import sqlite3  # SQLiteを使うためのもの
import time
import traceback
from collections import OrderedDict
"""
データベース関連のクラス
"""
class Database:
    """
    ModelDefクラス:データの定義
    SQliteSQLクラス:SQLite用のSQLを生成するクラス
    Instanceクラス:データベースを操作するクラス
    """
    class ModelDef:
        class ValueType:
            """データの型をここに記載"""
            INTEGER = "integer"  # 整数
            TEXT = "text"  # 文字列
            REAL = "real"  # 浮動小数

        class ColumnName:
            """カラム名をここに記載"""
            ID = "id"  # 何番目の検知かを区別するためのカラム プライマリキー
            TIME = "time"  # 検知時刻 文字列の形式は'%Y-%m-%d %H:%M:%S'
            TEMPERATURE = "temperature"  # 温度
            HUMIDITY = "humidity"  # 湿度

        def __init__(self) -> dict:
            """
            @note:データベースの構造を忘れないように書いておく
            """
            self.defDict = OrderedDict()
            self.defDict["model_name"] = "detected_data"
            self.defDict["table_name"] = "detected_data"
            self.defDict["db_name"] = "database.db"
            self.defDict["fields"] = OrderedDict()
            self.defDict["fields"][self.ColumnName.ID] = {
                "column_name": self.ColumnName.ID,
                "type": self.ValueType.INTEGER,
                "jpn_name": "検知番号",
                "option": "primary key autoincrement"
            }
            self.defDict["fields"][self.ColumnName.TIME] = {
                "column_name": self.ColumnName.TIME,
                "type": self.ValueType.TEXT,
                "jpn_name": "時刻"
            }
            self.defDict["fields"][self.ColumnName.TEMPERATURE] = {
                "column_name": self.ColumnName.TEMPERATURE,
                "type": self.ValueType.REAL,
                "jpn_name": "温度"
            }
            self.defDict["fields"][self.ColumnName.HUMIDITY] = {
                "column_name": self.ColumnName.HUMIDITY,
                "type": self.ValueType.REAL,
                "jpn_name": "湿度"
            }

    # SQLite用のSQLを扱うためのクラス
    class SQliteSQL:

        @staticmethod
        def insert(record: dict):
            """
            データをSQLiteに追加するための関数
            :param record: dict  新規に登録したいデータのディクショナリー
            format of record
            record = {"fieldName":value,...} Database.ModelDef()の"fields"キー以下の構造と同じもの
            :return: sql: str
            """
            modeldef = Database.ModelDef().defDict
            sql = "insert into " + modeldef["table_name"]
            column = "("
            values = "("
            for key, value in record.items():
                column += key + ","
                if isinstance(value, str):
                    values += "\"" + value + "\" "
                else:
                    values += str(value)
                values += ","
            column = column[:-1]
            values = values[:-1]
            column += ")"
            values += ")"
            sql += column + " values" + values + ";"
            return sql

        @staticmethod
        def select(datetimeString: str, days: int):
            """
            データをSQLiteから取り出すための関数
            :param datetimeString: 形式'%Y-%m-%d %H:%M:%S'
            :param days: 何日前かの値 例：一週間前 days = -7
            :return:
            """
            modeldef = Database.ModelDef().defDict
            sql = "select "
            for field in modeldef["fields"]:
                sql += modeldef["fields"][field]["column_name"] + ","
            sql = sql[:-1]  # 最後のコンマを削除
            sql += " "
            sql += "from " + modeldef["table_name"] + " "
            # where句
            sql += "where time > datetime('"+datetimeString+"', '0 years', '0 months','"+str(days)+" days');"
            return sql

    class Instance:
        """
        データベースのインスタンス
        """
        def __init__(self):
            self.dbname = Database.ModelDef().defDict["db_name"]
            """
            データベース接続部分
            """
            try:
                print("DB connecting...")
                print("Connect:Start")
                startTime = time.time()

                self.connection = sqlite3.connect(self.dbname)  # Databaseのコネクション
                self.connection.row_factory = sqlite3.Row
                self.cursor = self.connection.cursor()  # Databaseのカーソル

                elapsed_time = time.time() - startTime
                print("Connect:Done. ElapsedTime=[%f]sec", elapsed_time)
                print("DB connected.")
            except sqlite3.DatabaseError as e:
                error, = e.args
                print(error)
                print(traceback.format_exc())
                print("Database接続に失敗しました。")
                raise

        """
        データの挿入
        """
        def insert(self, record):
            sql = Database.SQliteSQL.insert(record)
            try:
                # SQLの実行
                self.cursor.execute(sql)
                # データベースのコミット この操作で挿入したデータが確定する
                self.connection.commit()
            except:
                # エラーがあったらロールバックして元の状態に戻す
                self.connection.rollback()
                raise

        """
        データの検索
        """
        def select(self, datetimeString, days) -> [dict]:
            """
            :param datetimeString: 基準となる日付の文字列：文字列の形式は'%Y-%m-%d %H:%M:%S'
            :param days: 何日前かの日付　基準となる日付から一週間前 => -7
            :return: 該当するデータの配列
            """
            sql = Database.SQliteSQL.select(datetimeString, days)
            try:
                self.cursor.execute(sql)
                result = []
                data = self.cursor.fetchall()
                for row in data:
                    result.append(dict(row))
                return result
            except:
                raise

"""
初期設定時に呼ぶ関数。データベースの作成とテーブルの作成を行う。
"""
def create_table():
    model_def = Database.ModelDef().defDict
    sql = "create table if not exists " + model_def["table_name"] + "("
    for key, val in model_def["fields"].items():
        sql += val["column_name"] + " " + val["type"]
        if "option" in val:
            sql += " " + val["option"]
        sql += ","

    sql = sql[:-1]
    sql += ");"
    db = Database.Instance()
    db.cursor.execute(sql)
    db.connection.commit()
    print("create database and it's table.")

if __name__ == "__main__":
    create_table()








