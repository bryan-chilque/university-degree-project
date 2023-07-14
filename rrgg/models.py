from django.db import models


class SeguroVehicular(models.Model):
    nombre = models.CharField(max_length=64)
    prima_neta = models.PositiveIntegerField()
    derecho_emision = models.PositiveIntegerField()
    igv = models.PositiveIntegerField()

    @property
    def prima_total(self):
        return self.prima_neta + self.derecho_emision + self.igv

    def __str__(self):
        return self.nombre
