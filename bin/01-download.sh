#!/usr/bin/env bash

set -e

mlflow run . \
  -P steps=download
