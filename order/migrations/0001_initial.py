# Generated by Django 4.1.7 on 2023-04-04 16:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False,
                 primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('created', 'created'), ('pending', 'pending'), (
                    'accepted', 'accepted'), ('cancelled', 'cancelled'), ('paid', 'paid')], default='created', max_length=100)),
                ('payment_type', models.CharField(choices=[('payme', 'Payme'), ('click', 'CLICK'), (
                    'cash', 'Naqd pul'), ('terminal', 'Terminal')], max_length=50)),
                ('user', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='telegram.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False,
                 primary_key=True, serialize=False, unique=True)),
                ('amount', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='order_items', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='order_items', to='product.product')),
            ],
        ),
    ]
