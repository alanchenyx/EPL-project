"""

Scripts for spark job submission and mongoDB operations

"""


spark-submit \
    --driver-memory 2g \
    --executor-memory 6g \
    --total-executor-cores 6 \
    --master spark://115.146.92.116:7077  \
    --packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 \
    --conf spark.debug.maxToStringFields=100 \
    preprocess.py



mongodump --db tweet --collection tweet_raw --username admin --password 88404 --authenticationDatabase admin --out \mnt\mongodb\
mongorestore --db tweet --collection tweet_reduce /mnt/dump/tweet/tweet_raw.bson --username admin --password 88404 --authenticationDatabase admin --drop


--conf spark.debug.maxToStringFields=100
CORES=6
DR_MEM=2g
EX_MEM=6g
    --driver-library-path /mnt/hadoop-2.7.4/lib/native \
        --driver-class-path mongodb-driver-3.5.0.jar \
    --packages org.mongodb.spark:mongo-spark-connector_2.10:2.2.0

