# Generated by Django 2.2.2 on 2019-08-13 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("app", "0006_auto_20190702_1657")]

    operations = [
        migrations.AddField(
            model_name="gradingjob", name="log_html", field=models.TextField(null=True)
        )
    ]
