
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
                # return redirect('upload') 

            else:
                print(f"CSV file does not have the required headers.")
                messages.error(request, "CSV file does not have the required headers.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")

    messages.success(request, "Hello bro!")
    return render(request, 'uploadCSV.html')


def build_query(request):
    context = {}
    query_count = 0
    data = None

    if request.method == "GET":
        industry = Company.objects.values_list("industry", flat=True).distinct()
        year_founded = Company.objects.values_list("year_founded", flat=True).distinct()
        city = Company.objects.values_list("locality", flat=True).distinct()
        country = Company.objects.values_list("country", flat=True).distinct()
        employee_from = Company.objects.values_list("size_range", flat=True).distinct()

        query_count += len(industry)
        query_count += len(year_founded)
        query_count += len(city)
        query_count += len(country)
        query_count += len(employee_from)
        query_count += len(employee_from)


    elif request.method == "POST":
        industry = request.POST.get("industry")
        year_founded = request.POST.get("yearFounded")
        city = request.POST.get("city")
        country = request.POST.get("country")
        employee_from = request.POST.get("empFrom")
        employee_to = request.POST.get("empTo")

        print(f"industry: {industry}")
        print(type(industry))

        print(f"year_founded: {year_founded}")
        print(type(year_founded))
        
        
        if industry != "None":
            data = Company.objects.filter(industry=industry)
        
        if year_founded != "None":
            data = Company.objects.filter(year_founded=year_founded)

        if city != "None":
            data = Company.objects.filter(locality=city)

        if country != "None":
            data = Company.objects.filter(country=country)

        if employee_from != "None":
            data = Company.objects.filter(size_range=employee_from)
        
        if employee_to != "None":
            data = Company.objects.filter(size_range=employee_to)

        query_count = data.count() if data else 0
        

    context["count"] = query_count if query_count else 0

    context["industry"] = list(industry)
    context["year_founded"] = list(year_founded)
    context["city"] = list(city)
    context["country"] = list(country)
    context["employee_from"] = list(employee_from)
    context["employee_to"] = list(employee_from)

    # context["industry"] = []
    # context["year_founded"] = []
    # context["city"] = []
    # context["country"] = []
    # context["employee_from"] = []
    # context["employee_to"] = []
    
    return render(request, "queryForm.html", context=context)


def manage_users(request):
    return render(request, "index.html")