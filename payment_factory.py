from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def pagar(self, amount: float) -> str:
        pass

class PagoEfectivo(MetodoPago):
    def __init__(self, servicio):
        self.servicio = servicio
    def pagar(self, amount: float) -> str:
        return self.servicio._pay_cash(amount)

class PagoTarjeta(MetodoPago):
    def __init__(self, servicio):
        self.servicio = servicio
    def pagar(self, amount: float) -> str:
        return self.servicio._pay_card(amount)

class PagoTransferencia(MetodoPago):
    def __init__(self, servicio):
        self.servicio = servicio
    def pagar(self, amount: float) -> str:
        return self.servicio._pay_transfer(amount)

class PagoCrypto(MetodoPago):
    def __init__(self, servicio):
        self.servicio = servicio
    def pagar(self, amount: float) -> str:
        # El profe dijo que no toquemos PaymentService, así que hacemos la lógica aquí directo
        return f"Pago con Criptomonedas registrado de forma segura. Total: ${amount:.2f}"



class PaymentFactory:
    @staticmethod
    def crear_pago(payment_type: str, servicio) -> MetodoPago:
        if payment_type == "efectivo":
            return PagoEfectivo(servicio)
        elif payment_type == "tarjeta":
            return PagoTarjeta(servicio)
        elif payment_type == "transferencia":
            return PagoTransferencia(servicio)
        elif payment_type == "crypto":  # <--- Agregado en la fábrica
            return PagoCrypto(servicio)
        else:
            return None