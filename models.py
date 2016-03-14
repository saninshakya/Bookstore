# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class CategoryList(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    category = models.TextField()
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'category_list'


class ChallengeOthers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    item = models.ForeignKey('ItemList')
    challengedby = models.ForeignKey(AuthUser, db_column='challengedBy_id')  # Field name made lowercase.
    challengedto = models.ForeignKey(AuthUser, db_column='challengedTo_id')  # Field name made lowercase.
    acceptchallenge = models.BooleanField(db_column='acceptChallenge')  # Field name made lowercase.
    challengecompleted = models.BooleanField(db_column='challengeCompleted')  # Field name made lowercase.
    challengeddate = models.DateField(db_column='challengedDate')  # Field name made lowercase.
    challengecompleteddate = models.DateField(db_column='challengeCompletedDate', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateField(db_column='dueDate', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(max_length=500, blank=True)
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'challenge_others'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ItemAbstract(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    file = models.CharField(max_length=100, blank=True)
    uploadeddate = models.DateTimeField(db_column='uploadedDate')  # Field name made lowercase.
    modified = models.DateTimeField()
    deleted = models.BooleanField()
    item = models.ForeignKey('ItemList')

    class Meta:
        managed = False
        db_table = 'item_abstract'


class ItemBulkInsertion(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    file = models.CharField(max_length=100)
    uploadeddate = models.DateTimeField(db_column='uploadedDate')  # Field name made lowercase.
    uploadedby = models.ForeignKey(AuthUser, db_column='uploadedBy_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'item_bulk_insertion'


class ItemCoverImage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    file = models.CharField(max_length=100)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    deleted = models.BooleanField()
    item = models.ForeignKey('ItemList')

    class Meta:
        managed = False
        db_table = 'item_cover_image'


class ItemList(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=250)
    publisher = models.CharField(max_length=500)
    publicationdate = models.CharField(db_column='publicationDate', max_length=50)  # Field name made lowercase.
    isbn = models.CharField(max_length=200)
    editionlanguage = models.CharField(db_column='editionLanguage', max_length=50)  # Field name made lowercase.
    awards = models.CharField(max_length=500)
    summary = models.TextField()
    coverimageurl = models.CharField(db_column='coverImageUrl', max_length=500)  # Field name made lowercase.
    url = models.CharField(max_length=500)
    category = models.ForeignKey(CategoryList)
    createdby = models.ForeignKey(AuthUser, db_column='createdBy_id')  # Field name made lowercase.
    created = models.DateTimeField()
    modified = models.DateTimeField()
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'item_list'


class ItemTableOfContent(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    file = models.CharField(max_length=100, blank=True)
    uploadeddate = models.DateTimeField(db_column='uploadedDate')  # Field name made lowercase.
    modified = models.DateTimeField()
    deleted = models.BooleanField()
    item = models.ForeignKey(ItemList)

    class Meta:
        managed = False
        db_table = 'item_table_of_content'


class ReviewItem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    review = models.CharField(max_length=1000)
    item = models.ForeignKey(ItemList)
    createdby = models.ForeignKey(AuthUser, db_column='createdBy_id')  # Field name made lowercase.
    created = models.DateTimeField()
    modified = models.DateTimeField()
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'review_item'


class WishList(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    item = models.ForeignKey(ItemList)
    status = models.CharField(max_length=50, blank=True)
    dateadded = models.DateTimeField(db_column='dateAdded')  # Field name made lowercase.
    readdate = models.DateField(db_column='readDate', blank=True, null=True)  # Field name made lowercase.
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'wish_list'
