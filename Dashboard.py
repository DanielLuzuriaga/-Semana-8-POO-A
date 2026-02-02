import os
import subprocess
import platform

class Dashboard:
    """
    Clase Dashboard
    =================
    Esta clase implementa un sistema de menú interactivo en consola
    para la gestión de scripts Python.
    
    Con los cambios realizados se:

    ✔ Aplica Programación Orientada a Objetos (POO)
    ✔ Se implementa validación defensiva (mejor práctica)
    ✔ Se interactúa con el sistema operativo
    ✔ Permite navegación, búsqueda y ejecución de scripts
    """

    def __init__(self):
        """
        Constructor de la clase.

        - Inicializa la ruta base del proyecto usando __file__
        - Define las unidades disponibles
        - Centraliza la configuración inicial del sistema
        """
        self.ruta_base = os.path.dirname(__file__)  # Ruta donde se ejecuta el dashboard
        self.unidades = {
            '1': 'Unidad 1',
            '2': 'Unidad 2'
        }

    # ==========================================================
    # MÉTODOS DE UTILIDAD GENERAL
    # ==========================================================

    def limpiar_pantalla(self):
        """
        Limpia la consola según el sistema operativo.

        ✔ Mejora la experiencia del usuario
        ✔ Hace el menú más claro y ordenado
        ✔ Aplica portabilidad (Windows / Linux)
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def entrada_valida(self, entrada, opciones_validas):
        """
        Valida defensivamente cualquier entrada del usuario.

        ¿Qué hace esta validación?
        - Elimina espacios en blanco
        - Evita entradas largas (errores del IDE)
        - Comprueba que la opción esté permitida

        ✔ Evita fallos del programa
        ✔ Implementa la mejor práctica: NO confiar en la entrada del usuario
        """
        entrada = entrada.strip()

        # Evita que comandos largos (ejecución automática del IDE) rompan el menú
        if len(entrada) > 2:
            return None

        # Verifica que la opción esté dentro del conjunto permitido
        if entrada not in opciones_validas:
            return None

        return entrada

    # ==========================================================
    # MENÚ PRINCIPAL
    # ==========================================================

    def mostrar_menu_principal(self):
        """
        Muestra el menú principal del sistema.

        ✔ Controla el flujo general del programa
        ✔ Redirige a las diferentes funcionalidades
        ✔ Usa validación defensiva
        """
        while True:
            self.limpiar_pantalla()
            print("🧭 DASHBOARD DE SCRIPTS\n")
            print("1. Navegar por Unidades")
            print("2. Listar todos los scripts")
            print("3. Buscar un script")
            print("4. Información del sistema")
            print("5. Ayuda")
            print("0. Salir")

            print("\n⚠ Ingrese SOLO el número de la opción")

            opcion = self.entrada_valida(
                input("Seleccione una opción: "),
                ['1', '2', '3', '4', '5', '0']
            )

            # Validación defensiva del menú principal
            if opcion is None:
                input("⚠ Entrada inválida. Presione Enter...")
                continue

            # Enrutamiento de opciones
            if opcion == '1':
                self.menu_unidades()
            elif opcion == '2':
                self.listar_todos_los_scripts()
            elif opcion == '3':
                self.buscar_script()
            elif opcion == '4':
                self.info_sistema()
            elif opcion == '5':
                self.mostrar_ayuda()
            elif opcion == '0':
                print("👋 Saliendo del sistema...")
                break

    # ==========================================================
    # MENÚ DE UNIDADES
    # ==========================================================

    def menu_unidades(self):
        """
        Muestra las unidades disponibles.

        ✔ Primer nivel de navegación
        ✔ Permite seleccionar el contexto de trabajo
        """
        while True:
            self.limpiar_pantalla()
            print("📁 UNIDADES\n")

            for key, value in self.unidades.items():
                print(f"{key}. {value}")

            print("0. Regresar")

            opcion = self.entrada_valida(
                input("Seleccione una unidad: "),
                list(self.unidades.keys()) + ['0']
            )

            if opcion is None:
                input("⚠ Entrada inválida...")
                continue

            if opcion == '0':
                break

            # Construye la ruta de la unidad seleccionada
            ruta = os.path.join(self.ruta_base, self.unidades[opcion])
            self.menu_subcarpetas(ruta)

    # ==========================================================
    # MENÚ DE SUBCARPETAS
    # ==========================================================

    def menu_subcarpetas(self, ruta_unidad):
        """
        Muestra las subcarpetas dentro de una unidad.

        ✔ Usa os.scandir para interacción con el sistema de archivos
        ✔ Navegación dinámica
        """
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
        opciones_validas = [str(i) for i in range(1, len(sub_carpetas) + 1)] + ['0']

        while True:
            self.limpiar_pantalla()
            print("📂 SUBCARPETAS\n")

            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i}. {carpeta}")

            print("0. Regresar")

            opcion = self.entrada_valida(
                input("Seleccione una subcarpeta: "),
                opciones_validas
            )

            if opcion is None:
                input("⚠ Entrada inválida...")
                continue

            if opcion == '0':
                break

            idx = int(opcion) - 1
            self.menu_scripts(os.path.join(ruta_unidad, sub_carpetas[idx]))

    # ==========================================================
    # MENÚ DE SCRIPTS
    # ==========================================================

    def menu_scripts(self, ruta):
        """
        Muestra los scripts Python disponibles en una carpeta.

        ✔ Filtra solo archivos .py
        ✔ Permite ejecutar scripts
        """
        scripts = [f.name for f in os.scandir(ruta)
                   if f.is_file() and f.name.endswith('.py')]

        opciones_validas = [str(i) for i in range(1, len(scripts) + 1)] + ['0']

        while True:
            self.limpiar_pantalla()
            print("📜 SCRIPTS\n")

            for i, script in enumerate(scripts, start=1):
                print(f"{i}. {script}")

            print("0. Regresar")

            opcion = self.entrada_valida(
                input("Seleccione un script: "),
                opciones_validas
            )

            if opcion is None:
                input("⚠ Entrada inválida...")
                continue

            if opcion == '0':
                break

            idx = int(opcion) - 1
            self.ejecutar_script(os.path.join(ruta, scripts[idx]))

    # ==========================================================
    # FUNCIONALIDADES ADICIONALES
    # ==========================================================

    def listar_todos_los_scripts(self):
        """
        Lista todos los scripts Python del proyecto.

        ✔ Usa os.walk para recorrido recursivo
        ✔ Permite inspección global del proyecto
        """
        self.limpiar_pantalla()
        print("📄 TODOS LOS SCRIPTS\n")

        for root, _, files in os.walk(self.ruta_base):
            for file in files:
                if file.endswith('.py'):
                    print(os.path.join(root, file))

        input("\nPresione Enter para regresar...")

    def buscar_script(self):
        """
        Permite buscar scripts por nombre.

        ✔ Mejora la usabilidad
        ✔ Evita navegación manual innecesaria
        """
        self.limpiar_pantalla()
        nombre = input("🔎 Ingrese el nombre del script: ").strip().lower()

        if not nombre:
            input("⚠ Nombre inválido...")
            return

        encontrados = []

        for root, _, files in os.walk(self.ruta_base):
            for file in files:
                if nombre in file.lower() and file.endswith('.py'):
                    encontrados.append(os.path.join(root, file))

        if encontrados:
            print("\nScripts encontrados:\n")
            for s in encontrados:
                print(s)
        else:
            print("\n❌ No se encontraron scripts.")

        input("\nPresione Enter...")

    def info_sistema(self):
        """
        Muestra información básica del sistema operativo.

        ✔ Aplica conceptos de Sistemas Operativos
        ✔ Consulta información del entorno de ejecución
        """
        self.limpiar_pantalla()
        print("💻 INFORMACIÓN DEL SISTEMA\n")
        print(f"Sistema Operativo: {platform.system()}")
        print(f"Versión: {platform.version()}")
        print(f"Arquitectura: {platform.architecture()[0]}")
        input("\nPresione Enter...")

    def mostrar_ayuda(self):
        """
        Muestra ayuda básica del dashboard.
        """
        self.limpiar_pantalla()
        print("❓ AYUDA\n")
        print("Este dashboard permite navegar, buscar y ejecutar scripts Python.")
        print("El sistema utiliza validación defensiva para evitar errores.")
        input("\nPresione Enter...")

    # ==========================================================
    # EJECUCIÓN DE SCRIPTS
    # ==========================================================

    def ejecutar_script(self, ruta_script):
        """
        Ejecuta un script Python como proceso independiente.

        ✔ Usa subprocess.Popen
        ✔ No bloquea el dashboard
        ✔ Aplica gestión de procesos del S.O.
        """
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(['cmd', '/k', 'python', ruta_script])
            else:  # Linux / Unix
                subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
        except Exception as e:
            input(f"❌ Error al ejecutar: {e}")

    def ejecutar(self):
        """
        Método principal que inicia el dashboard.
        """
        self.mostrar_menu_principal()


# ==========================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================================
if __name__ == "__main__":
    Dashboard().ejecutar()
