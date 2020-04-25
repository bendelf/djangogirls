from django.db import models


class Volume(models.Model):
    """
    Define model of paroi
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    paroi = models.ForeignKey('Paroi', on_delete=models.CASCADE)
    glass = models.ForeignKey('GlassType', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='Volume')
    type = models.IntegerField(default=10)
    l_cste = models.FloatField(default=-9999)
    l_left_angle = models.IntegerField(default=0)
    l_right_angle = models.IntegerField(default=0)
    h_left_angle = models.IntegerField(default=0)
    h_right_angle = models.IntegerField(default=0)
    l_left_slope = models.IntegerField(default=0)
    l_right_slope = models.IntegerField(default=0)
    h_left_slope = models.IntegerField(default=0)
    h_right_slope = models.IntegerField(default=0)

    def __str__(self):
        return self.name
