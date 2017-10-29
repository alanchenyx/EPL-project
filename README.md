# EPL-project
Premier League Event Detection Based on Sentiment Changes in Social Media

Video Demo: https://youtu.be/6a2vsYxhlD4

All match&player info used in this project is in doc folder

Clone this repo and run index.html in web folder to visualise

Key files:

preprocess.py - spark application for preprocessing and classify sentiment using existing pkl model

spark_job.sh - scrpits used for running spark application

prediction.py - generate time-serialised data and give predictions

ml.ipynb - python notebook for machine learning 

process_tweet.py - preprocessing functions


#Todos:

Refactoring code

Host webApp in cloud and intergrate with database
