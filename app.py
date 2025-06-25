from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import matplotlib
matplotlib.use('Agg')  # Backend para servidores sin GUI
import matplotlib.pyplot as plt
import os
import random

app = Flask(__name__)

# Habitos que vamos a trackear
HABITOS_BINARIOS = ["comi_sano", "entrene", "medite", "fui_gimnasio"]
HABITOS_EXTRA = ["litros_agua", "peso_actual"]

# Frases motivadoras
FRASES = [
    "Cada día es una nueva oportunidad para mejorar.",
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "No esperes a que las condiciones sean perfectas para comenzar.",
    "La disciplina es el puente entre metas y logros.",
    "El progreso, no la perfección, es lo que importa.",
    "Hazlo con pasión o no lo hagas en absoluto.",
    "El único límite eres tú mismo.",
    "La constancia transforma lo imposible en posible.",
    "Cree en ti y todo será posible.",
    "Tus hábitos definen tu futuro.",
    "Pequeños cambios hacen grandes diferencias."
]

@app.route("/")
def index():
    frase = random.choice(FRASES)
    return render_template("index.html", frase=frase)

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        hoy = date.today().isoformat()

        entradas = []

        # Hábitos binarios: sí/no
        for hab in HABITOS_BINARIOS:
            valor = request.form.get(hab, "0")
            entradas.append(f"{hab}:{valor}")

        # Hábitos extra: agua y peso
        for hab in HABITOS_EXTRA:
            valor = request.form.get(hab, "0")
            entradas.append(f"{hab}:{valor}")

        linea = f"{hoy};" + ";".join(entradas) + "\n"

        with open("habits.txt", "a") as archivo:
            archivo.write(linea)

        return redirect(url_for("index"))

    return render_template("register.html", habitos_bin=HABITOS_BINARIOS, habitos_extra=HABITOS_EXTRA)

@app.route("/estadisticas")
def estadisticas():
    if not os.path.exists("habits.txt"):
        return render_template("stats.html", dias=[], racha=0, fechas_completas=[])

    with open("habits.txt", "r") as archivo:
        lineas = archivo.readlines()

    fechas = []
    cumplidos = []
    racha = 0
    dias_ordenados = []

    for linea in lineas:
        partes = linea.strip().split(";")
        fecha = partes[0]
        valores = {p.split(":")[0]: p.split(":")[1] for p in partes[1:]}

        binarios_cumplidos = [int(valores.get(h, "0")) for h in HABITOS_BINARIOS]
        total = sum(binarios_cumplidos)

        fechas.append(fecha)
        cumplidos.append(total)
        dias_ordenados.append({"fecha": fecha, "valores": valores})

    for dia in reversed(dias_ordenados):
        binarios = [int(dia["valores"].get(h, "0")) for h in HABITOS_BINARIOS]
        if all(binarios):
            racha += 1
        else:
            break

    fechas_completas = [dia["fecha"] for dia in dias_ordenados if all(int(dia["valores"].get(h, "0")) for h in HABITOS_BINARIOS)]

    plt.figure(figsize=(8, 4))
    plt.plot(fechas, cumplidos, marker='o', color="#0077b6")
    plt.ylim(0, len(HABITOS_BINARIOS))
    plt.title("Progreso de hábitos")
    plt.ylabel("Hábitos cumplidos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/grafica.png")
    plt.close()

    return render_template("stats.html", dias=dias_ordenados, racha=racha, fechas_completas=fechas_completas)

@app.route("/reset")
def reset():
    if os.path.exists("habits.txt"):
        os.remove("habits.txt")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
