from django.db import models
from .connection import PositionsPieces

class RefPiece(models.Model):
    """
    Define model of ref_pieces
    """
    cd = models.CharField(max_length=20)
    marque = models.ForeignKey('Marque', on_delete=models.CASCADE)
    type = models.ForeignKey('TypePiece', on_delete=models.CASCADE)
    finition_piece = models.ForeignKey('FinitionPiece', on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    longueur_m = models.FloatField(default=0)
    jeu_mm = models.IntegerField(default=0)
    unit = models.CharField(default='ML', max_length=5)

    def __str__(self):
        return self.ref_article


class FinitionPiece(models.Model):
    """
    Define model of finition_pieces
    """
    cd = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class TypePiece(models.Model):
    """
       Define model of type_pieces
       """
    cd = models.CharField(max_length=20)
    designation = models.CharField(max_length=30)
    notch = models.IntegerField(default=0)
    qte_defaut = models.IntegerField(default=0)

    def __str__(self):
        return self.designation


class Marque(models.Model):
    """
    Define model of finition_pieces
    """
    cd = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PieceProject(models.Model):
    """
    Define model of pieces_projet
    TODO : table for connection ?
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    piece = models.ForeignKey('RefPiece', on_delete=models.CASCADE)
    pos_piece = models.ForeignKey('PositionsPieces', on_delete=models.CASCADE)

    def __str__(self):
        return self.connection

