from flask import Flask, render_template, request
import requests



app = Flask(__name__)


# ✅ Sheety API Endpoint
SHEETY_ENDPOINT = "https://api.sheety.co/1b10d87e4d8d97401a38c4a463481a52/flightDeals/sheet1"
SHEETY_URL = "https://api.sheety.co/1b10d87e4d8d97401a38c4a463481a52/flightDeals/sheet1"


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/signup', methods=['POST'])
def signup():
    full_name = request.form['fullName']
    email = request.form['email']
    destination = request.form['destination']

    # ✅ Format data for Sheety (no signInTime)
    new_row = {
        "sheet1": {  # ✅ key must be lowercase
            "name": full_name,
            "email": email,
            "destination": destination
        }
    }

    # ✅ Send to Google Sheet
    response = requests.post(SHEETY_ENDPOINT, json=new_row)
    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 200:
        return render_template("index.html", message="✅ Thanks for signing up!")
    else:
        return render_template("index.html", message="❌ Error saving data. Please try again.")


if __name__ == "__main__":
    print("✅ app.py is running directly")
    response = requests.get(SHEETY_ENDPOINT)
    print(response.json())
    app.run(debug=True)