from django.db import models




class Register(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.email
    
class issues_register(models.Model):
    name = models.CharField(max_length=20, null=True)
    comments = models.CharField(max_length=2500, null=True)
    date = models.DateField(auto_now_add=True)
    issues_image = models.ImageField(upload_to="uploads/", null=True)
    gender = models.TextField(max_length=200,null=True)
    issues = models.TextField(max_length=500,null=True)

    def __str__(self):
        return self.name
