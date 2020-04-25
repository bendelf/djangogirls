from django.db import models


class Paroi(models.Model):
    """
    Define model of paroi
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(default='Paroi', max_length=20)
    h_finie = models.FloatField(default=2000)
    l_finie = models.FloatField(default=1000)

    def __str__(self):
        return self.name
