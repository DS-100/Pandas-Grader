# Generated by Django 2.2.2 on 2019-06-25 22:07

import app.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("app", "0004_delete_config")]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="last_updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="gradingjob",
            name="status",
            field=models.CharField(
                choices=[
                    (app.models.JobStatusEnum("QUEUED"), "QUEUED"),
                    (app.models.JobStatusEnum("DONE"), "DONE"),
                    (app.models.JobStatusEnum("RUNNING"), "RUNNING"),
                    (app.models.JobStatusEnum("FINISHED"), "FINISHED"),
                ],
                default=app.models.JobStatusEnum("QUEUED"),
                max_length=10,
            ),
        ),
    ]
