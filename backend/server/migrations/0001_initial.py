# Generated by Django 4.2.3 on 2023-08-06 12:14

from django.db import migrations, models
import pgvector.django


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'answers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'conversations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExcludeFromCache',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('embedding', pgvector.django.VectorField(blank=True, dimensions=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'exclude_from_cache',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'messages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('embedding', pgvector.django.VectorField(blank=True, dimensions=512, null=True)),
                ('difficulty', models.FloatField()),
                ('created_by', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'questions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'ratings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'topics',
                'managed': False,
            },
        ),
    ]
