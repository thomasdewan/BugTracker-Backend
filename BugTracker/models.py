from django.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
    owner = models.ForeignKey(User, related_name='issue', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    creationDate = models.DateField(auto_now_add=True, blank=False)
    state = models.ForeignKey('State')

    def __str__(self):
        return self.name+" by "+ self.owner.username

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
