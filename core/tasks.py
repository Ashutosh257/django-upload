
import pandas as pd
from celery import shared_task
from .models import Company

@shared_task
def process_csv_file(file_path):
    """
    Background task to process large CSV files asynchronously.
    """
    try:
        print(f"Processing CSV file: {file_path}")
        # Read CSV file in chunks to avoid memory issues
        chunk_size = 10000  # Adjust the chunk size based on memory capacity
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
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
                for index, row in chunk.iterrows()
            ]
            Company.objects.bulk_create(companies, ignore_conflicts=True)
    except Exception as e:
        # Log the error or raise it
        print(f"An error occurred: {str(e)}")
        raise e
