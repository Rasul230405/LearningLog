from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """Create models"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    public = models.BooleanField(default=True)

    def __str__(self):
        """Return string represent of the model"""
        return self.text

class Entry(models.Model):
    """Create entires"""
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)        
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """Return string represent of the modesl"""
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text
