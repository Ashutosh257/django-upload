
import pandas as pd
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from .tasks import process_csv_file

from rest_framework.response import Response


# Expected headers
REQUIRED_HEADERS = ['company_id', 'name', 'domain', 'year founded', 'industry',
       'size range', 'locality', 'country', 'linkedin url',
       'current employee estimate', 'total employee estimate']

def validate_csv_headers(headers):
    return all(header in headers for header in REQUIRED_HEADERS)

def index(request): 
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")

def logout(request):
    return render(request, "logout.html")


def upload_csv(request):
    if request.method == 'POST':
        # get the file from the request
        csv_file = request.FILES['file']
        print(f"csv_file: {csv_file}")
        print(f"csv_file.temporary_file_path(): {csv_file.temporary_file_path()}")
        # Read the uploaded CSV file
        try:
            # Using pandas to handle large file validation efficiently
            df = pd.read_csv(csv_file, chunksize=2)
            first_chunk = next(df)

            # Now you can print the columns of the first chunk
            print(f"df columns: {first_chunk.columns}")

            # Validate headers
            if validate_csv_headers(first_chunk.columns):
                print("CSV headers are valid!")
                # Process the CSV and insert into the database
                # bulk insert or handle the data row by row

                process_csv_file.delay(csv_file.temporary_file_path())

                messages.success(request, "CSV file successfully uploaded and data imported!")
                return redirect('upload_csv')
            else:
                print(f"CSV file does not have the required headers.")
                messages.error(request, "CSV file does not have the required headers.")
        except pd.errors.EmptyDataError:
            print(f"The uploaded file is empty.")
            messages.error(request, "The uploaded file is empty.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'uploadCSV.html')


def build_query(request):
    collection = ["Company", "Person"]
    return render(request, "queryForm.html", {"collections": collection})


def manage_users(request):
    return render(request, "index.html")