# Archivo para la clase del boss IT
# Importaciones necesarias y dependencias
from Logic_All.logic_combat import CombatLogic
from PIL import Image
import random

# Clase para el boss IT
class BossIT:
    def __init__(self):
        # Atributos básicos del boss
        self.nombre = "🎭 IT Boss"
        self.imagen = "Image/it.png"
        self.vida_max = 65000
        self.vida = 65000
        self.energia_max = 35000
        self.energia = 35000
        self.defensa_max = 10000
        self.defensa = 10000
        self.ataque = 1000
        # Estados y habilidades
        self.estados = []
        self.turnos_estado = {}
        self.habilidad_disponible = True
        # Contadores de objetos
        self.usos_pocion = 0
        self.usos_antidoto = 0
        self.usos_hiper_pocion = 0
        self.usos_elixir = 0
        # Mecánica de recuperación de energía automática
        self.recuperando_energia = False
        self.turnos_recuperacion = 0

# Procesar estados
    def procesar_estados(self):
        to_remove = []
        mensajes = []
        # Procesar recuperación de energía si está en ese estado
        if self.recuperando_energia:
            self.turnos_recuperacion -= 1
            mensajes.append(f"{self.nombre} está recuperando energía... quedan {self.turnos_recuperacion} turno(s) sin poder moverse.")
            # Cuando termina la recuperación
            if self.turnos_recuperacion <= 0:
                self.recuperando_energia = False
                self.energia = self.energia_max
                # Aplica boost de ataque y defensa
                self.estados.append("boss_boost_ataque")
                self.turnos_estado["boss_boost_ataque"] = 4
                self.ataque = int(self.ataque * 1.5)
                self.defensa = int(self.defensa * 1.2)
                mensajes.append(f"{self.nombre} ha recuperado toda la energía y obtiene un boost de +50% ataque y +20% defensa durante 4 turnos!")
            return mensajes
        
        # Procesar otros estados
        for estado in list(self.turnos_estado.keys()):
            self.turnos_estado[estado] -= 1
            # Finaliza boost de ataque y defensa
            if estado == "boss_boost_ataque" and self.turnos_estado[estado] == 0:
                self.ataque = int(self.ataque / 1.5)
                self.defensa = int(self.defensa / 1.2)
                mensajes.append(f"{self.nombre} termina el boost de ataque y defensa.")
            # Elimina estado si se acabaron los turnos
            if self.turnos_estado[estado] <= 0:
                to_remove.append(estado)
        # Elimina los estados que terminaron
        for estado in to_remove:
            if estado in self.estados:
                self.estados.remove(estado)
            self.turnos_estado.pop(estado)
        return mensajes
    
# Verificación de energía para ataques
    def verificar_energia_boss(self, energia_necesaria):
        # Verifica si el boss tiene suficiente energía para actuar
        if self.energia < energia_necesaria and not self.recuperando_energia:
            self.recuperando_energia = True
            self.turnos_recuperacion = 4
            return False, f"{self.nombre} se ha quedado sin energía y estará inactivo 4 turnos para recuperarse!"
        # Verifica si está en recuperación de energía
        if self.recuperando_energia:
            return False, f"{self.nombre} está en recuperación de energía y no puede realizar acciones."
        return True, ""

# Ataques y habilidades
    def ataque_normal(self, enemigo):
        # Verifica y consume energía
        ok, msg = self.verificar_energia_boss(self.energia_max * 0.05)
        # Si no puede atacar, retorna el mensaje
        if not ok: return msg
        # Realiza el ataque normal
        dano = int(120 + self.ataque * 0.6)
        # Consume energía
        self.energia -= self.energia_max * 0.05
        return CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Risa Demoníaca", especial=False, definitiva=False)

    def ataque_especial(self, enemigo):
        # Verifica y consume energía
        ok, msg = self.verificar_energia_boss(self.energia_max * 0.12)
        # SI NO puede atacar, retorna el mensaje
        if not ok: return msg
        # Realiza el ataque especial
        dano = int(140 + self.ataque * 0.5)
        # Consume energía
        self.energia -= self.energia_max * 0.12
        # Aplica veneno
        veneno_msg = CombatLogic.aplicar_veneno(enemigo, turnos=3, daño_por_turno=200)
        mensaje = CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Globo Envenenado", especial=True)
        return mensaje + f"\n{veneno_msg}"

    def habilidad_definitiva(self, enemigo):
        # Verifica y consume energía
        ok, msg = self.verificar_energia_boss(self.energia_max * 0.5)
        #  Si no puede atacar, retorna el mensaje
        if not ok: return msg
        # Verifica si la habilidad definitiva está disponible
        if not self.habilidad_disponible:
            return "¡La habilidad definitiva no está disponible!"
        # Realiza la habilidad definitiva
        dano = int(2500 + self.ataque * 3.0)
        # Consume energía y desactiva la habilidad definitiva
        self.energia -= self.energia_max * 0.5
        self.habilidad_disponible = False
        # Aplica efectos adicionales
        efecto_msgs = []
        import random
        # Aplica quemadura y veneno con 50% de probabilidad cada uno
        if random.random() < 0.5:
            efecto_msgs.append(CombatLogic.aplicar_quemadura(enemigo, turnos=3))
        if random.random() < 0.5:
            efecto_msgs.append(CombatLogic.aplicar_veneno(enemigo, turnos=3, daño_por_turno=250))
        mensaje = CombatLogic.realizar_ataque(self, enemigo, dano, nombre_ataque="Transmorfismo Eldritch", definitiva=True)
        return mensaje + ("\n" + "\n".join(efecto_msgs) if efecto_msgs else "")

# Incremento de ataque
    def incremento(self, enemigo):
        # Verifica y consume energía
        ok, msg = self.verificar_energia_boss(self.energia_max * 0.05)
        # si no puede atacar, retorna el mensaje
        if not ok: return msg
        # Aplica el incremento
        if "incremento_ataque" not in self.estados:
            self.estados.append("incremento_ataque")
        # Dura 8 turnos y aumenta ataque en 40%
        self.turnos_estado["incremento_ataque"] = 8
        self.ataque = int(self.ataque * 1.4)
        # Consume energía
        self.energia -= self.energia_max * 0.05
        # Aplica estuneo al enemigo
        if "estuneo" not in enemigo.estados:
            enemigo.estados.append("estuneo")
        enemigo.turnos_estado["estuneo"] = 2
        return "Luces de la Muerte: ¡Terror psicológico activado (ataque +40% por 8 turnos) y el jugador queda ESTUNEADO por 2 turnos!"

    # Defensa y energía igual a los personajes
    def defensa_habilidad_1(self):
        # Verifica y consume energía
        ok, msg = CombatLogic.consumir_energia_accion(self, "defensa")
        # si no hay energía suficiente, retorna el mensaje
        if not ok: return msg
        # sube la defensa en 30% por 2 turnos
        cantidad = int(self.defensa_max * 0.3)
        # Aplica el aumento de defensa
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("espectro_temporal")
        self.turnos_estado["espectro_temporal"] = 2
        return f"Espectro Temporal: Defensa incrementada en 30% ({cantidad}) este turno."

    def defensa_habilidad_2(self):
        # Verifica y consume energía
        ok, msg = CombatLogic.consumir_energia_accion(self, "defensa_absoluta")
        # si no hay energía suficiente, retorna el mensaje
        if not ok: return msg
        # sube la defensa en 70% por 2 turnos
        cantidad = int(self.defensa_max * 0.7)
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        # Aplica el aumento de defensa
        self.estados.append("resistencia_sobrenatural")
        self.turnos_estado["resistencia_sobrenatural"] = 2
        return f"Resistencia Sobrenatural: Defensa incrementada en 70% ({cantidad}) este turno."

    def defensa_buff(self):
        # Verifica y consume energía
        cantidad = int(self.defensa_max * 0.3)
        # Aplica el aumento de defensa
        self.defensa = min(self.defensa + cantidad, self.defensa_max)
        self.estados.append("buff_defensa")
        self.turnos_estado["buff_defensa"] = 10
        return f"Mente Indestructible: Defensa aumentada un 30% ({cantidad}) por 10 turnos."

    def defensa_esquive(self):
        # Verifica y consume energía
        self.estados.append("esquive")
        # Dura 2 turnos con 40% de esquive
        self.turnos_estado["esquive"] = 2
        return "Ilusiones: ¡Tienes un 40% de probabilidad de esquivar el próximo ataque!"

    def energia_carga(self):
        # Verifica y consume energía
        cargar = int(self.energia_max * 0.65)
        # Carga energía
        self.energia = min(self.energia + cargar, self.energia_max)
        return f"Ritual Cósmico: ¡IT ha cargado {cargar} puntos de energía!"

    def energia_carga_max(self):
        # Verifica y consume energía
        self.estados.append("recarga_maxima")
        # Dura 4 turnos
        self.turnos_estado["recarga_maxima"] = 4
        self.energia = self.energia_max
        return CombatLogic.recarga_maxima(self)

    # Nombres de ataques y habilidades
    def nombre_ataque_normal(self): return "Risa Demoníaca"
    def nombre_ataque_especial(self): return "Globo Envenenado"
    def nombre_habilidad_definitiva(self): return "Transmorfismo Eldritch"
    def nombre_incremento(self): return "Luces de la Muerte"
    def nombre_defensa_1(self): return "Espectro Temporal"
    def nombre_defensa_2(self): return "Resistencia Sobrenatural"
    def nombre_defensa_buff(self): return "Mente Indestructible"
    def nombre_defensa_esquive(self): return "Ilusiones"
    def nombre_energia_carga(self): return "Ritual Cósmico"
    def nombre_energia_carga_max(self): return "Invernación"