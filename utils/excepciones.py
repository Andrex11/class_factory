class MetodoPagoNoSoportadoError(Exception):
    """Excepción lanzada cuando se solicita un método de pago no soportado"""
    pass


class ValidacionPagoError(Exception):
    """Excepción lanzada cuando falla la validación de un método de pago"""
    pass