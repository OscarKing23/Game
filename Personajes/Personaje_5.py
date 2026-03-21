from Logic_All.logic_combat import CombatLogic
from PIL import Image
from Personajes.Objects import Pocion, HiperPocion, Antidoto, Elixir
import random

# Personaje 5: Kratos
class Kratos:
    def __init__(self):
        self.nombre = "🥷 Kratos"
        self.imagen = "Image/kratos.jpg"
        self.vida_max = 15000
        self.vida = 15000
        self.energia_max = 9000
        self.energia = 9000
        self.defensa_max = 1800
        self.defensa = 1800
        self.ataque = 3200
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
    def ataque_normal(self, enemigo): return self.hacha_leviatán(enemigo)
    def ataque_especial(self, enemigo): return self.espadas_caos(enemigo)
    def habilidad_definitiva(self, enemigo): return self.espada_olimpo(enemigo)
    def incremento(self): return self.ira_espartano()
    def nombre_ataque_normal(self): return "Hacha Leviatán"
    def nombre_ataque_especial(self): return "Espadas del Caos"
    def nombre_habilidad_definitiva(self): return "Ira de Kratos"
    def nombre_incremento(self): return "Modo Espartano"

    def hacha_leviatán(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 400
        multiplicador = 0.55
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Hacha Leviatán")

    def espadas_caos(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 500
        multiplicador = 0.8
        dano = int(base + self.ataque * multiplicador)
        mensaje = CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Espadas del Caos", especial=True)
        if random.random() < 0.4:
            quemadura_msg = CombatLogic.aplicar_quemadura(enemigo)
            mensaje += f"\n{quemadura_msg}"
        return mensaje

    def ira_espartano(self):
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        self.turnos_estado["incremento_ataque"] = 4
        self.ataque = int(self.ataque * 1.6)
        return "Modo Espartano activado: ¡Ataque incrementado en 60% por 4 turnos!"

    def espada_olimpo(self, enemigo):
        if not self.habilidad_disponible:
            return "¡La habilidad definitiva no está disponible!"
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 1800
        multiplicador = 1.8
        dano = int(base + self.ataque * multiplicador)
        self.habilidad_disponible = False
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Ira de Kratos", definitiva=True)

    def defensa_habilidad_1(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("guardia_olimpica")
        self.turnos_estado["guardia_olimpica"] = 2
        return f"Guardia Olímpica: Defensa incrementada en 30% ({cantidad}) este turno."

    def defensa_habilidad_2(self):
        cantidad = int(self.defensa_max * 0.7)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("escudo_aegis")
        self.turnos_estado["escudo_aegis"] = 2
        return f"Escudo de Aegis: Defensa incrementada en 70% ({cantidad}) este turno."

    def defensa_buff(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("buff_defensa")
        self.turnos_estado["buff_defensa"] = 6
        return f"Piel de Gigante: Defensa aumentada un 30% ({cantidad})."

    def defensa_esquive(self):
        self.estados.append("esquive")
        self.turnos_estado["esquive"] = 2
        return "Reflejo Divino: ¡Tienes 22% de probabilidad de esquivar el próximo ataque!"

    def energia_carga(self):
        cargar = int(self.energia_max * 0.37)
        self.energia = min(self.energia + cargar, self.energia_max)
        return f"Furia Rúnica: ¡Has cargado {cargar} puntos de energía!"

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
    def nombre_defensa_1(self): return "Guardia Olímpica"
    def nombre_defensa_2(self): return "Escudo de Aegis"
    def nombre_defensa_buff(self): return "Piel de Gigante"
    def nombre_defensa_esquive(self): return "Reflejo Divino"
    def nombre_energia_carga(self): return "Furia Rúnica"
    def nombre_energia_carga_max(self): return "Visión de Apolo"