HABITOS_BINARIOS = ["comi_sano", "entrene", "medite", "fui_gimnasio"]
HABITOS_EXTRA = ["litros_agua", "peso_actual"]

def normalizar_habits():
    try:
        with open("habits.txt", "r") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print("El archivo habits.txt no existe. Nada que normalizar.")
        return

    lineas_nuevas = []

    for linea in lineas:
        partes = linea.strip().split(";")
        fecha = partes[0]

        valores = {}
        for p in partes[1:]:
            if ":" in p:
                k, v = p.split(":", 1)
                valores[k] = v

        # Asegurarse que todas las claves estén presentes
        for hab in HABITOS_BINARIOS + HABITOS_EXTRA:
            if hab not in valores:
                valores[hab] = "0"

        # Reconstruir la línea normalizada
        nueva_linea = fecha + ";" + ";".join(f"{k}:{valores[k]}" for k in HABITOS_BINARIOS + HABITOS_EXTRA) + "\n"
        lineas_nuevas.append(nueva_linea)

    # Sobrescribir el archivo con las líneas normalizadas
    with open("habits.txt", "w") as f:
        f.writelines(lineas_nuevas)

    print("Archivo habits.txt normalizado correctamente.")

if __name__ == "__main__":
    normalizar_habits()
