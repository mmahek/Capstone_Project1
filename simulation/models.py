from django.db import models

class SimulationRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField()
    results = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Simulation {self.id}"
