from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model): 
    """A topic that the user wants to rank."""
    text = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Entry(models.Model):
    """Ranked list per topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    text = models.CharField(blank=True, null=True, max_length=150)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the entry."""
        return f"Rank {self.rank}: {self.text[:50] if self.text else 'Empty'}"
    #To exit shell, CTRL-D