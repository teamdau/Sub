# Generated by Django 4.2.6 on 2024-08-27 10:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("transcribe", "0003_alter_inputdata_language"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inputdata",
            name="end_time",
        ),
        migrations.RemoveField(
            model_name="inputdata",
            name="id",
        ),
        migrations.RemoveField(
            model_name="inputdata",
            name="start_time",
        ),
        migrations.RemoveField(
            model_name="inputdata",
            name="youtube_url",
        ),
        migrations.AddField(
            model_name="inputdata",
            name="input_text",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="inputdata",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "Anh"),
                    ("ko", "Hàn Quốc"),
                    ("vi", "Việt Nam"),
                    ("es", "Tây Ban Nha"),
                    ("fr", "Pháp"),
                    ("de", "Đức"),
                    ("ja", "Nhật Bản"),
                    ("zh", "Trung Quốc"),
                    ("ru", "Nga"),
                    ("pt-BR", "Bồ Đào Nha (Brazil)"),
                    ("pt-PT", "Bồ Đào Nha (Bồ Đào Nha)"),
                ],
                default="en",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="inputdata",
            name="uid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]