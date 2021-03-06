# Generated by Django 2.2.3 on 2019-07-02 16:57

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("app", "0005_auto_20190625_2207")]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="file",
            field=models.FileField(
                help_text="Please upload a zip file!",
                upload_to=app.models.get_file_path,
            ),
        )
    ]
