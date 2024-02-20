from django.db import models

# Create your models here.

class SoilData(models.Model):
    grid_section = models.CharField(max_length=10)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    moisture_level = models.FloatField()

    def __str__(self):
        return self.grid_section