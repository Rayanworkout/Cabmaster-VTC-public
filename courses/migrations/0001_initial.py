# Generated by Django 4.2.7 on 2023-12-04 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_address', models.CharField(max_length=200, verbose_name='Départ')),
                ('destination', models.CharField(max_length=200, verbose_name='Destination')),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name='Durée')),
                ('course_price', models.IntegerField(null=True, verbose_name='Prix')),
                ('worker_commission', models.FloatField(blank=True, default=0, null=True, verbose_name='Commission Partenaire')),
                ('cabmaster_commission', models.FloatField(blank=True, default=0, null=True, verbose_name='Commission Cabmaster')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Création')),
                ('happening_datetime', models.DateTimeField(verbose_name='Date')),
                ('status', models.CharField(choices=[('pending', 'En Attente'), ('done', 'Validée'), ('cancelled', 'Annulée')], default='pending', max_length=50, verbose_name='Statut')),
                ('course_type', models.CharField(choices=[('classic', 'Trajet'), ('disposition', 'Mise à Disposition')], default='classic', max_length=50, verbose_name='Type')),
                ('course_grade', models.CharField(choices=[('', 'Catégorie'), ('standard', 'Éco Confort'), ('berline', 'Premium'), ('van', 'Van')], default='standard', max_length=50, verbose_name='Grade')),
                ('payment_mode', models.CharField(choices=[('', 'Mode de Paiement'), ('cash', 'Espèces'), ('card', 'Carte Bancaire'), ('online', 'En Ligne')], default='cash', max_length=10, verbose_name='Paiement')),
                ('passengers', models.IntegerField(default=1, verbose_name='Passagers')),
                ('small_cases', models.IntegerField(default=0, verbose_name='Petites Valises')),
                ('big_cases', models.IntegerField(default=0, verbose_name='Grandes Valises')),
                ('comments', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Commentaires')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='customers.customer')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
    ]