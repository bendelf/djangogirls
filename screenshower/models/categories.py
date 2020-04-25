from django.db import models


class GlassType(models.Model):
    """
    Define model of glass type
    """
    ref_glass = models.CharField(max_length=10, default='8T')
    designation = models.CharField(max_length=50)
    finish = models.CharField(max_length=30)
    thickness = models.IntegerField(default=8)
