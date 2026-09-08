from django.db import models

class LogVarredura(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    detalhes = models.TextField()

    def __str__(self):
        return f"Varredura em {self.data_hora}"