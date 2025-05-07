from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Camara, Fotografo, Prestamo, Accesorio, PrestamoAccesorio
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch

# Vista de inicio
def inicio(request):
    return render(request, "inicio.html")

# Vista de home
def home(request):
    return render(request, "home.html")

# Vista para agregar nueva cámara
def nuevaCamara(request):
    return render(request, "nuevaCamara.html")

# Vista para agregar nuevo fotógrafo
def nuevoFotografo(request):
    return render(request, "nuevoFotografo.html")

# Vista para agregar nuevo préstamo
def nuevoPrestamo(request):
    camaras = Camara.objects.all()
    fotografos = Fotografo.objects.all()
    accesorios = Accesorio.objects.filter(disponible=True)  # Solo los disponibles

    return render(request, 'nuevoPrestamo.html', {
        'camaras': camaras,
        'fotografos': fotografos,
        'accesorios': accesorios
    })

# Vista para agregar nuevo accesorio
def nuevoAccesorio(request):
    return render(request, "nuevoAccesorio.html")

# Listar cámaras
def listarCamaras(request):
    camaras = Camara.objects.all()
    return render(request, "listaCamara.html", {'camaras': camaras})

# Listar fotógrafos
def listarFotografos(request):
    fotografos = Fotografo.objects.all()
    return render(request, "listaFotografos.html", {'fotografos': fotografos})


# Listar préstamos
def listarPrestamos(request):
    prestamos = Prestamo.objects.all().prefetch_related(
        Prefetch('prestamoaccesorio_set', queryset=PrestamoAccesorio.objects.select_related('accesorio'))
    )
    return render(request, "listaPrestamos.html", {'prestamos': prestamos})


# Listar accesorios
def listarAccesorios(request):
    accesorios = Accesorio.objects.all()
    return render(request, "listaAccesorio.html", {'accesorios': accesorios})

# Guardar nueva cámara
def guardar_camara(request):
    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        tipo = request.POST.get('tipo')
        valor_mercado = request.POST.get('valor_mercado')

        if not modelo or not tipo or not valor_mercado:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('nuevaCamara')

        try:
            Camara.objects.create(modelo=modelo, tipo=tipo, valor_mercado=valor_mercado)
            messages.success(request, "Cámara registrada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al registrar la cámara: {str(e)}")

        return redirect('listarCamaras')
    return redirect('nuevaCamara')

# Guardar nuevo fotógrafo
def guardar_fotografo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_cliente = request.POST.get('tipo_cliente')

        if not nombre or not tipo_cliente:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('nuevoFotografo')

        try:
            Fotografo.objects.create(nombre=nombre, tipo_cliente=tipo_cliente)
            messages.success(request, "Fotógrafo registrado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al registrar el fotógrafo: {str(e)}")

        return redirect('listarFotografos')
    return redirect('nuevoFotografo')

# Guardar nuevo préstamo
def guardar_prestamo(request):
    if request.method == 'POST':
        camara_id = request.POST.get('camara')
        fotografo_id = request.POST.get('fotografo')
        fecha_salida = request.POST.get('fecha_salida')
        seguro_activo = request.POST.get('seguro_activo') == 'on'
        accesorios_ids = request.POST.getlist('accesorios')  # ← lista de IDs de accesorios

        if not camara_id or not fotografo_id or not fecha_salida:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('nuevoPrestamo')

        try:
            camara = Camara.objects.get(idcam=camara_id)
            fotografo = Fotografo.objects.get(idfot=fotografo_id)

            # Guardar el préstamo
            prestamo = Prestamo.objects.create(
                camara=camara,
                fotografo=fotografo,
                fecha_salida=fecha_salida,
                seguro_activo=seguro_activo
            )

            # Registrar accesorios relacionados
            for acc_id in accesorios_ids:
                accesorio = Accesorio.objects.get(idacc=acc_id)
                PrestamoAccesorio.objects.create(
                    prestamo=prestamo,
                    accesorio=accesorio
                )
                accesorio.disponible = False
                accesorio.save()

            messages.success(request, "Préstamo registrado correctamente con sus accesorios.")
        except Exception as e:
            messages.error(request, f"Error al registrar el préstamo: {str(e)}")

        return redirect('listarPrestamos')

    return redirect('nuevoPrestamo')

# Guardar nuevo accesorio
def guardar_accesorio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        disponible = request.POST.get('disponible') == 'on'

        if not nombre:
            messages.error(request, "El nombre del accesorio es obligatorio.")
            return redirect('nuevoAccesorio')

        try:
            Accesorio.objects.create(nombre=nombre, disponible=disponible)
            messages.success(request, "Accesorio registrado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al registrar el accesorio: {str(e)}")

        return redirect('listarAccesorios')
    return redirect('nuevoAccesorio')

# Editar cámara
def editar_camara(request, idcam):
    try:
        camara = Camara.objects.get(idcam=idcam)
        return render(request, 'editar_camara.html', {'camara': camara})
    except Camara.DoesNotExist:
        messages.error(request, "La cámara no existe.")
        return redirect('listarCamaras')

# Procesar edición de cámara
def procesar_edicion_camara(request, idcam):
    if request.method == 'POST':
        try:
            camara = Camara.objects.get(idcam=idcam)
            camara.modelo = request.POST['modelo']
            camara.tipo = request.POST['tipo']
            camara.valor_mercado = request.POST['valor_mercado']
            camara.save()
            messages.success(request, "Cámara actualizada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar la cámara: {str(e)}")
    return redirect('listarCamaras')

# Editar fotógrafo
def editar_fotografo(request, idfot):
    try:
        fotografo = Fotografo.objects.get(idfot=idfot)
        return render(request, 'editar_fotografo.html', {'fotografo': fotografo})
    except Fotografo.DoesNotExist:
        messages.error(request, "El fotógrafo no existe.")
        return redirect('listarFotografos')

# Procesar edición de fotógrafo
def procesar_edicion_fotografo(request, idfot):
    if request.method == 'POST':
        try:
            fotografo = Fotografo.objects.get(idfot=idfot)
            fotografo.nombre = request.POST['nombre']
            fotografo.tipo_cliente = request.POST['tipo_cliente']
            fotografo.save()
            messages.success(request, "Fotógrafo actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el fotógrafo: {str(e)}")
    return redirect('listarFotografos')

# Editar préstamo
# Editar préstamo
def editar_prestamo(request, idpre):
    try:
        # Obtiene el préstamo, las cámaras y los fotógrafos
        prestamo = Prestamo.objects.get(idpre=idpre)
        camaras = Camara.objects.all()
        fotografos = Fotografo.objects.all()
        accesorios = Accesorio.objects.all()

        # Obtener los accesorios asociados al préstamo
        selected_accesorios = prestamo.prestamoaccesorio_set.all()

        # Pasa todo el contexto en un solo diccionario
        context = {
            'prestamo': prestamo,
            'camaras': camaras,
            'fotografos': fotografos,
            'accesorios': accesorios,
            'selected_accesorios': selected_accesorios,  # Accesorios seleccionados para este préstamo
        }

        # Renderiza la plantilla con los datos
        return render(request, 'editar_prestamo.html', context)
    except Prestamo.DoesNotExist:
        messages.error(request, "El préstamo no existe.")
        return redirect('listarPrestamos')

# Procesar edición de préstamo
# Procesar edición de préstamo
def procesar_edicion_prestamo(request, idpre):
    if request.method == 'POST':
        try:
            prestamo = Prestamo.objects.get(idpre=idpre)

            # Actualizar campos de préstamo
            prestamo.fecha_salida = request.POST['fecha_salida']
            prestamo.seguro_activo = request.POST.get('seguro_activo') == 'on'
            prestamo.save()

            # Gestionar los accesorios seleccionados
            selected_accesorios = request.POST.getlist('accesorios')
            
            # Eliminar accesorios previamente asociados
            prestamo.prestamoaccesorio_set.all().delete()

            # Asociar los nuevos accesorios seleccionados
            for accesorio_id in selected_accesorios:
                accesorio = Accesorio.objects.get(idacc=accesorio_id)
                PrestamoAccesorio.objects.create(prestamo=prestamo, accesorio=accesorio)

            messages.success(request, "Préstamo actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el préstamo: {str(e)}")

    return redirect('listarPrestamos')


# Editar accesorio
def editar_accesorio(request, idacc):
    try:
        accesorio = Accesorio.objects.get(idacc=idacc)
        return render(request, 'editar_accesorio.html', {'accesorio': accesorio})
    except Accesorio.DoesNotExist:
        messages.error(request, "El accesorio no existe.")
        return redirect('listarAccesorios')

# Procesar edición de accesorio
def procesar_edicion_accesorio(request, idacc):
    if request.method == 'POST':
        try:
            accesorio = Accesorio.objects.get(idacc=idacc)
            accesorio.nombre = request.POST['nombre']
            accesorio.disponible = request.POST.get('disponible') == 'on'
            accesorio.save()
            messages.success(request, "Accesorio actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el accesorio: {str(e)}")
    return redirect('listarAccesorios')

# Eliminar cámara
@csrf_exempt
def eliminar_camara(request, idcam):
    if request.method == 'POST':
        try:
            camara = Camara.objects.get(idcam=idcam)
            camara.delete()
            return JsonResponse({'success': True, 'message': 'Cámara eliminada correctamente.'})
        except Camara.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'La cámara no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Eliminar fotógrafo
@csrf_exempt
def eliminar_fotografo(request, idfot):
    if request.method == 'POST':
        try:
            fotografo = Fotografo.objects.get(idfot=idfot)
            fotografo.delete()
            return JsonResponse({'success': True, 'message': 'Fotógrafo eliminado correctamente.'})
        except Fotografo.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El fotógrafo no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Eliminar préstamo
@csrf_exempt
def eliminar_prestamo(request, idpre):
    if request.method == 'POST':
        try:
            prestamo = Prestamo.objects.get(idpre=idpre)
            prestamo.delete()
            return JsonResponse({'success': True, 'message': 'Préstamo eliminado correctamente.'})
        except Prestamo.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El préstamo no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Eliminar accesorio
@csrf_exempt
def eliminar_accesorio(request, idacc):
    if request.method == 'POST':
        try:
            accesorio = Accesorio.objects.get(idacc=idacc)
            accesorio.delete()
            return JsonResponse({'success': True, 'message': 'Accesorio eliminado correctamente.'})
        except Accesorio.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El accesorio no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
