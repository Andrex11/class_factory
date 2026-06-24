from payment_system import PaymentService


def run_demo() -> None:
    # Inicializamos el servicio de pagos (el cliente no necesita saber qué pasa por detrás)
    service = PaymentService()

    print("=== Demo de Sistema de Pagos (Patrón Factory) ===")

    # Lista de pruebas con diferentes medios de pago y montos
    pruebas = [
        ("efectivo", 1200.0),
        ("tarjeta", 1200.0),
        ("transferencia", 1200.0),
        ("cripto", 500.0),  # Caso de prueba para verificar manejo de errores
        ("tarjeta", -50.0),  # Caso de prueba para verificar monto inválido
    ]

    # Ejecutamos las pruebas de manera limpia y legible
    for medio, monto in pruebas:
        print(f"\nProcesando: {medio} por ${monto:.2f}...")
        resultado = service.pay(medio, monto)
        print(f"Resultado: {resultado}")


if __name__ == "__main__":
    run_demo()
    