from models.proyecto import Proyecto
from services.configuracion import Configuracion


class ProyectoFactory:

    @staticmethod
    def crear_proyecto(
        nombre,
        descripcion,
        fecha_inicio,
        fecha_fin,
        horas_estimadas,
        usuario_id
    ):

        config = Configuracion()

        return Proyecto(

            nombre=nombre,

            descripcion=descripcion,

            fecha_inicio=fecha_inicio,

            fecha_fin=fecha_fin,

            horas_estimadas=horas_estimadas,

            prioridad=config.prioridad_proyecto,

            estado=config.estado_proyecto,

            usuario_id=usuario_id

        )