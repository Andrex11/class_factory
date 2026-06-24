from payment_factory import PaymentFactory

class PaymentService:
    def pay(self, payment_type: str, amount: float) -> str:
        if amount <= 0:
            return "Monto invalido"

        metodo = PaymentFactory.crear_pago(payment_type, self)
        
        if metodo:
            return metodo.pagar(amount)
        
        return f"Medio de pago no soportado: {payment_type}"

    def _pay_cash(self, amount: float) -> str:
        return f"Pago en efectivo registrado. Total: ${amount:.2f}"

    def _pay_card(self, amount: float) -> str:
        fee = amount * 0.03
        total = amount + fee
        return (
            f"Pago con tarjeta registrado. Monto: ${amount:.2f}, "
            f"comision: ${fee:.2f}, total: ${total:.2f}"
        )

    def _pay_transfer(self, amount: float) -> str:
        fee = amount * 0.01
        total = amount + fee
        return (
            f"Transferencia registrada. Monto: ${amount:.2f}, "
            f"comision: ${fee:.2f}, total: ${total:.2f}"
        )
