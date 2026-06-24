from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def procesarPago(self, monto: float):
        pass

class TarjetaCredito(MetodoPago):
    def procesarPago(self, monto):
        print(f"Cobro ${monto} via Pasarela")

class Paypal(MetodoPago):
    def procesarPago(self, monto):
        print(f"Cobro ${monto} via paypal")
    

class PagoFactory:
    @staticmethod
    def crearPago(tipo):
        if (tipo == "tarjeta"):
            return TarjetaCredito()
        elif (tipo == "paypal"):
            return Paypal()
