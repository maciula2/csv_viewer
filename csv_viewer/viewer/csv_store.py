from django.db import models
import jsonfield

class UploadedCSV(models.Model):
    name = models.CharField(max_length=255)
    data = jsonfield.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
