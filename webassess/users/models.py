from django.contrib.auth.models import models, User

class School(models.Model):
    short_name = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.short_name

class Student(models.Model):
    user = models.OneToOneField(User)
    school = models.ForeignKey(School, blank=True)
    def get_full_name(self):
        if self.mi != '':
            return self.user.last_name + ", " + self.user.first_name + " " + self.mi + "."
        else:
            return self.user.last_name + ", " + self.user.first_name
    
    def get_short_name(self):
        return self.user.username
        
    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User)
    school = models.OneToOneField(School)
    def get_full_name(self):
        if self.mi != '':
            return self.user.last_name + ", " + self.user.first_name + " " + self.mi + "."
        else:
            return self.user.last_name + ", " + self.user.first_name
    
    def get_short_name(self):
        return self.user.username
        
    def __str__(self):
        return self.user.username
