import functools

def gestionar_errores(capa="Sistema"):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                mensaje = f"[{capa.upper()} ERROR] En {func.__name__}: {str(e)}"
                # Usamos el logger que ya tienes inyectado en la clase
                if hasattr(self, 'logger'):
                    self.logger.registrar("ERROR_GENERAL", mensaje, nivel="ERROR")
                else:
                    print(mensaje) # Backup por si el logger no está listo
                return None # O False, dependiendo de lo que necesites
        return wrapper
    return decorador