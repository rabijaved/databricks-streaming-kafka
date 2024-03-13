# Databricks notebook source
dbutils.widgets.dropdown("reset_all_data", "false", ["true", "false"], "Reset all data")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS 'streaming_sessionization';
# MAGIC CREATE SCHEMA IF NOT EXISTS 'user_events';
# MAGIC
# MAGIC USE CATALOG 'streaming_sessionization';
# MAGIC USE SCHEMA 'user_events';

# COMMAND ----------

# MAGIC %run ./00-global-setup $reset_all_data=$reset_all_data $db_prefix=retail

# COMMAND ----------

import pyspark.sql.functions as F
from pyspark.sql.functions import col
import sys
import time
import pandas as pd 

cloud_storage_path = cloud_storage_path+"/sessions"

#Reduce parallelism as we have just a few messages being produced
spark.conf.set("spark.default.parallelism", "12")
spark.conf.set("spark.sql.shuffle.partitions", "12")
