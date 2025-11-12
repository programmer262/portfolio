from django.db import models

# Create your models here.
class Contact(models.Model):
    Full_name = models.CharField(max_length=200)
    Email = models.EmailField(verbose_name="The Email",blank=True, null=True)
    Phone = models.CharField(max_length=16,blank=True, null=True)
    Message = models.TextField()
    def __str__(self):
        return (self.Full_name +"\t"+ self.Email )
