#!/usr/bin/env python
"""
[An example of a step using MLflow and Weights & Biases]: Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import pandas as pd
import wandb

# Geographic boundaries for NYC area
# These coordinates define the bounding box for valid NYC rental properties
MIN_LONGITUDE = -74.25  # Western boundary (Staten Island)
MAX_LONGITUDE = -73.50  # Eastern boundary (Queens)
MIN_LATITUDE = 40.5  # Southern boundary (Staten Island)
MAX_LATITUDE = 41.2  # Northern boundary (Bronx)

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info(f"Downloading artifact {args.input_artifact}")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    # Read the data
    logger.info("Reading data")
    df = pd.read_csv(artifact_local_path)

    # Drop outliers based on price
    logger.info(f"Dropping price outliers outside range [{args.min_price}, {args.max_price}]")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info(f"Data shape after price filtering: {df.shape}")

    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Drop rows with invalid coordinates (as mentioned in README for sample2.csv)
    logger.info("Filtering geographic outliers")
    idx = df['longitude'].between(MIN_LONGITUDE, MAX_LONGITUDE) & df['latitude'].between(MIN_LATITUDE, MAX_LATITUDE)
    df = df[idx].copy()
    logger.info(f"Data shape after geographic filtering: {df.shape}")

    # Save cleaned data
    logger.info("Saving cleaned data")
    # save this to clean_sample.csv
    df.to_csv(args.output_artifact, index=False)

    # Upload it to W&B
    logger.info(f"Uploading {args.output_artifact} to Weights & Biases")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    # Upload clean_sample.csv to wandb artifact
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

    logger.info("Data cleaning completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="The input artifact that may have unclean data",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="The cleaned output artifact to be saved in wandb",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="The type or tag of an output. eg: cleaned_sample as opposed to raw_data, model_export",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="The output description, eg: data with outliers removed and cleaned",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price that for rental prices",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price for the rental price",
        required=True
    )

    args = parser.parse_args()

    go(args)
