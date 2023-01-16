# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Base(models.Model):
    base = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'base'

class Build(models.Model):
    car_name = models.OneToOneField('Car', models.DO_NOTHING, db_column='car_name', primary_key=True)
    industry = models.ForeignKey('Industry', models.DO_NOTHING, db_column='industry')
    amount = models.IntegerField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        managed = True
        db_table = 'build'
        unique_together = (('car_name', 'industry', 'date'),)


class Buy(models.Model):
    car_name = models.OneToOneField('Car', models.DO_NOTHING, db_column='car_name', primary_key=True)
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customer')
    industry = models.ForeignKey('Industry', models.DO_NOTHING, db_column='industry')
    amount = models.IntegerField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        managed = True
        db_table = 'buy'
        unique_together = (('car_name', 'customer', 'industry', 'date'),)


class Car(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    price = models.IntegerField(blank=True, null=True)
    brand = models.CharField(max_length=5, blank=True, null=True)
    size = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'car'


class Customer(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=5)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer'


class Industry(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=5)  # Field name made lowercase.
    profit = models.IntegerField(blank=True, null=True)
    car_in = models.IntegerField(blank=True, null=True)
    car_remain = models.IntegerField(blank=True, null=True)
    car_out = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'industry'


class Sizes(models.Model):
    name = models.CharField(max_length=5, blank=True, null=False,primary_key=True)
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    wheel_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sizes'
