from django.db import models
import re
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) < 2:
            errors['first_name'] = "First Name must be at least two characters long"
        if len(reqPOST['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least two characters long"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not EMAIL_REGEX.match(reqPOST['email']):
            errors['email'] = "Must be a valid email"
        current_users = User.objects.filter(email = reqPOST['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if reqPOST['password'] != reqPOST['confirm_password']:
            errors['mismatch'] = "Your password do not match"
        return errors
    
    def login_validator(self, reqPOST):
        errors = {}
        existing_user = User.objects.filter(email=reqPOST['email'])
        if len(existing_user) != 1:
            errors['email'] = "User does not exist."
        if len(reqPOST['email']) == 0:
            errors['email'] = "Email must be entered"
        if len(reqPOST['password']) < 8:
            errors['password'] = "An eight character password must be entered"
        elif bcrypt.checkpw(reqPOST['password'].encode(),existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password must match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['title']) < 1:
            errors['title'] = "Title must not be blank"
        if len(reqPOST['description']) < 5:
            errors['description'] = "Description must at least 5 characters long"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="has_created_books", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_books")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = BookManager()