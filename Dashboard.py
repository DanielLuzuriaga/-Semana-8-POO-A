import os
import subprocess
import platform

class Dashboard:
    """
    Dashboard interactivo en consola para gestionar scripts Python.
    Implementa Programación Orientada a Objetos y validación defensiva.
    """

    def __init__(self):
        self.ruta_base = os.path.dirname(__file__)
        self.unidades = {
            '1': 'Unidad 1',
            '2': 'Unidad 2'
        }

    # ---------------- UTILIDADES ----------------
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def entrada_valida(self, entrada, opciones_validas):
        """
        Valida defensivamente la entrada del usuario.
        - Elimina espacios
        - Rechaza cadenas largas (errores del IDE)
        - Verifica que esté dentro de las opciones permitidas
        """
        entrada = entrada.strip()
        if len(entrada) > 2:
            return None
        if entrada not in opciones_validas:
            return None
        return entrada

    # ---------------- MENÚ PRINCIPAL ----------------
    def mostrar_menu_principal(self):
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

            if opcion is None:
                input("⚠ Entrada inválida. Presione Enter...")
                continue

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

    # ---------------- UNIDADES ----------------
    def menu_unidades(self):
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

            ruta = os.path.join(self.ruta_base, self.unidades[opcion])
            self.menu_subcarpetas(ruta)

    # ---------------- SUBCARPETAS ----------------
    def menu_subcarpetas(self, ruta_unidad):
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

    # ---------------- SCRIPTS ----------------
    def menu_scripts(self, ruta):
        scripts = [f.name for f in os.scandir(ruta) if f.is_file() and f.name.endswith('.py')]
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

    # ---------------- FUNCIONALIDADES ----------------
    def listar_todos_los_scripts(self):
        self.limpiar_pantalla()
        print("📄 TODOS LOS SCRIPTS\n")

        for root, _, files in os.walk(self.ruta_base):
            for file in files:
                if file.endswith('.py'):
                    print(os.path.join(root, file))

        input("\nPresione Enter para regresar...")

    def buscar_script(self):
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
        self.limpiar_pantalla()
        print("💻 INFORMACIÓN DEL SISTEMA\n")
        print(f"Sistema Operativo: {platform.system()}")
        print(f"Versión: {platform.version()}")
        print(f"Arquitectura: {platform.architecture()[0]}")
        input("\nPresione Enter...")

    def mostrar_ayuda(self):
        self.limpiar_pantalla()
        print("❓ AYUDA\n")
        print("Este dashboard permite navegar, buscar y ejecutar scripts Python.")
        print("Todas las entradas están validadas para evitar errores.")
        input("\nPresione Enter...")

    # ---------------- EJECUCIÓN DE SCRIPTS ----------------
    def ejecutar_script(self, ruta_script):
        try:
            if os.name == 'nt':
                subprocess.Popen(['cmd', '/k', 'python', ruta_script])
            else:
                subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
        except Exception as e:
            input(f"❌ Error al ejecutar: {e}")

    def ejecutar(self):
        self.mostrar_menu_principal()


# ---------------- PUNTO DE ENTRADA ----------------
if __name__ == "__main__":
    Dashboard().ejecutar()
