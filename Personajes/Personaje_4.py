from Logic_All.logic_combat import CombatLogic
from PIL import Image
from Personajes.Objects import Pocion, HiperPocion, Antidoto, Elixir

# Personaje 4: Terminator
class Terminator:
    def __init__(self):
        self.nombre = "🤖 Terminator"
        self.imagen = "Image/Terminator.jpg"
        self.vida_max = 14000
        self.vida = 14000
        self.energia_max = 16000
        self.energia = 16000
        self.defensa_max = 4000
        self.defensa = 4000
        self.ataque = 1200
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

    def ataque_normal(self, enemigo): return self.rafaga_laser(enemigo)
    def ataque_especial(self, enemigo): return self.golpe_titanio(enemigo)
    def habilidad_definitiva(self, enemigo): return self.exterminio_total(enemigo)
    def incremento(self): return self.sistema_recalibrado()
    def nombre_ataque_normal(self): return "Ráfaga Láser"
    def nombre_ataque_especial(self): return "Golpe Titanio"
    def nombre_habilidad_definitiva(self): return "Exterminio Total"
    def nombre_incremento(self): return "Sistema Recalibrado"

    def rafaga_laser(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 150
        multiplicador = 0.25
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Ráfaga Láser")

    def golpe_titanio(self, enemigo):
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 230
        multiplicador = 0.35
        dano = int(base + self.ataque * multiplicador)
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Golpe Titanio", especial=True)

    def sistema_recalibrado(self):
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        self.turnos_estado["incremento_ataque"] = 4
        self.ataque = int(self.ataque * 1.3)
        return "Sistema Recalibrado: ¡Ataque incrementado en 30% por 4 turnos!"

    def exterminio_total(self, enemigo):
        if not self.habilidad_disponible:
            return "¡La habilidad definitiva no está disponible!"
        paralizado, msg = CombatLogic.verificar_paralisis(self)
        if paralizado: return msg
        base = 900
        multiplicador = 1.0
        dano = int(base + self.ataque * multiplicador)
        self.habilidad_disponible = False
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Exterminio Total", definitiva=True)

    def defensa_habilidad_1(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("escudo_termico")
        self.turnos_estado["escudo_termico"] = 2
        return f"Escudo Térmico: Defensa incrementada en 30% ({cantidad}) este turno."

    def defensa_habilidad_2(self):
        cantidad = int(self.defensa_max * 0.7)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("armadura_absoluta")
        self.turnos_estado["armadura_absoluta"] = 2
        return f"Armadura Absoluta: Defensa incrementada en 70% ({cantidad}) este turno."

    def defensa_buff(self):
        cantidad = int(self.defensa_max * 0.3)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("buff_defensa")
        self.turnos_estado["buff_defensa"] = 6
        return f"Auto-Reparación: Defensa aumentada un 30% ({cantidad})."

    def defensa_esquive(self):
        self.estados.append("esquive")
        self.turnos_estado["esquive"] = 2
        return "Camuflaje Óptico: ¡Tienes 25% de probabilidad de esquivar el próximo ataque!"

    def energia_carga(self):
        cargar = int(self.energia_max * 0.5)
        self.energia = min(self.energia + cargar, self.energia_max)
        return f"Recarga Nuclear: ¡Has cargado {cargar} puntos de energía!"

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
    def nombre_defensa_1(self): return "Escudo Térmico"
    def nombre_defensa_2(self): return "Armadura Absoluta"
    def nombre_defensa_buff(self): return "Auto-Reparación"
    def nombre_defensa_esquive(self): return "Camuflaje Óptico"
    def nombre_energia_carga(self): return "Recarga Nuclear"
    def nombre_energia_carga_max(self): return "Modo Infinito"