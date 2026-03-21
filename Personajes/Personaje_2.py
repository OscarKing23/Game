from Logic_All.logic_combat import CombatLogic
from PIL import Image
from Personajes.Objects import Pocion, HiperPocion, Antidoto, Elixir

# Personaje 2: Dragón
class Dragon:
    def __init__(self):
        self.nombre = "🐉 Dragón"
        self.imagen = "Image/DragonPixel.jpeg"
        self.vida_max = 12000
        self.vida = 12000
        self.energia_max = 13000
        self.energia = 13000
        self.defensa_max = 2200
        self.defensa = 2200
        self.ataque = 1500
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

# Procesar estados de personaje
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
    def ataque_normal(self, enemigo): return self.llamarada(enemigo)
    def ataque_especial(self, enemigo): return self.aliento_dragon(enemigo)
    def habilidad_definitiva(self, enemigo): return self.meteorito_supremo(enemigo)
    def incremento(self): return self.furia_draconica()
    def nombre_ataque_normal(self): return "Llamarada"
    def nombre_ataque_especial(self): return "Aliento Dragón"
    def nombre_habilidad_definitiva(self): return "Meteorito Supremo"
    def nombre_incremento(self): return "Furia Dracónica"

    def llamarada(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 300
        multiplicador = 0.4
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Llamarada")

    def aliento_dragon(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 450
        multiplicador = 0.6
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Aliento Dragón", especial=True)

    def furia_draconica(self):
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        self.turnos_estado["incremento_ataque"] = 6
        self.ataque = int(self.ataque * 1.4)
        return "Furia Dracónica activada: ¡Ataque incrementado en 40% por 6 turnos!"

    def meteorito_supremo(self, enemigo):
        if not self.habilidad_disponible:
            return "¡La habilidad definitiva no está disponible!"
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 1200
        multiplicador = 1.2
        dano = int(base + self.ataque * multiplicador)
        self.habilidad_disponible = False
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Meteorito Supremo", definitiva=True)

    # Defensa
    def defensa_habilidad_1(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("escamas_recias")
        self.turnos_estado["escamas_recias"] = 2
        return f"Escamas Récías: Defensa incrementada en 30% ({cantidad}) este turno."

    def defensa_habilidad_2(self):
        cantidad = int(self.defensa_max * 0.7)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("barrera_fuego")
        self.turnos_estado["barrera_fuego"] = 2
        return f"Barrera de Fuego: Defensa incrementada en 70% ({cantidad}) este turno."

    def defensa_buff(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("buff_defensa")
        self.turnos_estado["buff_defensa"] = 6
        return f"Foco Dracónico: Defensa aumentada un 30% ({cantidad})."

    def defensa_esquive(self):
        self.estados.append("esquive")
        self.turnos_estado["esquive"] = 2
        return "Ala Veloz: ¡Tienes 25% de probabilidad de esquivar el próximo ataque!"

    # Energía
    def energia_carga(self):
        cargar = int(self.energia_max * 0.45)
        self.energia = min(self.energia + cargar, self.energia_max)
        return f"Energía Pura: ¡Has cargado {cargar} puntos de energía!"

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

#nombre de habilidades y objetos
    def nombre_defensa_1(self): return "Escamas Récías"
    def nombre_defensa_2(self): return "Barrera de Fuego"
    def nombre_defensa_buff(self): return "Foco Dracónico"
    def nombre_defensa_esquive(self): return "Ala Veloz"
    def nombre_energia_carga(self): return "Energía Pura"
    def nombre_energia_carga_max(self): return "Visión Flamante"