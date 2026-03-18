# -*- coding: utf-8 -*-
#spark-submit /home/hadoop/heart_system/backend/app.py
from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.linalg import Vectors
import pymysql
from flask_cors import CORS

db = pymysql.connect(
    host="localhost",
    user="root",
    password="",#没有密码
    database="heart_system"
)

app = Flask(__name__)
CORS(app)

# ==============================
# 启动 Spark
# ==============================

spark = SparkSession.builder \
    .appName("HeartPredictionAPI") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# ==============================
# 加载模型
# ==============================

model = RandomForestClassificationModel.load(
    "hdfs://192.168.153.130:9000/model/heart_rf"
)

print("模型加载成功")


@app.route("/")
def home():
    return jsonify({"message":"Heart Disease Prediction API"})

@app.route("/register", methods=["POST"])
def register():

    data = request.json
    username = data["username"]
    password = data["password"]

    cursor = db.cursor()

    # 先检查用户是否存在
    sql = "SELECT id FROM user WHERE username=%s"
    cursor.execute(sql,(username,))
    user = cursor.fetchone()

    if user:
        return jsonify({"message":"user exists"})

    sql = """
    INSERT INTO user (username,password,create_time)
    VALUES (%s,%s,NOW())
    """

    cursor.execute(sql,(username,password))
    db.commit()

    return jsonify({"message":"register success"})


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    cursor = db.cursor()

    sql = """
    SELECT id FROM user
    WHERE username=%s AND password=%s
    """

    cursor.execute(sql,(username,password))

    user = cursor.fetchone()

    if user:
        return jsonify({
            "message":"login success",
            "user_id":user[0]
        })
    else:
        return jsonify({
            "message":"login failed"
        })

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    user_id = data["user_id"]
    features = [
        data["Age"],
        data["Sex"],
        data["ChestPain"],
        data["RestBP"],
        data["Chol"],
        data["Fbs"],
        data["RestECG"],
        data["MaxHR"],
        data["ExAng"],
        data["Oldpeak"],
        data["Slope"],
        data["Ca"],
        data["Thal"]
    ]

    df = spark.createDataFrame(
        [(Vectors.dense(features),)],
        ["features"]
    )

    result = model.transform(df)
    row = result.select("prediction","probability").collect()[0]

    prediction = row["prediction"]
    probability = float(row["probability"][1])
    #probability[1] = 患病概率

    cursor = db.cursor()
    sql = """
    INSERT INTO prediction_record
    (user_id,age,sex,chestPain,restBP,chol,fbs,restECG,maxHR,exAng,oldpeak,slope,ca,thal,prediction,probability,create_time)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
    """
    cursor.execute(sql,(
    user_id,
    data["Age"],
    data["Sex"],
    data["ChestPain"],
    data["RestBP"],
    data["Chol"],
    data["Fbs"],
    data["RestECG"],
    data["MaxHR"],
    data["ExAng"],
    data["Oldpeak"],
    data["Slope"],
    data["Ca"],
    data["Thal"],
    prediction,
    probability    
    ))
    db.commit()

    risk="High Risk"if prediction ==1 else "Low Risk"

    return jsonify({
        "prediction": int(prediction),
        "risk": risk,
        "probability": probability
    })

@app.route("/change_password", methods=["POST"])
def change_password():

    data = request.json

    user_id = data["user_id"]
    new_password = data["password"]

    cursor = db.cursor()

    sql = """
    UPDATE user
    SET password=%s
    WHERE id=%s
    """

    cursor.execute(sql,(new_password,user_id))
    db.commit()

    return jsonify({
        "message":"password updated"
    })
@app.route("/history", methods=["GET"])
def history():

    user_id = request.args.get("user_id")

    cursor = db.cursor()

    sql = """
    SELECT age,sex,chestPain,restBP,chol,fbs,restECG,maxHR,exAng,oldpeak,slope,ca,thal,prediction,probability,create_time
    FROM prediction_record
    WHERE user_id=%s
    ORDER BY id ASC
    LIMIT 20
    """

    cursor.execute(sql,(user_id,))
    rows = cursor.fetchall()

    result = []

    for r in rows:
        result.append({
            "age": r[0],
            "sex": r[1],
            "chestPain": r[2],
            "restBP": r[3],
            "chol": r[4],
            "fbs": r[5],
            "restECG": r[6],
            "maxHR": r[7],
            "exAng": r[8],
            "oldpeak": r[9],
            "slope": r[10],
            "ca": r[11],
            "thal": r[12],
            "prediction": r[13],
            "probability": r[14],
            "time": str(r[15])
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)