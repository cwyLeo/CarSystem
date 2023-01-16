from django.db import models
class Base(models.Model):
    name = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'base'
class Build(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    amount = models.IntegerField(blank=True, null=True)
    id = models.ForeignKey('Industry', models.DO_NOTHING, db_column='ID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'build'
names = [i for i in dir(Build) if i not in dir(Base)]
print(names)
# print(names[0],a.__dict__[names[0]])