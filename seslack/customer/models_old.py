# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AndroidOptions(models.Model):
    package_name = models.OneToOneField('Packages', models.DO_NOTHING, db_column='package_name', primary_key=True)
    update_date = models.DateTimeField(blank=True, null=True)
    check_root = models.BooleanField(default=False)
    detect_magisk = models.BooleanField(default=False)
    check_integrity = models.BooleanField(default=False)
    check_emul = models.BooleanField(default=False)
    check_debugging = models.BooleanField(default=False)
    prevent_debugging = models.BooleanField(default=False)
    prevent_adb = models.BooleanField(default=False)
    encrypt_so = models.BooleanField(default=False)
    self_protect = models.BooleanField(default=False)
    prevent_decompile = models.BooleanField(default=False)
    chekc_mem_scanner = models.BooleanField(default=False)
    encrypt_flutter = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'Android_options'


class Inspectiondocuments(models.Model):
    customer_name = models.ForeignKey('Customerlist', models.DO_NOTHING, db_column='customer_name')
    upload_date = models.DateTimeField(db_column='upload_Date')  # Field name made lowercase.
    file_path = models.CharField(max_length=30)
    # The composite primary key (index_num, CustomerList_customer_name, CustomerList_maange_name) found, that is not supported. The first column is selected.
    index_num = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'InspectionDocuments'


class Managerlist(models.Model):
    user_id = models.CharField(max_length=30,)
    manager_name = models.CharField(max_length=30, primary_key=True)
    append_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ManagerList'


class CustomerList(models.Model):
    customer_name = models.CharField(max_length=30, primary_key=True)
    manager_name = models.CharField(max_length=30,)
    append_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'CustomerList'


class Monthly(models.Model):
    customer_name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        managed = True
        db_table = 'Monthly'


class Packages(models.Model):
    customer_name = models.ForeignKey('CustomerList', models.DO_NOTHING, db_column='customer_name')  # Field name made lowercase.
    package_name = models.OneToOneField('AndroidInspectResult', models.DO_NOTHING, db_column='package_name', primary_key=True)
    license_expire_date = models.DateField(blank=True, null=True)
    append_date = models.DateField(blank=True, null=True)
    os_type = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Packages'


class AndroidInspectResult(models.Model):
    package_name = models.CharField(max_length=30, primary_key=True)
    inspection_date = models.DateField(blank=True, null=True)
    device_info = models.CharField(max_length=30, blank=True, null=True)
    rooting_test = models.BooleanField(default=False)
    rooting = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    emulator = models.BooleanField(default=False)
    obfuscate = models.BooleanField(default=False)
    decompile = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'android_inspect_result'


class IosInspectResult(models.Model):
    package_name = models.OneToOneField(Packages, models.DO_NOTHING, db_column='package_name', primary_key=True)
    inspection_date = models.DateField(blank=True, null=True)
    device_info = models.CharField(max_length=30, blank=True, null=True)
    jailbreak_test = models.BooleanField(default=False)
    jailbreak = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    string_encrypt = models.BooleanField(default=False)
    symbol_del = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'iOS_inspect_result'


class IosOptions(models.Model):
    package_name = models.OneToOneField(Packages, models.DO_NOTHING, db_column='package_name', primary_key=True)
    update_date = models.DateTimeField(blank=True, null=True)
    objc_string_encryption = models.BooleanField(default=False)
    swift_string_encryption = models.BooleanField(default=False)
    jailbreak_check = models.BooleanField(default=False)
    threat_check = models.BooleanField(default=False)
    integrity_check = models.BooleanField(default=False)
    flex_3_check = models.BooleanField(default=False)
    server_auth_manually = models.BooleanField(default=False)
    objc_obfuscate = models.BooleanField(default=False)
    swift_obfuscate = models.BooleanField(default=False)
    symbol_delete = models.BooleanField(default=False)
    log_hiding = models.BooleanField(default=False)
    dynamic_api_hiding = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'iOS_options'
