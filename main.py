from flask import Flask, render_template, send_from_directory, request
import os
import requests
import smtplib


app = Flask(__name__)
app.secret_key = f"{os.environ['APP_KEY']}"
app.config["CLIENT_PDF"] ="static/files"

my_email = f"{os.environ['SEND_FROM_EMAIL']}"
password = f"{os.environ['SEND_FROM_EMAIL_PASSWORD']}"

quote = "Building a successful program is a challenge. I am highly energetic in code writing, problem solving and learning."


@app.route("/", methods=["GET", "POST"])
def main_page():
 return render_template("index.html", quote=quote)

@app.route("/files" , methods=['GET', 'POST'])
def circum_vitae():
    return send_from_directory(app.config["CLIENT_PDF"], path="CVMihaNovak.pdf", as_attachment=True)

@app.route("/quote" , methods=['GET', 'POST'])
def free_quote():
    req_quote = requests.get('https://zenquotes.io/api/random')
    data = req_quote.json()
    quote= data[0]['q']

    return render_template("index.html", quote=quote)

@app.route("/send_email" , methods=['GET', 'POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:  # put in time out so that it can connect
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="miha.novaktb@gmail.com", msg=f"Subject:Maybe new job\n\n"
                                                                        f"Preson:{name}, Email: {email}\n\n"
                                                                        f"Message: {message}")

            quote = "Email was sent!"
    except:
        quote = "Error on the server it is a free version :) email was not sent "
    return render_template("index.html", quote=quote)

if __name__ == "__main__":
    app.run( debug=False )