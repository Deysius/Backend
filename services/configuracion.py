class Configuracion:

    _instancia = None

    def __new__(cls):

        if cls._instancia is None:

            cls._instancia = super().__new__(cls)

            cls._instancia.nombre = "TimeWise"

            cls._instancia.version = "1.0"

            cls._instancia.estado_proyecto = "Activo"

            cls._instancia.prioridad_proyecto = "Alta"

        return cls._instancia