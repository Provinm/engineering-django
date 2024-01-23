from django.db import models


class ViewRecord(models.Model):
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "topic_error_example2_view_record"
