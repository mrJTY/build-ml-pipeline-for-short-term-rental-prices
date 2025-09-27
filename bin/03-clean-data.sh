#!/usr/bin/env bash

set -e

conda run -n components \
  mlflow run . \
  -P steps=basic_cleaning \
  -P hydra_options="etl.min_price=50 etl.max_price=350"
