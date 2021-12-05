from django.db import models
from django.conf import settings

class NewTree(models.Model) :
      name = models.CharField(max_length=200)
      address = models.TextField()
      telephone = models.CharField(max_length = 15)
      gender = models.CharField(max_length = 15)
      job = models.CharField(max_length = 15)
      parent_id = models.CharField(max_length = 15)
      def __str__(self) :
          return self.name
