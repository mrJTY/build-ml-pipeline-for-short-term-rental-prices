#!/usr/bin/env bash

set -e

mlflow run . \
  -P steps=basic_cleaning \
  -P hydra_options="etl.min_price=50 etl.max_price=350"
