from django.shortcuts import render, redirect
from .models import Student
from django.shortcuts import render
from django.http import HttpResponse
from . import views
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponse
import errno
import os
import requests
from bs4 import BeautifulSoup
from .models import Book


def my_view(request):
    try:
        # Your view logic here
        return HttpResponse("Response to the client")
    except BrokenPipeError as e:
        # Handle the broken pipe error gracefully, for example:
        if e.errno != errno.EPIPE:
            raise


def index(request):
    data = Student.objects.all()
    context = {"data": data}
    return render(request, "index.html", context)

def insertData(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        student = Student(name=name, email=email, age=age, gender=gender)
        student.save()
    return redirect('index')


def updateData(request, id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.age = request.POST.get('age')
        student.gender = request.POST.get('gender')
        student.save()
        return redirect('index')
    context = {"d": student}
    return render(request, "update.html", context)

def deleteData(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('index')

def index(request):
    # Your view logic here
    return render(request, 'index.html')

# def signup(request):
#     # Your signup view logic here
#     return HttpResponse("Signup page")
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # return render(request, 'index.html')
        # return redirect('index')
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after signup
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def updateData(request, id):
    # Your view logic here
    return HttpResponse(f'Update Data with ID {id}')

# def login(request):
#     # Your login view logic here
#     return HttpResponse("Login page")
def login(request):
    # return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Authentication failed, display an error message
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')
# def dashboard(request):
#     # Your dashboard view logic here
#     return HttpResponse("Dashboard page")


# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')
def fetch_and_store_users():
    app_id = 'YOUR_APP_ID'
    api_url = f'https://dummyapi.io/data/v1/user'
    headers = {'app-id': app_id}

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json().get('data', [])
        for user_info in user_data:
            student = Student(
                name=user_info.get('firstName', '') + ' ' + user_info.get('lastName', ''),
                email=user_info.get('email', ''),
                age=user_info.get('age', 0),
                gender=user_info.get('gender', '')
            )
            student.save()



def scrape_books():
    base_url = 'http://books.toscrape.com/catalogue/page-{}'
    
    for page_num in range(1, 51):
        page_url = base_url.format(page_num)
        response = requests.get(page_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                title = book.h3.a.get('title')
                price = book.select('div p.price_color')[0].get_text()
                availability = book.select('div p.availability')[0].get_text().strip()
                rating = book.select('p.star-rating')[0].get('class')[1]
                
                book = Book(
                    title=title,
                    price=price,
                    availability=availability,
                    rating=rating
                )
                book.save()

def download_file(request, assignment_id):
    try:
        file = get_object_or_404(File, assignment_id=assignment_id)
        file_path = file.file_url.path

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file_content:
                response = HttpResponse(file_content.read())
                response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'
                return response
        else:
            return JsonResponse({"message": "File not found"}, status=404)
    except File.DoesNotExist:
        return JsonResponse({"message": "File not found"}, status=404)