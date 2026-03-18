# -*- coding: utf-8 -*-
#spark-submit /home/hadoop/heart_system/spark/train_model.py
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import datetime

LOG_FILE = "/home/hadoop/heart_system/spark/train_log.txt"
open(LOG_FILE, "w").close()
def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(str(datetime.datetime.now()) + " " + str(msg) + "\n")
# 启动 Spark
spark = SparkSession.builder \
    .appName("HeartDiseasePrediction") \
    .config("spark.ui.showConsoleProgress","false") \
    .getOrCreate()
log("Spark 启动成功")

# ==============================
# 1 读取数据
# ==============================

df = spark.read.csv(
    "hdfs://192.168.153.130:9000/heart/heart.csv",
    header=True,
    inferSchema=True
)

log("数据加载完成")

# ==============================
# 2 特征工程
# ==============================

indexers = [
    StringIndexer(inputCol="ChestPain", outputCol="ChestPain_index"),
    StringIndexer(inputCol="Ca", outputCol="Ca_index"),
    StringIndexer(inputCol="Thal", outputCol="Thal_index"),
    StringIndexer(inputCol="AHD", outputCol="label")
]

for indexer in indexers:
    df = indexer.fit(df).transform(df)

assembler = VectorAssembler(
    inputCols=[
        "Age",
        "Sex",
        "ChestPain_index",
        "RestBP",
        "Chol",
        "Fbs",
        "RestECG",
        "MaxHR",
        "ExAng",
        "Oldpeak",
        "Slope",
        "Ca_index",
        "Thal_index"
    ],
    outputCol="features"
)

data = assembler.transform(df)

log("特征工程完成")

# ==============================
# 3 模型训练
# ==============================

# Logistic Regression
lr = LogisticRegression(
    featuresCol="features",
    labelCol="label"
)

lr_model = lr.fit(data)

log("Logistic Regression 训练完成")

# Random Forest
rf = RandomForestClassifier(
    featuresCol="features",
    labelCol="label",
    numTrees=100
)

rf_model = rf.fit(data)

log("Random Forest 训练完成")

# GBT
gbt = GBTClassifier(
    featuresCol="features",
    labelCol="label",
    maxIter=50
)

gbt_model = gbt.fit(data)

log("GBT 训练完成")

# ==============================
# 4 模型预测
# ==============================

lr_predictions = lr_model.transform(data)
rf_predictions = rf_model.transform(data)
gbt_predictions = gbt_model.transform(data)

# ==============================
# 5 模型评估
# ==============================

accuracy_eval = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"
)

precision_eval = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="weightedPrecision"
)

recall_eval = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="weightedRecall"
)

auc_eval = BinaryClassificationEvaluator(
    labelCol="label",
    rawPredictionCol="probability",
    metricName="areaUnderROC"
)

def evaluate(name, predictions):

    accuracy = accuracy_eval.evaluate(predictions)
    precision = precision_eval.evaluate(predictions)
    recall = recall_eval.evaluate(predictions)

    log("===== {} =====".format(name))
    log("Accuracy = {}".format(accuracy))
    log("Precision = {}".format(precision))
    log("Recall = {}".format(recall))

    # 只有存在 rawPrediction 才计算 AUC
    if "rawPrediction" in predictions.columns:
        auc = auc_eval.evaluate(predictions)
        log("AUC = {}".format(auc))


evaluate("Logistic Regression", lr_predictions)
evaluate("Random Forest", rf_predictions)
evaluate("GBT", gbt_predictions)


# ==============================
# 7 示例输出
# ==============================
lr_sample = lr_predictions.select("features","label","prediction").take(10)
log("===== Logistic Regression 预测样例 =====")
for r in lr_sample:
    log(r)

rf_sample = rf_predictions.select("features","label","prediction").take(10)
log("===== Random Forest 预测样例 =====")
for r in rf_sample:
    log(r)

gbt_sample = gbt_predictions.select("features","label","prediction").take(10)
log("===== GBT 预测样例 =====")
for r in gbt_sample:
    log(r)

# ==============================
# 8 保存模型
# ==============================

lr_model.write().overwrite().save(
    "hdfs://192.168.153.130:9000/model/heart_lr"
)

rf_model.write().overwrite().save(
    "hdfs://192.168.153.130:9000/model/heart_rf"
)

gbt_model.write().overwrite().save(
    "hdfs://192.168.153.130:9000/model/heart_gbt"
)

log("模型保存完成")

# ==============================
# 7 关闭 Spark
# ==============================

spark.stop()

log("训练流程结束")