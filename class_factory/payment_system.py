from abc import ABC, abstractmethod


class MetodoPago(ABC):

    @abstractmethod
    def pagar(self, monto: float) -> str:
        pass


class PagoEfectivo(MetodoPago):

    def pagar(self, monto: float) -> str:
        return f"Pago en efectivo registrado. Total: ${monto:.2f}"


class PagoTarjeta(MetodoPago):

    def pagar(self, monto: float) -> str:
        comision = monto * 0.03
        total = monto + comision

        return (
            f"Pago con tarjeta registrado. "
            f"Monto: ${monto:.2f}, "
            f"comision: ${comision:.2f}, "
            f"total: ${total:.2f}"
        )


class PagoTransferencia(MetodoPago):

    def pagar(self, monto: float) -> str:
        comision = monto * 0.01
        total = monto + comision

        return (
            f"Transferencia registrada. "
            f"Monto: ${monto:.2f}, "
            f"comision: ${comision:.2f}, "
            f"total: ${total:.2f}"
        )


class FabricaPago:

    @staticmethod
    def crear_pago(tipo: str) -> MetodoPago:

        if tipo == "efectivo":
            return PagoEfectivo()

        elif tipo == "tarjeta":
            return PagoTarjeta()

        elif tipo == "transferencia":
            return PagoTransferencia()

        else:
            raise ValueError(
                f"Tipo de pago no soportado: {tipo}"
            )


class PaymentService:

    def pay(self, payment_type: str, amount: float) -> str:

        if amount <= 0:
            return "Monto invalido"

        metodo_pago = FabricaPago.crear_pago(
            payment_type
        )

        return metodo_pago.pagar(amount)