
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from .models import Company


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
        csv_file = request.FILES['file']
        file_path = default_storage.save(csv_file.name, csv_file)
        print(f"file_path: {file_path}")

        # Read the uploaded CSV file
        try:
            df = pd.read_csv(default_storage.open(file_path), nrows=1)
            if validate_csv_headers(list(df.columns)):
                print("\n CSV headers are valid! \n")

                # Call the background task to process the CSV file
                # save_csv_file.delay(file_path)

                messages.success(request, "CSV file successfully uploaded and data imported!")
                return redirect('upload') 

            else:
                print(f"CSV file does not have the required headers.")
                messages.error(request, "CSV file does not have the required headers.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'uploadCSV.html')


def build_query(request):
    context = {}
    query_count = 0
    data = None

    employees = {
        "1-10": "1-10",
        "11-50": "11-50",
        "51-200": "51-200",
        "201-500": "201-500",
        "501-1000": "501-1000",
        "1001-5000": "1001-5000",
        "5001-10000": "5001-10000",
        "10001+": "10001+"
    }

    if request.method == "GET":
        industry = Company.objects.values_list("industry", flat=True).distinct()
        
        year_founded = Company.objects.values_list("year_founded", flat=True).distinct() #? index 

        city = Company.objects.values_list("locality", flat=True).distinct()
        country = Company.objects.values_list("country", flat=True).distinct()
        employee_from = employees.keys()

        query_count += len(industry)
        query_count += len(year_founded)
        query_count += len(city)
        query_count += len(country)
        query_count += len(employee_from)
        query_count += len(employee_from)


    elif request.method == "POST":
        industry = request.POST.get("industry") if request.POST.get("industry") != "None" else None
        year_founded = request.POST.get("year_founded") if request.POST.get("year_founded") != "None" else None
        city = request.POST.get("city") if request.POST.get("city") != "None" else None
        country = request.POST.get("country") if request.POST.get("country") != "None" else None
        employee_from = request.POST.get("emp_from") if request.POST.get("emp_from") != "None" else None
        employee_to = request.POST.get("emp_to") if request.POST.get("emp_to") != "None" else None
        
        if industry:
            data = Company.objects.filter(industry=industry)
        
        if year_founded:
            data = Company.objects.filter(year_founded=year_founded)

        if city:
            data = Company.objects.filter(locality=city)

        if country:
            data = Company.objects.filter(country=country)

        if employee_from:
            data = Company.objects.filter(size_range=employee_from)
        
        if employee_to:
            data = Company.objects.filter(size_range=employee_to)

        query_count = data.count() if data else 0
        

    context["count"] = query_count if query_count else 0

    context["industry"] = list(industry) if industry else []
    context["year_founded"] = list(year_founded) if year_founded else []
    context["city"] = list(city) if city else []
    context["country"] = list(country) if country else []
    context["employee_from"] = list(employee_from) if employee_from else []
    context["employee_to"] =  context["employee_from"]
    
    # context["industry"] = [] 
    # context["year_founded"] = [] 
    # context["city"] = [] 
    # context["country"] = [] 
    # context["employee_from"] = employees.keys()
    # context["employee_to"] =  context["employee_from"]

    messages.success(request, f"{query_count} records found!")

    print(f"context: {context}")

    return render(request, "queryForm.html", context=context)


def manage_users(request):
    return render(request, "index.html")