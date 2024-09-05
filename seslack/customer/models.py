# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Manager'


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(Manager, to_field="name", on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Customer'


class Packages(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=10)  # 'Android' or 'iOS'
    license_expire_date = models.DateField(blank=True, null=True)
    customer = models.ForeignKey(Customer, to_field="name", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Packages'
        unique_together = ['name', 'platform']


class AndroidApplyOptions(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
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
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'AndroidApplyOptions'


class iOSApplyOptions(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
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
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'iOSApplyOptions'


class AndroidInspectResult(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    device_info = models.CharField(max_length=30, blank=True, null=True)
    rooting_test = models.BooleanField(default=False)
    rooting = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    emulator = models.BooleanField(default=False)
    obfuscate = models.BooleanField(default=False)
    decompile = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'AndroidInspectResult'


class iOSInspectResult(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    device_info = models.CharField(max_length=30, blank=True, null=True)
    jailbreak_test = models.BooleanField(default=False)
    jailbreak = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    string_encrypt = models.BooleanField(default=False)
    symbol_del = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'iOSInspectResult'


class InspectionRecord(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    inspection_date = models.DateField()
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'InspectionRecord'


class InspectionSchedule(models.Model):
    name = models.ForeignKey(Customer, to_field="name", on_delete=models.CASCADE)
    January = models.BooleanField(default=False)
    February = models.BooleanField(default=False)
    March = models.BooleanField(default=False)
    April = models.BooleanField(default=False)
    May = models.BooleanField(default=False)
    June = models.BooleanField(default=False)
    July = models.BooleanField(default=False)
    August = models.BooleanField(default=False)
    September = models.BooleanField(default=False)
    October = models.BooleanField(default=False)
    November = models.BooleanField(default=False)
    December = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'InspectionSchedule'
