#!/bin/bash

# Install conda dependencies for ML pipeline project

echo "Installing conda environments..."

# Check if environment files exist
if [ ! -f "environment.yml" ]; then
    echo "Error: environment.yml not found in current directory"
    exit 1
fi

if [ ! -f "conda.yml" ]; then
    echo "Error: conda.yml not found in current directory"
    exit 1
fi

# Create development environment from environment.yml
echo "Creating development environment (nyc_airbnb_dev)..."
conda env create -f environment.yml

# Create components environment from conda.yml
echo "Creating components environment for MLflow..."
conda env create -f conda.yml

echo "Both environments created successfully!"
echo "Development environment: conda activate nyc_airbnb_dev"
echo "Components environment: conda activate components"
