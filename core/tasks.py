
import os
import pandas as pd

from django.conf import settings
from celery import shared_task
from .models import Company


def process_csv_data_to_db(chunk_df):
    """
    Background task to process large CSV files asynchronously.
    """
    try:
        print(f"Number of chunks {len(chunk_df)} to be processed")
        # Insert rows in bulk to minimize database hits
        companies = [
            Company(
                name=row['name'],
                domain=row['domain'],
                year_founded=row.get('year founded'),
                industry=row['industry'],
                size_range=row['size range'],
                locality=row['locality'],
                country=row['country'],
                linkedin_url=row['linkedin url'],
                current_employee_estimate=row.get('current employee estimate'),
                total_employee_estimate=row.get('total employee estimate')
            )
            for _, row in chunk_df.iterrows()
        ]
        
        Company.objects.bulk_create(companies, batch_size=100000, ignore_conflicts=True)
        print(f"Saved {len(companies)} records to the database")

    except Exception as e:
        # Log the error or raise it
        print(f"An error occurred: {str(e)}")
        raise e


@shared_task
def save_csv_file(file_path):
    absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(f"Processing CSV file to: {absolute_file_path}")

    try:
        chunk_size = 100000  
        for chunk_df in pd.read_csv(absolute_file_path, chunksize=chunk_size):
            # process_chunk(chunk_df) 
            process_csv_data_to_db(chunk_df)
            print(f"Processed a chunk of {len(chunk_df)} rows")
    except Exception as e:
        print(f"Error while processing CSV: {e}")

