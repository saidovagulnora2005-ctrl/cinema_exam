from django.db import models
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class MovieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    poster = models.ImageField(upload_to='movies/')
    trailer = models.FileField(upload_to='trailers/',blank=True)    
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE,related_name='movies')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)

    objects = MovieManager()
    all_objects = models.Manager()

    class Meta:
        permissions = [
            ("restore_movie","Can restore movie!"),
        ]

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def str(self):
        return self.title


class Hall(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall,on_delete=models.CASCADE,related_name='seats')
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hall', 'row', 'number')

    def str(self):
        return f'Ряд {self.row}, место {self.number} - {self.hall}'


class Session(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='sessions')
    hall = models.ForeignKey(Hall,on_delete=models.CASCADE,related_name='sessions')
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def str(self):
        return f'{self.movie} - {self.start_time}'


class Booking(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE,related_name='bookings')
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE,related_name='bookings')
    email = models.EmailField()
    confirmation_code = models.CharField(max_length=8,unique=True,blank=True)
    status = models.CharField(max_length=20,
        choices=[('reserved', 'Ожидает оплаты'),('paid', 'Оплачено'),('cancelled', 'Отменено'),], default='reserved')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'seat')

    def str(self):
        return f'{self.email} - {self.confirmation_code}'