from models.metodo_pago import (
    MetodoPago,
    PagoCripto,
    PagoPaypal,
    PagoTarjeta,
    PagoTransferencia,
)
from utils.excepciones import MetodoPagoNoSoportadoError


class PagoFactory:
    # Fábrica para crear instancias de métodos de pago

    # Diccionario de métodos disponibles (mapeo tipo -> clase)
    _metodos = {
        "1": {"nombre": "Tarjeta de Crédito", "clase": PagoTarjeta},
        "2": {"nombre": "PayPal", "clase": PagoPaypal},
        "3": {"nombre": "Transferencia Bancaria", "clase": PagoTransferencia},
        "4": {"nombre": "Criptomonedas", "clase": PagoCripto},
    }

    @staticmethod
    def crear_pago(tipo: str, **kwargs) -> MetodoPago:
        metodo_info = PagoFactory._metodos.get(opcion)

        if metodo_info is None:
            disponibles = ", ".join(
                [f"{k}. {v['nombre']}" for k, v in PagoFactory._metodos.items()]
            )

            raise MetodoPagoNoSoportadoError(
                f"Opción '{opcion}' no válida.\n Opciones disponibles: {disponibles}"
            )

        # Normalizar el tipo a minúsculas
        tipo_normalizado = tipo.lower()

        # Buscar la clase en el diccionario
        clase_pago = PagoFactory._metodos.get(tipo_normalizado)

        if clase_pago is None:
            # Si no existe, lanzar excepción personalizada
            disponibles = ", ".join(PagoFactory._metodos.keys())
            raise MetodoPagoNoSoportadoError(
                f"Método de pago '{tipo}' no soportado. Disponibles: {disponibles}"
            )

        try:
            return metodo_info["clase"](**kwargs)
        except TypeError as e:
            raise MetodoPagoNoSoportadoError(
                f"Error al crear el método de pago: {str(e)}"
            )

    @staticmethod
    def listar_metodos() -> dict:
        """Devuelve los métodos de pago disponibles"""
        return {k: v["nombre"] for k, v in PagoFactory._metodos.items()}

