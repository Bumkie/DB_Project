from django.db import models

class Theater(models.Model):
    theater_id = models.CharField(max_length=10, primary_key=True)
    theater_name = models.CharField(max_length=50)
    theater_genre = models.CharField(max_length=20)
    playtime = models.CharField(max_length=20)
    price = models.IntegerField()
    class Meta:
        app_label = 'booking'
    def __str__(self):
        return self.theater_name

class Screening(models.Model):
    screening_id = models.CharField(max_length=10, primary_key=True)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)

class Seat(models.Model):
    seat_id = models.IntegerField(primary_key=True)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    status = models.BooleanField()

class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    phone_number = models.CharField(max_length=20)
