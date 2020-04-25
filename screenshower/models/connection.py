from django.db import models


class PositionsPieces(models.Model):
    """
    Define model of positions
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    connection = models.ForeignKey('Connection', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Connection(models.Model):
    """
    Define model of connection type
    """
    cd = models.IntegerField(default=1)
    designation = models.CharField(max_length=30)
