from email.policy import default
from django.db import models

# Create your models here.

# https://docs.djangoproject.com/en/4.1/ref/models/fields/#choices


class userDetails(models.Model):

    userId = models.CharField(max_length=38, primary_key=True)
    userName = models.CharField(max_length=38)


class expenseDetails(models.Model):

    expenseCategory = models.CharField(max_length=38, default=True)
    date = models.DateTimeField(default=0)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    comments = models.TextField(max_length=38, default=None)
    availablechoices = [
        ("PENDING", 'Pending'),
        ("ACCEPTED", 'Accepted'),
        ("REJECTED", 'Rejecteed')

    ]
    recieptImage = models.ImageField(
        max_length=None, default=1, blank=True
    )
    approvedStatus = models.TextField(
        default="Pending", blank=True, choices=availablechoices)

    userDetail = models.ForeignKey(
        userDetails, on_delete=models.CASCADE, default=101)

    approversComments = models.TextField(
        max_length=38, blank=True, default="Pending")
