import os
import time

from factories.pago_factory import PagoFactory
from models.metodo_pago import (
    MetodoPago,
    PagoCripto,
    PagoPaypal,
    PagoTarjeta,
    PagoTransferencia,
)
from utils.excepciones import MetodoPagoNoSoportadoError


class AppPagos:
    def __init__(self):
        self.historial = []
        self.usuario_actual = None

    def limpiar_pantalla(self):
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_encabezado(self, titulo):
        print("\n" + "=" * 60)
        print(f"🏦 {titulo}")
        print("=" * 60)

    def mostrar_menu_principal(self):
        self.limpiar_pantalla()
        self.mostrar_encabezado("SISTEMA DE PROCESAMIENTO DE PAGOS")
        print("\n📋 OPCIONES:")
        print("   1. 💳 Procesar un pago")
        print("   2. 📊 Ver historial de pagos")
        print("   3. 📋 Ver métodos de pago disponibles")
        print("   4. 🗑️ Limpiar historial")
        print("   5. 🚪 Salir")
        print("\n" + "=" * 60)

    def mostrar_metodos_pago(self):
        self.limpiar_pantalla()
        self.mostrar_encabezado("MÉTODOS DE PAGO DISPONIBLES")

        metodos = PagoFactory.listar_metodos()
        print("\n📋 Selecciona un método de pago:")
        for opcion, nombre in metodos.items():
            iconos = {"1": "💳", "2": "🌐", "3": "🏦", "4": "🪙"}
            print(f"   {opcion}. {iconos.get(opcion, '')} {nombre}")

        print("\n   0. 🔙 Volver al menú principal")
        print("\n" + "=" * 60)

    def solicitar_datos_tarjeta(self):
        print("\n💳 DATOS DE LA TARJETA:")
        nombre = input("   Titular de la tarjeta: ").strip()
        numero = input("   Número de tarjeta (16 dígitos): ").strip().replace(" ", "")
        cvv = input("   CVV (3 dígitos): ").strip()

        # Validaciones básicas
        while len(numero) != 16 or not numero.isdigit():
            print("   ❌ Número inválido. Debe tener 16 dígitos.")
            numero = (
                input("   Número de tarjeta (16 dígitos): ").strip().replace(" ", "")
            )

        while len(cvv) != 3 or not cvv.isdigit():
            print("   ❌ CVV inválido. Debe tener 3 dígitos.")
            cvv = input("   CVV (3 dígitos): ").strip()

        return {"numero_tarjeta": numero, "cvv": cvv, "nombre": nombre}

    def solicitar_datos_paypal(self):
        print("\n🌐 DATOS DE PAYPAL:")
        email = input("   Email de PayPal: ").strip()
        password = input("   Contraseña: ").strip()

        while "@" not in email:
            print("   ❌ Email inválido. Debe contener '@'")
            email = input("   Email de PayPal: ").strip()

        while len(password) < 6:
            print("   ❌ Contraseña muy corta. Mínimo 6 caracteres.")
            password = input("   Contraseña: ").strip()

        return {"email": email, "password": password}

    def solicitar_datos_transferencia(self):
        print("\n🏦 DATOS DE TRANSFERENCIA:")
        titular = input("   Titular de la cuenta: ").strip()
        banco = input("   Banco: ").strip()
        cuenta = input("   Número de cuenta: ").strip()

        while len(cuenta) < 8:
            print("   ❌ Número de cuenta inválido. Mínimo 8 dígitos.")
            cuenta = input("   Número de cuenta: ").strip()

        return {"titular": titular, "banco": banco, "cuenta": cuenta}

    def solicitar_datos_cripto(self):
        print("\n🪙 DATOS DE CRIPTOMONEDAS:")
        wallet = input("   Dirección de wallet: ").strip()
        red = input("   Red (Ej: Bitcoin, Ethereum, BSC): ").strip()

        while len(wallet) < 10:
            print("   ❌ Wallet inválida. Mínimo 10 caracteres.")
            wallet = input("   Dirección de wallet: ").strip()

        return {"wallet": wallet, "red": red}

    def procesar_pago_interactivo(self):
        self.limpiar_pantalla()
        self.mostrar_metodos_pago()

        opcion = input("\n👉 Selecciona una opción: ").strip()

        if opcion == "0":
            return

        # Solicitar monto
        try:
            monto = float(input("\n💰 Ingresa el monto a pagar: $"))
            if monto <= 0:
                print("❌ El monto debe ser mayor a 0")
                input("\nPresiona Enter para continuar...")
                return
        except ValueError:
            print("❌ Monto inválido. Ingresa un número.")
            input("\nPresiona Enter para continuar...")
            return

        # Solicitar datos según el método
        kwargs = {}
        if opcion == "1":
            kwargs = self.solicitar_datos_tarjeta()
        elif opcion == "2":
            kwargs = self.solicitar_datos_paypal()
        elif opcion == "3":
            kwargs = self.solicitar_datos_transferencia()
        elif opcion == "4":
            kwargs = self.solicitar_datos_cripto()
        else:
            print("❌ Opción no válida")
            input("\nPresiona Enter para continuar...")
            return

        # Crear y procesar el pago
        try:
            print("\n⏳ Procesando pago...")
            time.sleep(1.5)  # Simular procesamiento

            metodo = PagoFactory.crear_pago(opcion, **kwargs)
            resultado = metodo.pagar(monto)

            # Guardar en historial
            self.historial.append(
                {
                    "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "metodo": PagoFactory.listar_metodos()[opcion],
                    "monto": monto,
                    "resultado": resultado,
                    "exitoso": True,
                }
            )

            print("\n" + "=" * 60)
            print("🎉 ¡PAGO EXITOSO!")
            print("=" * 60)
            print(f"\n{resultado}")
            print(f"\n📝 Referencia: #{len(self.historial):04d}")

        except MetodoPagoNoSoportadoError as e:
            print(f"\n{e}")
        except Exception as e:
            print(f"\n❌ Error inesperado: {str(e)}")

        input("\n\nPresiona Enter para continuar...")

    def mostrar_historial(self):
        """Muestra el historial de pagos"""
        self.limpiar_pantalla()
        self.mostrar_encabezado("HISTORIAL DE PAGOS")

        if not self.historial:
            print("\n📭 No hay pagos registrados aún.")
        else:
            print("\n📊 REGISTRO DE PAGOS:")
            print("-" * 60)
            for i, pago in enumerate(self.historial, 1):
                print(f"\n{i}. {pago['fecha']}")
                print(f"   📌 Método: {pago['metodo']}")
                print(f"   💰 Monto: ${pago['monto']:.2f}")
                print(f"   ✅ Estado: {pago['resultado']}")
            print("\n" + "-" * 60)
            print(f"\n📊 Total de pagos: {len(self.historial)}")
            total = sum(p["monto"] for p in self.historial)
            print(f"💵 Monto total procesado: ${total:.2f}")

        input("\nPresiona Enter para continuar...")

    def limpiar_historial(self):
        """Limpia el historial de pagos"""
        self.limpiar_pantalla()
        self.mostrar_encabezado("LIMPIAR HISTORIAL")

        if not self.historial:
            print("\n📭 El historial ya está vacío.")
        else:
            confirmacion = input(
                f"\n⚠️ ¿Estás seguro de eliminar {len(self.historial)} registros? (s/n): "
            ).lower()
            if confirmacion == "s":
                self.historial.clear()
                print("\n✅ Historial limpiado correctamente.")
            else:
                print("\n❌ Operación cancelada.")

        input("\nPresiona Enter para continuar...")

    def mostrar_metodos_disponibles(self):
        """Muestra los métodos de pago disponibles"""
        self.limpiar_pantalla()
        self.mostrar_encabezado("MÉTODOS DE PAGO DISPONIBLES")

        metodos = PagoFactory.listar_metodos()
        print("\n📋 Métodos de pago soportados:")
        for opcion, nombre in metodos.items():
            print(f"   {opcion}. {nombre}")

        print("\n🔧 Cada método requiere datos específicos:")
        print("   💳 Tarjeta: Número, CVV, Titular")
        print("   🌐 PayPal: Email, Contraseña")
        print("   🏦 Transferencia: Banco, Cuenta, Titular")
        print("   🪙 Cripto: Wallet, Red")

        input("\nPresiona Enter para continuar...")

    def ejecutar(self):
        """Bucle principal de la aplicación"""
        while True:
            self.mostrar_menu_principal()

            opcion = input("\n👉 Selecciona una opción: ").strip()

            if opcion == "1":
                self.procesar_pago_interactivo()
            elif opcion == "2":
                self.mostrar_historial()
            elif opcion == "3":
                self.mostrar_metodos_disponibles()
            elif opcion == "4":
                self.limpiar_historial()
            elif opcion == "5":
                print("\n👋 ¡Gracias por usar el sistema de pagos!")
                print("🔒 Cerrando sesión...")
                break
            else:
                print("\n❌ Opción no válida. Por favor, selecciona 1-5.")
                input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    app = AppPagos()
    app.ejecutar()
