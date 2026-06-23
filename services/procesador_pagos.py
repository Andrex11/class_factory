from factories.pago_factory import PagoFactory
from models.metodo_pago import MetodoPago


class ProcesadorPagos:
    # Servicio que procesa pagos usando la fábrica de métodos de pago

    def __init__(self):
        self.historial = []

    def procesar_pago(self, tipo_pago: str, monto: float, **kwargs) -> str:
        try:
            # Método de pago usando la fábrica
            metodo = PagoFactory.crear_pago(tipo_pago, **kwargs)

            # Validar el método de pago
            if not metodo.validar():
                return "Error: Falló la validación del método de pago"

            # Ejecutar el pago
            resultado = metodo.pagar(monto)

            # Guardar en historial
            self.historial.append(
                {
                    "tipo": tipo_pago,
                    "monto": monto,
                    "resultado": resultado,
                    "exitoso": True,
                }
            )

            return resultado

        except Exception as e:
            # Guardar error en historial
            self.historial.append(
                {"tipo": tipo_pago, "monto": monto, "error": str(e), "exitoso": False}
            )
            return f"Error procesando pago: {str(e)}"

    def mostrar_metodos_disponibles(self):
        """Muestra los métodos de pago disponibles"""
        metodos = PagoFactory.listar_metodos()
        print("\n Métodos de pago disponibles:")
        for i, metodo in enumerate(metodos, 1):
            print(f"   {i}. {metodo.capitalize()}")
        print()
