from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

server_process = None
client_process = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start-server")
def start_server():
    global server_process
    if server_process is None:
        server_process = subprocess.Popen(["python", "/Users/josiah/Desktop/Python Projects/Ona Vision/main.py"])
    return redirect(url_for("index"))


@app.route("/start-client")
def start_client():
    global client_process
    if client_process is None:
        client_process = subprocess.Popen(["python", "/Users/josiah/Desktop/Python Projects/Ona Vision/client.py"])
    return redirect(url_for("index"))


@app.route("/stop")
def stop_all():
    global server_process, client_process
    if server_process:
        server_process.terminate()
        server_process = None
    if client_process:
        client_process.terminate()
        client_process = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
