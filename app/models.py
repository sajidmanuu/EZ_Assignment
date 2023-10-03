from django.db import models
from django.contrib.auth.models import User
class Student(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=25, blank=False, null=False)

    def __str__(self):
        return self.name



class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
