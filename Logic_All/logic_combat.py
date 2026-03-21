# importaciones necesarias
import random


# Clase de lógica de combate
class CombatLogic:
    # Realiza un ataque considerando energía, defensa y estados
    @staticmethod
    def realizar_ataque(atacante, defensor, dano, nombre_ataque="", especial=False, definitiva=False):
        # Gestión de energía
        if definitiva:
            # gasto de energía del 50%
            porcentaje = 0.5
            # Verifica si hay suficiente energía
            if atacante.energia < atacante.energia_max * porcentaje:
                return f"{atacante.nombre} no tiene suficiente energía para usar la habilidad definitiva."
            atacante.energia -= atacante.energia_max * porcentaje
            # Defensa reducida en 50%
            def_msg = f"{defensor.nombre} ¡defensa destruida!"
        # Ataque especial o normal
        elif especial:
            # gasto de energía del 12%
            porcentaje = 0.12
            # Verifica si hay suficiente energía
            if atacante.energia < atacante.energia_max * porcentaje:
                return f"{atacante.nombre} no tiene suficiente energía para ataque especial."
            # energía consumida
            atacante.energia -= atacante.energia_max * porcentaje
            # energía consumida, reduce defensa en 25%
            defensa_reducida = int(defensor.defensa * 0.25)
            defensor.defensa = max(0, defensor.defensa - defensa_reducida)
            def_msg = f"{defensor.nombre} perdió {defensa_reducida} de defensa por ataque especial."
        # Ataque normal
        else:
            # gasto de energía del 5%
            porcentaje = 0.05
            # Verifica si hay suficiente energía
            if atacante.energia < atacante.energia_max * porcentaje:
                return f"{atacante.nombre} no tiene suficiente energía para ataque normal."
            # energia consumida
            atacante.energia -= atacante.energia_max * porcentaje
            # energía consumida, reduce defensa en 25%
            defensa_reducida = int(defensor.defensa * 0.25)
            # defensa reducida
            defensor.defensa = max(0, defensor.defensa - defensa_reducida)
            def_msg = f"{defensor.nombre} perdió {defensa_reducida} de defensa por ataque normal."
        # Cansancio si energía <= 0
        CombatLogic._verificar_cansancio(atacante)
        # Calcula el daño recibido
        recibido = CombatLogic.recibir_dano(defensor, dano)
        # Mensaje del ataque
        desc = f"{atacante.nombre} usó {nombre_ataque} y causó {recibido:.1f} de daño a {defensor.nombre}. {def_msg}"
        if especial:
            desc += " ¡Ataque especial!"
        if definitiva:
            desc += " ¡Ataque definitivo!"
        return desc

    # Verifica y consume energía para acciones de defensa
    @staticmethod
    def consumir_energia_accion(personaje, tipo):
        # tipo: "defensa", "defensa_absoluta"
        if tipo == "defensa":
            porcentaje = 0.05
            # Verifica si hay suficiente energía
            if personaje.energia < personaje.energia_max * porcentaje:
                return False, "No tienes suficiente energía para defensa."
            personaje.energia -= personaje.energia_max * porcentaje
        # defensa absoluta
        elif tipo == "defensa_absoluta":
            # 20% de energía
            porcentaje = 0.20
            # Verifica si hay suficiente energía
            if personaje.energia < personaje.energia_max * porcentaje:
                return False, "No tienes suficiente energía para defensa absoluta."
            personaje.energia -= personaje.energia_max * porcentaje
        # Verificar cansancio
        CombatLogic._verificar_cansancio(personaje)
        return True, None

    # Verifica y aplica cansancio si la energía es 0 o menos
    @staticmethod
    def _verificar_cansancio(personaje):
        # Aplica cansancio si la energía es 0 o menos
        if personaje.energia <= 0 and "cansancio" not in personaje.estados:
            personaje.energia = 0
            # Aplica el estado de cansancio
            personaje.estados.append("cansancio")
            personaje.turnos_estado["cansancio"] = 2
            # Reduce ataque y defensa en 20%
            personaje.ataque = int(personaje.ataque * 0.8)
            personaje.defensa = int(personaje.defensa * 0.8)

    # Calcula el daño recibido considerando defensa y estados
    @staticmethod
    def recibir_dano(personaje, cantidad):
        # Calcula el daño considerando defensa y estados
        bonus = 1.1 if "estuneo" in personaje.estados else 1.0
        # daño mínimo de 10
        daño = max(10, cantidad * bonus - (personaje.defensa / 15))
        personaje.vida = max(0, personaje.vida - daño)
        personaje.defensa = max(0, personaje.defensa)
        # Defensa a 0, estunea
        if personaje.defensa == 0 and "estuneo" not in personaje.estados:
            CombatLogic.aplicar_estado(personaje, "estuneo")
        return daño

    # Aplica un estado a un personaje
    @staticmethod
    def aplicar_estado(personaje, estado):
        duraciones = {
            "paralisis": 4, "incremento_ataque": 6, "veneno": 6, "buff_defensa": 6,
            "cura_estado": 4, "recarga_maxima": 4, "esquive": 2, "proteccion": 2,
            "estuneo": 2, "quemadura": 6, "mascara_maligna": 2, "resistencia_sobrenatural":2,
            "cansancio": 2,
        }
        duracion = duraciones.get(estado, 4)
        # Aplica el estado si no está ya presente
        if estado not in personaje.estados:
            personaje.estados.append(estado)
            personaje.turnos_estado[estado] = duracion
            return f"{personaje.nombre} ahora sufre el estado: {estado}."
        return f"{personaje.nombre} ya tiene el estado: {estado}."

    # Aplica paralisis, quemadura o veneno
    @staticmethod
    def aplicar_paralisis(personaje, turnos=2):
        turnos *= 2
        # Aplica paralisis
        if "paralisis" not in personaje.estados:
            personaje.estados.append("paralisis")
            # Dura el doble de turnos
            personaje.turnos_estado["paralisis"] = turnos
            return f"{personaje.nombre} ha sido paralizado."
        return f"{personaje.nombre} ya está paralizado."

    # Aplica quemadura o veneno
    @staticmethod
    def aplicar_quemadura(personaje, turnos=3):
        turnos *= 2
        # Aplica quemadura
        if "quemadura" not in personaje.estados:
            personaje.estados.append("quemadura")
            personaje.turnos_estado["quemadura"] = turnos
            # Reduce defensa en 20%
            personaje.defensa = int(personaje.defensa * 0.8)
            personaje.defensa_quemadura_reducida = True
            # Mensaje de quemadura
            return f"{personaje.nombre} ha recibido quemadura: sufrirá daño por {turnos} turnos y su defensa se redujo un 20%."
        # Mensaje si ya tiene quemadura
        return f"{personaje.nombre} ya está bajo el efecto de quemadura."

    # aplica veneno
    @staticmethod
    def aplicar_veneno(personaje, turnos=3, daño_por_turno=50):
        turnos *= 2
        # Aplica veneno
        if "veneno" not in personaje.estados:
            personaje.estados.append("veneno")
            personaje.turnos_estado["veneno"] = turnos
            # daño por turno del veneno
            personaje.daño_veneno = daño_por_turno
            return f"{personaje.nombre} ha sido envenenado."
        return f"{personaje.nombre} ya está envenenado."

    # Verifica si el personaje está paralizado
    @staticmethod
    def verificar_paralisis(personaje):
        # si está paralizado, hay 50% de probabilidad de no actuar
        if "paralisis" in personaje.estados:
            # 50% de probabilidad de no actuar
            if random.random() < 0.5:
                return True, f"{personaje.nombre} está paralizado y no puede moverse este turno."
        return False, ""

    # Realiza una recarga máxima de energía
    @staticmethod
    def recarga_maxima(personaje):
        # Llena la energía y aplica el estado de recarga máxima
        personaje.energia = personaje.energia_max
        personaje.estados.append("recarga_maxima")
        personaje.turnos_estado["recarga_maxima"] = 4
        personaje.recarga_maxima_turnos = 4
        # energía extra por turno
        personaje.recarga_maxima_bonus = personaje.energia_max // 6
        personaje.recarga_maxima_bloqueo = True
        return f"{personaje.nombre} realizó una recarga máxima. Energía al máximo y recuperará energía extra por 4 turnos, pero pierde el turno actual."

    # Procesa los estados al final del turno
    @staticmethod
    def procesar_estados(personaje):
        eliminar = []
        mensajes = []
        # Procesa cada estado
        for estado in list(personaje.estados):
            personaje.turnos_estado[estado] -= 1
            # Efectos por estado
            if estado == "veneno":
                # aplica daño por veneno
                personaje.vida = max(0, personaje.vida - getattr(personaje, "daño_veneno", 0))
                mensajes.append(f"{personaje.nombre} sufre {getattr(personaje, 'daño_veneno', 0)} de daño por veneno.")
            if estado == "quemadura":
                # aplica daño por quemadura
                quemadura_damage = int(personaje.vida_max * 0.03)
                personaje.vida = max(0, personaje.vida - quemadura_damage)
                mensajes.append(f"{personaje.nombre} sufre {quemadura_damage} de daño por quemadura.")
            if estado == "recarga_maxima":
                # aplica recarga máxima
                if personaje.recarga_maxima_turnos > 0:
                    personaje.energia = min(personaje.energia_max, personaje.energia + personaje.recarga_maxima_bonus)
                    mensajes.append(f"{personaje.nombre} recupera {personaje.recarga_maxima_bonus} de energía extra por recarga máxima.")
                    # decrementa turnos restantes
                    personaje.recarga_maxima_turnos -= 1
                if personaje.recarga_maxima_bloqueo:
                    personaje.recarga_maxima_bloqueo = False
            # bloquea el turno actual
            if estado == "estuneo" and personaje.turnos_estado[estado] == 1:
                defensa_recuperada = int(personaje.defensa_max * 0.10)
                personaje.defensa = min(personaje.defensa + defensa_recuperada, personaje.defensa_max)
                mensajes.append(f"{personaje.nombre} recupera {defensa_recuperada} puntos de defensa tras estuneo.")
            # elimina el estado si los turnos llegan a 0
            if estado == "cansancio" and personaje.turnos_estado[estado] == 0:
                # restaura ataque y defensa
                personaje.ataque = int(personaje.ataque / 0.8)
                personaje.defensa = int(personaje.defensa / 0.8)
                mensajes.append(f"{personaje.nombre} ya no está cansado, se restauró ataque y defensa.")
            # elimina el estado si los turnos llegan a 0
            if personaje.turnos_estado[estado] <= 0:
                eliminar.append(estado)
        # Elimina los estados expirados
        for e in eliminar:
            # elimina el estado
            if e in personaje.estados:
                personaje.estados.remove(e)
                del personaje.turnos_estado[e]
                # efectos al eliminar ciertos estados
                if e == "quemadura":
                    if hasattr(personaje, "defensa_quemadura_reducida") and personaje.defensa_quemadura_reducida:
                        personaje.defensa = int(personaje.defensa / 0.8)
                        personaje.defensa_quemadura_reducida = False
                # efectos al eliminar recarga máxima
                if e == "recarga_maxima":
                    # elimina atributos relacionados
                    if hasattr(personaje, "recarga_maxima_turnos"):
                        del personaje.recarga_maxima_turnos
                    if hasattr(personaje, "recarga_maxima_bonus"):
                        del personaje.recarga_maxima_bonus
                    if hasattr(personaje, "recarga_maxima_bloqueo"):
                        del personaje.recarga_maxima_bloqueo
                mensajes.append(f"{personaje.nombre} ya no sufre el estado: {e}.")
        return mensajes

    # Verifica si el personaje está en recarga máxima y bloqueado
    @staticmethod
    def verificar_recarga_maxima_bloqueo(personaje):
        return getattr(personaje, "recarga_maxima_bloqueo", False)

    # Incrementa el ataque de un personaje por varios turnos
    @staticmethod
    # incrementa el ataque de un personaje por varios turnos
    def incrementar_ataque(personaje, turnos=2, bonus=1.5):
        turnos *= 2
        # Aplica el aumento de ataque
        personaje.estados.append("ataque_incrementado")
        personaje.turnos_estado["ataque_incrementado"] = turnos
        personaje.bonus_ataque = bonus
        return f"{personaje.nombre} incrementó su ataque por {turnos} turnos."