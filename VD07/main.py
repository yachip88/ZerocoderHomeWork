from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "homework-secret"

user = {
    "name": "Артем",
    "email": "artem@example.com",
    "password": "1234",
}


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form.get("email") == user["email"] and request.form.get("password") == user["password"]:
            session["user"] = user["email"]
            return redirect(url_for("profile"))
        error = "Неверная почта или пароль"
    return render_template("login.html", error=error)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        user["name"] = request.form.get("name") or user["name"]
        user["email"] = request.form.get("email") or user["email"]
        if request.form.get("password"):
            user["password"] = request.form.get("password")
        session["user"] = user["email"]
    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
