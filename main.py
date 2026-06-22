from payment_system import PaymentService


def run_demo() -> None:
    service = PaymentService()

    print("=== Demo de medios de pago (antipatron) ===")
    print(service.pay("efectivo", 1200.0))
    print(service.pay("tarjeta", 1200.0))
    print(service.pay("transferencia", 1200.0))


if __name__ == "__main__":
    run_demo()
