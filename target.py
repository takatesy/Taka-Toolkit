from flask import Flask, request, redirect

app = Flask(__name__)

CORRECT_PASSWORD = "sunshine"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == CORRECT_PASSWORD:
            return "<h1>Welcome admin! Login successful.</h1>"
        else:
            return "<h1>Invalid username or password</h1>"
    return '''
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route("/admin")
def admin():
    return "Forbidden", 403

@app.route("/secret")
def secret():
    return "Forbidden", 403

@app.route("/dashboard")
def dashboard():
    return "<h1>Dashboard</h1>", 200

if __name__ == "__main__":
    app.run(port=5000)