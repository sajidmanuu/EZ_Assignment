from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('insert', views.insertData, name="insertData"),
    path('update/<int:id>', views.updateData, name="updateData"),
    path('delete/<int:id>', views.deleteData, name="deleteData"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('fetch/', views.fetch_and_store_users, name="fetch"),
    path('scrap/', views.scrape_books, name="scrap"),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('download-file/<str:assignment_id>/', views.download_file, name='download_file'),

]



# from django.urls import path
# from app import views


# urlpatterns = [
#     path('', views.index, name="index"),
#     path('insert', views.insertData, name="insertData"),
#     path('update/<int:id>', views.updateData, name="updateData"),
#     path('delete/<int:id>', views.deleteData, name="deleteData"),
#     path('signup/', views.signup, name="signup"),
#     path('login/', views.login, name="login"),
#     # path('dashboard/', views.dashboard, name="dashboard"),
# ]
