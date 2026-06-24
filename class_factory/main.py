from payment_system import PaymentService


def mostrar_pago(service: PaymentService, metodo: str, monto: float) -> None:
    print(service.pay(metodo, monto))


def run_demo() -> None:
    service = PaymentService()

    print("=== Demo de medios de pago (antipatrón) ===")

    metodos_pago = [
        "efectivo",
        "tarjeta",
        "transferencia",
    ]

    for metodo in metodos_pago:
        mostrar_pago(service, metodo, 1200.0)


if __name__ == "__main__":
    run_demo()