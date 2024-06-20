from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

# Create your models here.

class Korisnici(AbstractUser):
    ROLES = (("profesor", "profesor"),("administrator", "administrator"),("student", "student"))
    STATUS = (("redovan","redovan"),("izvanredan", "izvanredan"),("none", "none"))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='korisnici_set' 
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='korisnici_set' 
    )

    @classmethod
    def get_students(cls):
        return cls.objects.filter(role="student")    
    @classmethod
    def get_professors(cls):
        return cls.objects.filter(role="profesor")    


class Predmeti(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=10)
    program = models.TextField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=10, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnici, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.name


class StudentEnrollment(models.Model):  
    STATUS_UPISA = (('Passed', 'Passed'),('Enrolled', 'Enrolled'),('Failed', 'Failed'))
    student = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    subject = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=STATUS_UPISA)