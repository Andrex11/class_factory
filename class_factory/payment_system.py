from abc import ABC, abstractmethod


# ==========================================
# Paso 1: Crear una clase base o interfaz
# ==========================================
class MetodoPago(ABC):
    @abstractmethod
    def pagar(self, amount: float) -> str:
        """Contrato común para todos los métodos de pago."""
        pass


# ==========================================
# Paso 2: Crear productos concretos
# ==========================================
class PagoEfectivo(MetodoPago):
    def pagar(self, amount: float) -> str:
        return f"Pago en efectivo registrado. Total: ${amount:.2f}"


class PagoTarjeta(MetodoPago):
    def pagar(self, amount: float) -> str:
        fee = amount * 0.03
        total = amount + fee
        return (
            f"Pago con tarjeta registrado. Monto: ${amount:.2f}, "
            f"comision: ${fee:.2f}, total: ${total:.2f}"
        )


class PagoTransferencia(MetodoPago):
    def pagar(self, amount: float) -> str:
        fee = amount * 0.01
        total = amount + fee
        return (
            f"Transferencia registrada. Monto: ${amount:.2f}, "
            f"comision: ${fee:.2f}, total: ${total:.2f}"
        )


# ==========================================
# Paso 3: Crear la fábrica
# ==========================================
class FabricaPago:
    @staticmethod
    def crear_pago(payment_type: str) -> MetodoPago:
        """Encargada de centralizar la creación de las instancias."""
        if payment_type == "efectivo":
            return PagoEfectivo()
        elif payment_type == "tarjeta":
            return PagoTarjeta()
        elif payment_type == "transferencia":
            return PagoTransferencia()
        else:
            raise ValueError(f"Medio de pago no soportado: {payment_type}")


# ==========================================
# Paso 4: Usar la fábrica desde el cliente
# ==========================================
class PaymentService:
    def pay(self, payment_type: str, amount: float) -> str:
        # Validación de negocio inicial
        if amount <= 0:
            return "Monto invalido"

        try:
            # El cliente le pide el tipo de pago a la fábrica
            metodo = FabricaPago.crear_pago(payment_type)
            # Trabaja con el objeto devuelto usando la interfaz común
            return metodo.pagar(amount)
        except ValueError as e:
            # Manejo del error en caso de que el tipo no exista
            return str(e)
        