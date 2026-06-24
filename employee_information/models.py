from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employees(models.Model):
    # Personnel Information
    code = models.CharField(max_length=100, blank=True)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField()

    contact = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()

    department_id = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    position_id = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    date_hired = models.DateField()
    salary = models.FloatField(default=0)

    # ==========================
    # TRAINING INFORMATION
    # ==========================

    safety_training_hours = models.FloatField(default=0)
    technical_training_hours = models.FloatField(default=0)
    pra_training_hours = models.FloatField(default=0)
    ojt_training_hours = models.FloatField(default=0)

    total_hour = models.FloatField(default=0)

    # Safety Training
    safety_training_start_date = models.DateField(
        blank=True,
        null=True
    )
    safety_training_end_date = models.DateField(
        blank=True,
        null=True
    )

    # Technical Training
    technical_training_start_date = models.DateField(
        blank=True,
        null=True
    )
    technical_training_end_date = models.DateField(
        blank=True,
        null=True
    )

    # PRA Training
    pra_training_start_date = models.DateField(
        blank=True,
        null=True
    )
    pra_training_end_date = models.DateField(
        blank=True,
        null=True
    )

    # OJT Training
    ojt_training_start_date = models.DateField(
        blank=True,
        null=True
    )
    ojt_training_end_date = models.DateField(
        blank=True,
        null=True
    )

    total_completion_hour = models.FloatField(default=0)

    training_need_to_completed = models.FloatField(default=0)

    # Status
    status = models.IntegerField(default=1)

    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto Calculate Total Hour
        self.total_hour = (
            self.safety_training_hours +
            self.technical_training_hours +
            self.pra_training_hours +
            self.ojt_training_hours
        )

        super().save(*args, **kwargs)

    @property
    def fullname(self):
        return f"{self.firstname} {self.middlename or ''} {self.lastname}"

    def __str__(self):
        return self.fullname.strip()