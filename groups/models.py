from django.db import models
from users.models import User
from django.utils import timezone

class MainGroup(models.Model):
    name = models.CharField(max_length=1, unique=True)  # A-J
    delta = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Delta'}
    )

    def __str__(self):
        return self.name


class SubGroup(models.Model):
    name = models.CharField(max_length=3, unique=True)  # A01
    main_group = models.ForeignKey(MainGroup, on_delete=models.CASCADE)
    code = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Code'}
    )

    def __str__(self):
        return self.name
    



class DailyActivity(models.Model):
    member = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Member'}
    )
    subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('member', 'date')

    def __str__(self):
        return f"{self.member.username} - {self.date}"

class PostBooking(models.Model):
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    main_group = models.ForeignKey(MainGroup, on_delete=models.CASCADE)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'booking_date')  # Prevent double booking

    def __str__(self):
        return f"{self.member.username} - {self.booking_date}"


class WeeklyPost(models.Model):
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    main_group = models.ForeignKey(MainGroup, on_delete=models.CASCADE)
    post_link = models.URLField()
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('member', 'booking_date')  # One post per member per week

    def __str__(self):
        return f"{self.member.username} - {self.booking_date}"

