# Archivo para los objetos consumibles
# Clase para Poción y HiperPoción
class Pocion:
    def __init__(self):
        self.max_uses = 3
        self.uses = 0
    def usar(self, personaje):
        # Verifica si quedan usos
        if self.uses >= self.max_uses:
            return f"{personaje.nombre} ya usó todas sus pociones."
        # Cura el 25% de la vida máxima
        curado = personaje.vida_max * 0.25
        personaje.vida = min(personaje.vida_max, personaje.vida + curado)
        # Incrementa el contador de usos
        self.uses += 1
        return f"{personaje.nombre} usó una Poción y curó {curado:.1f} de vida. ({self.uses}/{self.max_uses})"

# Clase para HiperPoción 
class HiperPocion:
    def __init__(self):
        self.max_uses = 1
        self.uses = 0
    def usar(self, personaje):
        # Verifica si quedan usos
        if self.uses >= self.max_uses:
            return f"{personaje.nombre} ya usó su HiperPoción."
        # Cura el 70% de la vida máxima
        curado = personaje.vida_max * 0.7
        personaje.vida = min(personaje.vida_max, personaje.vida + curado)
        # Incrementa el contador de usos
        self.uses += 1
        return f"{personaje.nombre} usó HiperPoción y curó {curado:.1f} de vida. (Sólo 1 uso)"

# Clase para Antídoto y Elixir
class Antidoto:
    def __init__(self):
        self.max_uses = 2
        self.uses = 0
    def usar(self, personaje):
        # Verifica si quedan usos
        if self.uses >= self.max_uses:
            return f"{personaje.nombre} ya usó todos sus Antídotos."
        eliminado = []
        # Elimina estados negativos
        for est in ["paralisis", "veneno", "quemadura", "cansancio"]:
            if est in personaje.estados:
                personaje.estados.remove(est)
                if est in personaje.turnos_estado: del personaje.turnos_estado[est]
                eliminado.append(est)
        # Incrementa el contador de usos
        self.uses += 1
        # Mensaje según si se eliminó algún estado       
        if not eliminado:
            return f"{personaje.nombre} usó Antídoto, pero no tenía estados negativos. ({self.uses}/{self.max_uses})"
        return f"{personaje.nombre} eliminó estados negativos ({', '.join(eliminado)}) con Antídoto. ({self.uses}/{self.max_uses})"

# Clase para Elixir
class Elixir:
    def __init__(self):
        self.max_uses = 2
        self.uses = 0
    def usar(self, personaje):
        # Verifica si quedan usos
        if self.uses >= self.max_uses:
            return f"{personaje.nombre} ya usó todos sus Elixir."
        recuperar = int(personaje.energia_max * 0.6)
        # Recupera energía y resetea habilidad definitiva
        personaje.energia = min(personaje.energia_max, personaje.energia + recuperar)
        if hasattr(personaje, "habilidad_disponible"):
            personaje.habilidad_disponible = True
        # Incrementa el contador de usos
        self.uses += 1
        return f"{personaje.nombre} usó Elixir, recuperó {recuperar} energía y puede usar la habilidad definitiva de nuevo. ({self.uses}/{self.max_uses})"