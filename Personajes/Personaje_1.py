from Logic_All.logic_combat import CombatLogic
from PIL import Image
from Personajes.Objects import Pocion, HiperPocion, Antidoto, Elixir
# Personaje 1: Tortuga
class Tortuga:
    def __init__(self):
        self.nombre = "🐢 Tortuga"
        self.imagen = "Image/TortugaPixel.png"
        self.vida_max = 20000
        self.vida = 20000
        self.energia_max = 8000
        self.energia = 8000
        self.defensa_max = 3500
        self.defensa = 3500
        self.ataque = 900
        self.estados = []
        self.turnos_estado = {}
        self.habilidad_disponible = True
        # Contadores de objetos
        self.usos_pocion = 0
        self.usos_antidoto = 0
        self.usos_hiper_pocion = 0
        self.usos_elixir = 0
        # Objetos
        self.pocion = Pocion()
        self.hiper_pocion = HiperPocion()
        self.antidoto = Antidoto()
        self.elixir = Elixir()

 # Procesar estados
    def procesar_estados(self):
        to_remove = []
        for estado in list(self.turnos_estado.keys()):
            self.turnos_estado[estado] -= 1
            if self.turnos_estado[estado] <= 0:
                to_remove.append(estado)
        for estado in to_remove:
            if estado in self.estados:
                self.estados.remove(estado)
            self.turnos_estado.pop(estado)

    # Ataque
    def ataque_normal(self, enemigo): return self.cabezaso(enemigo)
    def ataque_especial(self, enemigo): return self.hidrochorro(enemigo)
    def habilidad_definitiva(self, enemigo): return self.hidrodama(enemigo)
    def incremento(self): return self.rompecoraza()
    def nombre_ataque_normal(self): return "Cabezaso"
    def nombre_ataque_especial(self): return "Hidrochorro"
    def nombre_habilidad_definitiva(self): return "HidroDama"
    def nombre_incremento(self): return "RompeCoraza"

# Ataques específicos
    def cabezaso(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 100
        multiplicador = 0.1
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Cabezaso")

# Ataque especial
    def hidrochorro(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 150
        multiplicador = 0.2
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Hidrochorro", especial=True)

# Incremento de ataque
    def rompecoraza(self):
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        self.turnos_estado["incremento_ataque"] = 6
        self.ataque = int(self.ataque * 1.2)
        return "RompeCoraza activada: ¡Ataque incrementado en 20% por 6 turnos!"

# Habilidad definitiva
    def hidrodama(self, enemigo):
        if not self.habilidad_disponible:
            return "¡La habilidad definitiva no está disponible!"
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 200
        multiplicador = 0.35
        dano = int(base + self.ataque * multiplicador)
        self.habilidad_disponible = False
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="HidroDama", definitiva=True)

    # Defensa
    def defensa_habilidad_1(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("caparason_hueco")
        self.turnos_estado["caparason_hueco"] = 2
        return f"Caparason Hueco: Defensa incrementada en 30% ({cantidad}) este turno."

    def defensa_habilidad_2(self):
        cantidad = int(self.defensa_max * 0.7)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("hidrocaparazon")
        self.turnos_estado["hidrocaparazon"] = 2
        return f"HidroCaparazon: Defensa incrementada en 70% ({cantidad}) este turno."

    def defensa_buff(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("buff_defensa")
        self.turnos_estado["buff_defensa"] = 6
        return f"Caparazon Chueco: Defensa aumentada un 30% ({cantidad})."

    def defensa_esquive(self):
        self.estados.append("esquive")
        self.turnos_estado["esquive"] = 2
        return "Caparason Fuera: ¡Tienes 20% de probabilidad de esquivar el próximo ataque!"

    # Energía
    def energia_carga(self):
        cargar = int(self.energia_max * 0.35)
        self.energia = min(self.energia + cargar, self.energia_max)
        return f"Chueco: ¡Has cargado {cargar} puntos de energía!"

    def energia_carga_max(self):
        self.estados.append("recarga_maxima")
        self.turnos_estado["recarga_maxima"] = 4
        self.energia = self.energia_max
        return CombatLogic.recarga_maxima(self)
    
    def usar_objeto(self, tipo):
        if tipo == "pocion": return self.pocion.usar(self)
        elif tipo == "hiper_pocion": return self.hiper_pocion.usar(self)
        elif tipo == "cura_estado": return self.antidoto.usar(self)
        elif tipo == "elixir": return self.elixir.usar(self)
        else: return "Objeto desconocido."

# Nombres de habilidades
    def nombre_defensa_1(self): return "Caparason Hueco"
    def nombre_defensa_2(self): return "HidroCaparazon"
    def nombre_defensa_buff(self): return "Caparazon Chueco"
    def nombre_defensa_esquive(self): return "Caparason Fuera"
    def nombre_energia_carga(self): return "Chueco"
    def nombre_energia_carga_max(self): return "Consentración Visual"