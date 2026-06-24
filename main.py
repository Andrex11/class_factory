from payment_system import PaymentService

def run_demo() -> None:
    service = PaymentService()

    print("   SISTEMA DE PAGOS   ")


    while True:
        print("\nMedios de pago disponibles:")
        print("1. Efectivo")
        print("2. Tarjeta (Comision: 3%)")
        print("3. Transferencia (Comision: 1%)")
        print("4. Crypto")
        print("5. Salir del simulador")
        
        opcion = input("\nSelecciona una opcion (1-5): ").strip()

        if opcion == "5":
            print("\nGracias por usar el simulador. ¡Hasta luego!")
            break

        if opcion == "1":
            tipo_pago = "efectivo"
        elif opcion == "2":
            tipo_pago = "tarjeta"
        elif opcion == "3":
            tipo_pago = "transferencia"
        elif opcion == "4":
            tipo_pago = "crypto"
        else:
            print("\nError: Opcion invalida. Intenta de nuevo.")
            continue

        try:
            monto_input = input(f"Ingresa el monto para el pago con {tipo_pago}: ")
            monto = float(monto_input)
        except ValueError:
            print("\nError: El monto debe ser un numero valido.")
            continue

        print("\n--- Procesando transaccion con la Fabrica ---")
        resultado = service.pay(tipo_pago, monto)
        print(resultado)
        print("==================================================")

if __name__ == "__main__":
    run_demo()