#!/usr/bin/env bash
# We use the following commands before each run to ensure the app id is unique
#CURR_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S.%sZ") && APP_NAME=BasicDataframeRunner-$CURR_DATE

#CURR_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S.%sZ") && APP_NAME=BasicDataframeRunner-$CURR_DATE && spark-submit --class cmsc.basic.df.BasicDataframeRunner --master local[2] --conf spark.app.name=$APP_NAME target/basic-dataframe-1.0.0-SNAPSHOT-shaded.jar ../data/test-gsod/

#This is the Stage metrics, but I don't think we need these.
CURR_DATE=$(date -u +"%Y-%m-%dT%H:%M:%S.%sZ") && APP_NAME=BasicDataframeRunner-$CURR_DATE && spark-submit --class cmsc.basic.df.BasicDataframeRunner --master local[1] --conf spark.app.name=$APP_NAME --conf spark.extraListeners=ch.cern.sparkmeasure.FlightRecorderStageMetrics --conf spark.executorEnv.stageMetricsFileName=/tmp/$APP_NAME --conf spark.executorEnv.stageMetricsFormat="json" target/basic-dataframe-1.0.0-SNAPSHOT-shaded.jar ../data/test-gsod/