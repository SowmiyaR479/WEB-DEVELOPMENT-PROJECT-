from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = "hospital_advanced_key"

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Basic Info
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")

        # Contact Info
        phone = request.form.get("phone")
        address = request.form.get("address")

        # Medical Info
        blood = request.form.get("blood")
        disease = request.form.get("disease")
        symptoms = request.form.get("symptoms")
        doctor = request.form.get("doctor")
        date = request.form.get("date")

        # Emergency
        emergency = request.form.get("emergency")

        # 🔍 Validations
        if not name or len(name) < 3:
            flash("Name must be at least 3 characters!", "error")
            return redirect(url_for("home"))

        if not age or not age.isdigit():
            flash("Invalid age!", "error")
            return redirect(url_for("home"))

        if not re.match(r"^[0-9]{10}$", phone):
            flash("Phone must be 10 digits!", "error")
            return redirect(url_for("home"))

        if not disease:
            flash("Disease cannot be empty!", "error")
            return redirect(url_for("home"))

        flash("Patient record saved successfully!", "success")

        return render_template("result.html",
            name=name, age=age, gender=gender,
            phone=phone, address=address,
            blood=blood, disease=disease,
            symptoms=symptoms, doctor=doctor,
            date=date, emergency=emergency
        )

    except Exception as e:
        flash("Something went wrong!", "error")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)