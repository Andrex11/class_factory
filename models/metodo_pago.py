from abc import ABC, abstractmethod


class MetodoPago(ABC):
    """Clase base abstracta para todos los métodos de pago"""

    @abstractmethod
    def pagar(self, monto: float) -> str:
        # Procesa un pago por el monto especificado
        pass

    @abstractmethod
    def validar(self) -> bool:
        # Valida que el método de pago esté configurado correctamente
        pass


class PagoTarjeta(MetodoPago):
    def __init__(self, numero_tarjeta: str = None, cvv: str = None):
        self.numero_tarjeta = numero_tarjeta
        self.cvv = cvv
        self.nombre = nombre

    def pagar(self, monto: float) -> str:
        if not self.validar():
            return "Error: Tarjeta inválida"
        return f"Pago de ${monto:.2f} aprobado con Tarjeta de Crédito (Titular: {self.nombre})"

    def validar(self) -> bool:
        # la tarjeta debe tener 16 dígitos y CVV 3 dígitos
        if not self.numero_tarjeta or len(self.numero_tarjeta) != 16:
            return False
        if not self.cvv or len(self.cvv) != 3:
            return False
        return True


class PagoPaypal(MetodoPago):
    def __init__(self, email: str = None):
        self.email = email

    def pagar(self, monto: float) -> str:
        if not self.validar():
            return "Error: Email de PayPal inválido"
        return f"Pagando ${monto:.2f} con PayPal (Cuenta: {self.email})"

    def validar(self) -> bool:
        # el email debe contener @
        if not self.email or "@" not in self.email:
            return False
        return True


class PagoTransferencia(MetodoPago):
    def __init__(self, banco: str = None, cuenta: str = None):
        self.banco = banco
        self.cuenta = cuenta

    def pagar(self, monto: float) -> str:
        if not self.validar():
            return "Error: Datos bancarios inválidos"
        return f"Pagando ${monto:.2f} vía Transferencia Bancaria (Banco: {self.banco})"

    def validar(self) -> bool:
        # el banco y cuenta deben tener datos
        if not self.banco or not self.cuenta:
            return False
        return True


class PagoCripto(MetodoPago):
    def __init__(self, wallet: str = None):
        self.wallet = wallet

    def pagar(self, monto: float) -> str:
        if not self.validar():
            return "Error: Wallet inválida"
        return f"Pagando ${monto:.2f} con Criptomonedas (Wallet: {self.wallet[:6]}...)"

    def validar(self) -> bool:
        # el wallet debe tener 34 caracteres
        if not self.wallet or len(self.wallet) != 34:
            return False
        return True
