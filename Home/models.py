from django.db import models

class SearchQ(models.Model):
    query = models.CharField(max_length=15)
    created_at = models.DateField()
    def __str__(self):
        return self.query
    
# Create your models here.
