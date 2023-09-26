from django.db import models
from django.utils.translation import gettext_lazy as _

class AlarmCode(models.TextChoices):
    ACCOFF = "ACCOFF", "Parada"
    ACCON = "ACCON", "Inicio"
    OFFLINETIMEOUT = "OFFLINETIMEOUT", "Tiempo de espera sin conexión"
    STAYTIMEOUT = "STAYTIMEOUT", "Tiempo de espera de estancia"
    REMOVE = "REMOVE", "Desmontaje, sensor de luz, fallo de alimentación, enchufar y desenchufar"
    LOWVOT = "LOWVOT", "Baja electricidad"
    ERYA = "ERYA", "Segunda carga"
    FENCEIN = "FENCEIN", "Entrar en la cerca"
    FENCEOUT = "FENCEOUT", "Fuera de la cerca"
    SEP = "SEP", "Separado"
    SOS = "SOS", "Alarma SOS"
    OVERSPEED = "OVERSPEED", "Alarma de exceso de velocidad"
    HOME = "HOME", "Residencia permanente anormal (casa)"
    COMPANY = "COMPANY", "Residencia permanente anormal (empresa)"
    CRASH = "CRASH", "Alarma de colisión"
    SHAKE = "SHAKE", "Vibración"
    ACCELERATION = "ACCELERATION", "Aceleración rápida"
    DECELERATION = "DECELERATION", "Desaceleración rápida"
    TURN = "TURN", "Giro brusco"
    FASTACCELERATION = "FASTACCELERATION", "Aceleración máxima"
    SHARPTURN = "SHARPTURN", "Giro brusco"
    TURNOVER = "TURNOVER", "Volcar"
    FASTDECELERATION = "FASTDECELERATION", "Desaceleración rápida"

class DeviceBase(models.Model):
    code = models.IntegerField()
    imei = models.CharField(max_length=20)
    lat = models.CharField(max_length=20, blank=True, null=True)
    lng = models.CharField(max_length=20, blank=True, null=True)
    time = models.IntegerField()
    position_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    speed = models.IntegerField(blank=True, null=True)
    course = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

class Detail(DeviceBase):
    alarm_code = models.CharField(
        max_length=20,
        choices=AlarmCode.choices,
        default=AlarmCode.ACCOFF,
    )
    alarm_time = models.IntegerField()
    device_type = models.IntegerField()
    alarm_type = models.IntegerField()

    class Meta:
        verbose_name = _("Alarma")
        verbose_name_plural = _("Alarmas")

    def __str__(self):
        return f"{self.alarm_code} - {self.imei}"

class User(models.Model):
    account_id = models.IntegerField()
    account_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    imei = models.CharField(max_length=20, unique=True)
    license_number = models.CharField(max_length=255, blank=True, null=True)
    vin = models.CharField(max_length=255, blank=True, null=True)
    car_owner = models.CharField(max_length=255, blank=True, null=True)
    is_tracking = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Usuario del dispositivo")
        verbose_name_plural = _("Usuarios de los dispositivos")

    def __str__(self):
        return str(self.user_name)
