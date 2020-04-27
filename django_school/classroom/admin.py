from django.contrib import admin
from .models import Profile, Subject,  Student, Equipe, Quiz,  ExpertListe



# Register your models here.

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Equipe)
admin.site.register(Quiz)
admin.site.register(ExpertListe)