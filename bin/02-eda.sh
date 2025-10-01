#!/usr/bin/env bash

set -e

conda run -n nyc_airbnb_dev \
  mlflow run src/eda
