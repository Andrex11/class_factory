from models.metodo_pago import (
    MetodoPago,
    PagoCripto,
    PagoPaypal,
    PagoTarjeta,
    PagoTransferencia,
)
from utils.excepciones import MetodoPagoNoSoportadoError


class PagoFactory:
    """Fábrica para crear instancias de métodos de pago"""

    _metodos = {
        "1": {"nombre": "Tarjeta de Crédito", "clase": PagoTarjeta},
        "2": {"nombre": "PayPal", "clase": PagoPaypal},
        "3": {"nombre": "Transferencia Bancaria", "clase": PagoTransferencia},
        "4": {"nombre": "Criptomonedas", "clase": PagoCripto},
    }

    @staticmethod
    def crear_pago(opcion: str, **kwargs) -> MetodoPago:
        """
        Crea una instancia del método de pago solicitado

        Args:
            opcion: String con la opción seleccionada ("1", "2", "3", "4")
            **kwargs: Parámetros específicos para cada método

        Returns:
            MetodoPago: Instancia del método de pago

        Raises:
            MetodoPagoNoSoportadoError: Si la opción no es válida
        """
        # Buscar el método en el diccionario
        metodo_info = PagoFactory._metodos.get(opcion)

        if metodo_info is None:
            disponibles = ", ".join(
                [f"{k}. {v['nombre']}" for k, v in PagoFactory._metodos.items()]
            )
            raise MetodoPagoNoSoportadoError(
                f"❌ Opción '{opcion}' no válida.\n📋 Opciones disponibles: {disponibles}"
            )

        try:
            # Obtener la clase
            clase = metodo_info["clase"]

            # Filtrar los kwargs para que solo pasen los que espera la clase
            # Esto evita errores de parámetros inesperados
            import inspect

            sig = inspect.signature(clase.__init__)
            params = list(sig.parameters.keys())

            # Filtrar kwargs para solo incluir los que acepta el constructor
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in params}

            # Crear la instancia
            return clase(**filtered_kwargs)

        except TypeError as e:
            raise MetodoPagoNoSoportadoError(
                f"❌ Error al crear el método de pago: {str(e)}"
            )
        except Exception as e:
            raise MetodoPagoNoSoportadoError(
                f"❌ Error inesperado al crear el método: {str(e)}"
            )

    @staticmethod
    def listar_metodos() -> dict:
        """
        Devuelve los métodos de pago disponibles

        Returns:
            dict: Diccionario con opción -> nombre del método
        """
        return {k: v["nombre"] for k, v in PagoFactory._metodos.items()}
