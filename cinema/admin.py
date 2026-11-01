from django.contrib import admin
from .models import Hall, Seat,Movie,Genre


admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(Movie)
admin.site.register(Genre)