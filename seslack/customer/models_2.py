from django.db import models

class Manager(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Manager'

class Customer(models.Model):
    name = models.CharField(max_length=100)
    manger_name = models.ForeignKey(Manager, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Customer'

class Packages(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=10)  # 'Android' or 'iOS'
    license_expire_date = models.DateField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'iOSInspectResult'

class InspectionRecord(models.Model):
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    inspection_date = models.DateTimeField()
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'InspectionRecord'
