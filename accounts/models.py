from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class MyProfile(models.Model):
    type = (('customer','customer'),('seller','seller'))
    ge = (('male','Male'),('female','Female'))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100,choices=ge)
    phone = models.CharField(max_length=100)
    register_type = models.CharField(max_length=100,choices=type)
    profile_pic = models.ImageField(default='facebook.jpg', upload_to='profile_pic/', null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            MyProfile.objects.create(user=instance)
            print('profile created')

@receiver(post_save,sender=User)
def save_user_profile(instance,created,**kwargs):
    if instance.is_superuser:
        pass
    else:
        print('profile aganin and again')
        instance.myprofile.save()





