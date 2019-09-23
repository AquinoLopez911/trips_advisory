from django.db import models
import re
import bcrypt
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        user_with_email = User.objects.filter(email = post_data['email'])

        if len(post_data['name']) < 2:
            errors['name'] = "name nust be atleast 2 characters"
        if len(post_data['username']) < 2:
            errors['username'] = "alias nust be atleast 2 characters"
        if len(post_data['email']) < 1:
            errors['email_blank'] = "email is required"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email_pattern'] = "valid email required"
        if len(user_with_email) > 0:
            errors['emails_taken'] = "email is being used by another user"
        if len(post_data['password']) < 2:
            errors['password_length'] = "password must be atleast 8 characters"
        if post_data['password'] != post_data['confirm'] :
            errors['password_match'] = "passwords dont match"
        print(errors)
        return errors

    def login_validator(self, post_data):
        errors = {}
        #get a list of all users with the email entered (shoukld only be one)
        users_with_email = User.objects.filter(email = post_data['email'].lower())
        #storing the user with the specific email in user variable 

        if len(post_data['email']) < 1:
            errors['empty_email'] = "email is being used by another user"

        if len(post_data['password']) < 1:
            errors['password_length'] = "password must be atleast 8 characters"

        if len(users_with_email) < 1:
            errors['no_matching_email'] = "no user with that email"
        else:
            user = users_with_email[0]
            if bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['password_incorrect'] = 'incorrect password'

        return errors





class TripManager(models.Manager):
    def trip_registration(self, post_data):
        errors = {}
        start = post_data['start_date']
        end = post_data['end_date']
        today = str(date.today())

        print(str(today))
        print(start)

        if len(post_data['destination']) < 2:
            errors['destination'] = "destination must be atleast 2 characters ex 'VA'"
        if start:
            if start < today:
                errors['invalid start'] = "start date must come today or later"
            if start > end:
                errors['invalid dates'] = "start date must come before end date"
            if not end:
                errors['infinit_vacay'] = "trip must come to an end"
        else:
            errors['no_start'] = "trip must have a start date"
        if not end:
            errors['no_end'] = "trip must have a end date"      
        if len(post_data['plan']) < 10 :
            errors['short_plan'] = "plan must be atleast 10 characters"
        print(errors)
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __repr__(self):
        return f"User object: {self.id}, name: {self.name}, email: {self.email}, password: {self.password}"


class Trip(models.Model):
    destination =  models.CharField(max_length=255)
    start_date = created_at = models.DateTimeField()
    end_date = created_at = models.DateTimeField()
    plan = models.TextField()
    planner = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    buddies = models.ManyToManyField(User, related_name="trip")
    objects = TripManager()

    def __repr__(self):
        return f"Trip object: {self.id}, Destination: {self.destination}, start: {self.start_date}, end: {self.end_date}, plan: {self.plan}"