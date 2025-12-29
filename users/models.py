from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CEO', 'CEO'),
        ('Director', 'Director'),
        ('Delta', 'Delta'),
        ('Code', 'Code'),
        ('Member', 'Member'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Rejected', 'Rejected'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    instagram_username = models.CharField(max_length=50, blank=True)
    instagram_url = models.URLField(blank=True)
    custom_password = models.CharField(max_length=50, blank=True)

    main_group = models.ForeignKey(
        'groups.MainGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    sub_group = models.ForeignKey(
        'groups.SubGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
