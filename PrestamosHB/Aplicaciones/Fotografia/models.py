from django.db import models

class Camara(models.Model):
    idcam = models.AutoField(primary_key=True)  # idcam como campo autoincremental
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=[('DSLR', 'DSLR'), ('dron', 'Dron')])
    valor_mercado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.modelo

class Fotografo(models.Model):
    idfot = models.AutoField(primary_key=True)  # idfot como campo autoincremental
    nombre = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=20, choices=[('estudiante', 'Estudiante'), ('profesional', 'Profesional')])

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    idpre = models.AutoField(primary_key=True)  # idpre como campo autoincremental
    camara = models.ForeignKey(Camara, on_delete=models.CASCADE)
    fotografo = models.ForeignKey(Fotografo, on_delete=models.CASCADE)
    fecha_salida = models.DateField()
    seguro_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Préstamo de {self.camara.modelo} a {self.fotografo.nombre}"

class Accesorio(models.Model):
    idacc = models.AutoField(primary_key=True)  # idacc como campo autoincremental
    nombre = models.CharField(max_length=50, choices=[('trípode', 'Trípode'), ('filtro', 'Filtro')])
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class PrestamoAccesorio(models.Model):
    idpa = models.AutoField(primary_key=True)  # idpa como campo autoincremental
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    accesorio = models.ForeignKey(Accesorio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Accesorio {self.accesorio.nombre} para préstamo {self.prestamo.idpre}"
