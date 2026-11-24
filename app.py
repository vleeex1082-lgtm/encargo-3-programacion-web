from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "clave-para-el-trabajo-local"

# Esta lista guarda los resultados mientras el servidor está funcionando.
resultados = []
siguiente_id = 1


def guardar_resultado(tipo, titulo, detalle, resultado):
    global siguiente_id

    registro = {
        "id": siguiente_id,
        "kind": tipo,
        "titulo": titulo,
        "detalle": detalle,
        "result": resultado,
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M"),
    }
    resultados.insert(0, registro)
    siguiente_id = siguiente_id + 1
    return registro["id"]


def contar_letras(nombre):
    letras = ""
    for caracter in nombre:
        if caracter.isalpha():
            letras = letras + caracter
    return letras


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio/1", methods=["GET", "POST"])
def exercise_one():
    if request.method == "GET":
        return render_template("ejercicio1.html")

    notas = []
    for numero in range(1, 4):
        dato = request.form.get("nota" + str(numero), "")
        try:
            nota = int(dato)
        except ValueError:
            flash("Las notas deben ser números enteros entre 10 y 70.", "error")
            return render_template("ejercicio1.html"), 400

        if nota < 10 or nota > 70:
            flash("Las notas deben estar entre 10 y 70.", "error")
            return render_template("ejercicio1.html"), 400
        notas.append(nota)

    dato_asistencia = request.form.get("asistencia", "")
    try:
        asistencia = int(dato_asistencia)
    except ValueError:
        flash("La asistencia debe ser un número entre 0 y 100.", "error")
        return render_template("ejercicio1.html"), 400

    if asistencia < 0 or asistencia > 100:
        flash("La asistencia debe estar entre 0 y 100.", "error")
        return render_template("ejercicio1.html"), 400

    promedio = (notas[0] + notas[1] + notas[2]) / 3
    if promedio >= 40 and asistencia >= 75:
        estado = "Aprobado"
    else:
        estado = "Reprobado"

    detalle = "Notas: " + str(notas[0]) + ", " + str(notas[1]) + ", " + str(notas[2])
    detalle = detalle + " · Asistencia: " + str(asistencia) + "%"
    texto_resultado = estado + " · promedio " + str(round(promedio, 1))
    registro_id = guardar_resultado("Ejercicio 1", "Promedio y asistencia", detalle, texto_resultado)
    return redirect(url_for("result", record_id=registro_id))


@app.route("/ejercicio/2", methods=["GET", "POST"])
def exercise_two():
    if request.method == "GET":
        return render_template("ejercicio2.html")

    nombres = [
        request.form.get("nombre1", "").strip(),
        request.form.get("nombre2", "").strip(),
        request.form.get("nombre3", "").strip(),
    ]

    for nombre in nombres:
        if nombre == "" or contar_letras(nombre) == "":
            flash("Escribe tres nombres que contengan letras.", "error")
            return render_template("ejercicio2.html", names=nombres), 400

    if nombres[0].lower() == nombres[1].lower() or nombres[0].lower() == nombres[2].lower() or nombres[1].lower() == nombres[2].lower():
        flash("Los tres nombres deben ser diferentes.", "error")
        return render_template("ejercicio2.html", names=nombres), 400

    largo_mayor = len(contar_letras(nombres[0]))
    for nombre in nombres:
        largo = len(contar_letras(nombre))
        if largo > largo_mayor:
            largo_mayor = largo

    nombres_mas_largos = []
    for nombre in nombres:
        if len(contar_letras(nombre)) == largo_mayor:
            nombres_mas_largos.append(nombre)

    ganador = ", ".join(nombres_mas_largos)
    detalle = "Nombres ingresados: " + ", ".join(nombres)
    texto_resultado = ganador + " · " + str(largo_mayor) + " letras"
    registro_id = guardar_resultado("Ejercicio 2", "Nombre con más letras", detalle, texto_resultado)
    return redirect(url_for("result", record_id=registro_id))


@app.route("/resultado/<int:record_id>")
def result(record_id):
    for registro in resultados:
        if registro["id"] == record_id:
            return render_template("resultado.html", entry=registro)
    abort(404)


@app.route("/historial")
def history():
    return render_template("historial.html", records=resultados)


@app.route("/historial/<int:record_id>/eliminar", methods=["POST"])
def delete_record(record_id):
    for registro in resultados:
        if registro["id"] == record_id:
            resultados.remove(registro)
            flash("Resultado eliminado del historial.", "success")
            return redirect(url_for("history"))
    abort(404)


@app.route("/historial/vaciar", methods=["POST"])
def clear_history():
    resultados.clear()
    flash("Historial vacío.", "success")
    return redirect(url_for("history"))


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)


