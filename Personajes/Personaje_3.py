from Logic_All.logic_combat import CombatLogic
from PIL import Image
from Personajes.Objects import Pocion, HiperPocion, Antidoto, Elixir

# Personaje 3: Jason
class Jason:
    def __init__(self):
        self.nombre = "🧙 Jason"
        self.imagen = "Image/stick3.png"
        self.vida_max = 26000
        self.vida = 26000
        self.energia_max = 7000
        self.energia = 7000
        self.defensa_max = 1500
        self.defensa = 1500
        self.ataque = 2100
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

# Ataques y habilidades 
    def ataque_normal(self, enemigo): return self.machetazo(enemigo)
    def ataque_especial(self, enemigo): return self.terror_nocturno(enemigo)
    def habilidad_definitiva(self, enemigo): return self.muerte_inesperada(enemigo)
    def incremento(self): return self.furia_slayer()
    def ataque_normal(self, enemigo):
        return CombatLogic.realizar_ataque(self, enemigo, self._calc_dano_machetazo(), nombre_ataque="Machetazo", especial=False, definitiva=False)
    def ataque_especial(self, enemigo):
        return CombatLogic.realizar_ataque(self, enemigo, self._calc_dano_terror_nocturno(), nombre_ataque="Terror Nocturno", especial=True, definitiva=False)
    def habilidad_definitiva(self, enemigo):
        return CombatLogic.realizar_ataque(self, enemigo, self._calc_dano_muerte_inesperada(), nombre_ataque="Muerte Inesperada", especial=False, definitiva=True)
    def incremento(self):
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        self.turnos_estado["incremento_ataque"] = 6
        self.ataque = int(self.ataque * 1.35)
        return "Furia Slayer activada: ¡Ataque incrementado en 35% por 6 turnos!"

    def _calc_dano_machetazo(self): return int(280 + self.ataque * 0.3)
    def _calc_dano_terror_nocturno(self): return int(340 + self.ataque * 0.6)
    def _calc_dano_muerte_inesperada(self): return int(1500 + self.ataque * 1.1)

    def nombre_ataque_normal(self): return "Machetazo"
    def nombre_ataque_especial(self): return "Terror Nocturno"
    def nombre_habilidad_definitiva(self): return "Muerte Inesperada"
    def nombre_incremento(self): return "Furia Slayer"

    def machetazo(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 280
        multiplicador = 0.3
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Machetazo")

    def terror_nocturno(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 340
        multiplicador = 0.6
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Terror Nocturno", especial=True)

    def furia_slayer(self):
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        self.turnos_estado["incremento_ataque"] = 6
        self.ataque = int(self.ataque * 1.35)
        return "Furia Slayer activada: ¡Ataque incrementado en 35% por 6 turnos!"

    def muerte_inesperada(self, enemigo):
        if not self.habilidad_disponible:
            return "¡La habilidad definitiva no está disponible!"
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 1500
        multiplicador = 1.1
        dano = int(base + self.ataque * multiplicador)
        self.habilidad_disponible = False
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Muerte Inesperada", definitiva=True)

    def defensa_habilidad_1(self):
        ok, msg = CombatLogic.consumir_energia_accion(self, "defensa")
        if not ok: return msg
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("mascara_maligna")
        self.turnos_estado["mascara_maligna"] = 2
        return f"Máscara Maligna: Defensa incrementada en 30% ({cantidad}) este turno."
    def defensa_habilidad_2(self):
        ok, msg = CombatLogic.consumir_energia_accion(self, "defensa_absoluta")
        if not ok: return msg
        cantidad = int(self.defensa_max * 0.7)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("regreso_maligno")
        self.turnos_estado["regreso_maligno"] = 2
        return f"Regreso Maligno: Defensa incrementada en 70% ({cantidad}) este turno."

    def defensa_buff(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("buff_defensa")
        self.turnos_estado["buff_defensa"] = 6
        return f"Piel Slayer: Defensa aumentada un 30% ({cantidad})."

    def defensa_esquive(self):
        self.estados.append("esquive")
        self.turnos_estado["esquive"] = 2
        return "Salto Sorpresa: ¡Tienes 22% de probabilidad de esquivar el próximo ataque!"

    def energia_carga(self):
        cargar = int(self.energia_max * 0.33)
        self.energia = min(self.energia + cargar, self.energia_max)
        return f"Recuperación Macabra: ¡Has cargado {cargar} puntos de energía!"

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
    def nombre_defensa_1(self): return "Máscara Maligna"
    def nombre_defensa_2(self): return "Regreso Maligno"
    def nombre_defensa_buff(self): return "Piel Slayer"
    def nombre_defensa_esquive(self): return "Salto Sorpresa"
    def nombre_energia_carga(self): return "Recuperación Macabra"
    def nombre_energia_carga_max(self): return "Visión Asesina"