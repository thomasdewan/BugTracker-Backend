from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Issue(models.Model):
    owner = models.ForeignKey(User, related_name='issue', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    creationDate = models.DateTimeField(auto_now_add=True, blank=False)
    state = models.ForeignKey('State')

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE)
    creationDate = models.DateField(auto_now_add=True, blank=False)
    
    def __str__(self):
        return self.owner.username +" about "+self.issue.name
