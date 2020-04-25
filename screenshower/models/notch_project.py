from django.db import models


class NotchProject(models.Model):
    """
    Define model of paroi
    """
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    pos_piece = models.ForeignKey('PositionsPieces', on_delete=models.CASCADE)
    pos_rel = models.FloatField(default=200)
    pos_ref = models.IntegerField(default=0)

    def __str__(self):
        return self.name
