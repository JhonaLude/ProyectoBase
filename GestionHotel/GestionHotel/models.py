from django.db import models

# Tabla Categoria
class Categoria(models.Model):
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Categoria'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return self.descripcion or f"Categoria {self.id}"

# Tabla Hotel (relación uno a uno con Categoria)
class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    anio_construccion = models.PositiveIntegerField(blank=True, null=True)
    categoria = models.OneToOneField(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Hotel'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return self.nombre

# Tabla Habitacion
class Habitacion(models.Model):
    TIPO_CHOICES = (
        ('suite', 'Suite'),
        ('doble', 'Doble'),
        ('individuales', 'Individuales'),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='habitaciones')
    numero_habitacion = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        db_table = 'Habitacion'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return f'Habitacion {self.numero_habitacion} - {self.hotel.nombre}'

# Tabla Servicios
class Servicio(models.Model):
    TIPO_CHOICES = (
        ('spa', 'Spa'),
        ('comida', 'Comida'),
        ('transporte', 'Transporte'),
        ('estacionamiento', 'Estacionamiento'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        db_table = 'Servicio'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return self.tipo

# Tabla intermedia Habitacion_Servicio (muchos a muchos con campos adicionales)
class HabitacionServicio(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'Habitacionservicio'  # Asegúrate de que el nombre coincida con la tabla
        unique_together = ('habitacion', 'servicio')

    def __str__(self):
        return f'{self.habitacion} - {self.servicio}'

# Tabla Reservacion
class Reservacion(models.Model):
    nombre_persona = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    habitaciones = models.ManyToManyField(Habitacion, through='HabitacionReservacion')

    class Meta:
        db_table = 'Reservacion'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return f'Reservacion {self.id}'

# Subtipo de Reservacion: Particular
class ReservacionParticular(models.Model):
    reservacion = models.OneToOneField(Reservacion, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'Reservacionparticular'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return f'ReservacionParticular {self.reservacion.id}'

# Subtipo de Reservacion: Agencia
class ReservacionAgencia(models.Model):
    reservacion = models.OneToOneField(Reservacion, on_delete=models.CASCADE, primary_key=True)
    nombre_agencia = models.CharField(max_length=100)

    class Meta:
        db_table = 'Reservacionagencia'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return f'ReservacionAgencia {self.reservacion.id} - {self.nombre_agencia}'

# Relación intermedia entre Habitacion y Reservacion
class HabitacionReservacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Habitacionreservacion'  # Asegúrate de que el nombre coincida con la tabla
        unique_together = ('habitacion', 'reservacion')

    def __str__(self):
        return f'Habitacion {self.habitacion.id} - Reservacion {self.reservacion.id}'

# Tabla Factura
class Factura(models.Model):
    METODO_PAGO_CHOICES = (
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    )
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    fecha_factura = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)

    class Meta:
        db_table = 'Factura'  # Asegúrate de que el nombre coincida con la tabla

    def __str__(self):
        return f'Factura {self.id} - Reservacion {self.reservacion.id}'
