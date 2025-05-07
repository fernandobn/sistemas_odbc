from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.home, name='home'),

    # Formularios de registro
    path('nuevaCamara/', views.nuevaCamara, name='nuevaCamara'),
    path('nuevoFotografo/', views.nuevoFotografo, name='nuevoFotografo'),
    path('nuevoPrestamo/', views.nuevoPrestamo, name='nuevoPrestamo'),
    path('nuevoAccesorio/', views.nuevoAccesorio, name='nuevoAccesorio'),

    # Listados
    path('listarCamaras/', views.listarCamaras, name='listarCamaras'),
    path('listarFotografos/', views.listarFotografos, name='listarFotografos'),
    path('listarPrestamos/', views.listarPrestamos, name='listarPrestamos'),
    path('listarAccesorios/', views.listarAccesorios, name='listarAccesorios'),

    # CRUD Cámara
    path('guardar_camara/', views.guardar_camara, name='guardar_camara'),
    path('editar_camara/<int:idcam>/', views.editar_camara, name='editar_camara'),
    path('procesar_edicion_camara/<int:idcam>/', views.procesar_edicion_camara, name='procesar_edicion_camara'),
    path('eliminarCamara/<int:idcam>/', views.eliminar_camara, name='eliminarCamara'),

    # CRUD Fotógrafo
    path('guardar_fotografo/', views.guardar_fotografo, name='guardar_fotografo'),
    path('editar_fotografo/<int:idfot>/', views.editar_fotografo, name='editarFotografo'),
    path('procesar_edicion_fotografo/<int:idfot>/', views.procesar_edicion_fotografo, name='procesar_edicion_fotografo'),
    path('eliminarFotografo/<int:idfot>/', views.eliminar_fotografo, name='eliminarFotografo'),

    # CRUD Préstamo
    path('guardar_prestamo/', views.guardar_prestamo, name='guardar_prestamo'),
    path('editar_prestamo/<int:idpre>/', views.editar_prestamo, name='editarPrestamo'),
    path('procesar_edicion_prestamo/<int:idpre>/', views.procesar_edicion_prestamo, name='procesar_edicion_prestamo'),
    path('eliminarPrestamo/<int:idpre>/', views.eliminar_prestamo, name='eliminarPrestamo'),

    # CRUD Accesorio
    path('guardar_accesorio/', views.guardar_accesorio, name='guardar_accesorio'),
    path('editar_accesorio/<int:idacc>/', views.editar_accesorio, name='editar_accesorio'),
    path('procesar_edicion_accesorio/<int:idacc>/', views.procesar_edicion_accesorio, name='procesar_edicion_accesorio'),
    path('eliminarAccesorio/<int:idacc>/', views.eliminar_accesorio, name='eliminarAccesorio'),
]
