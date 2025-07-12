import sys
from app import app  # ✅ Flask server
from fetch_deals.sample import get_flight_deals, get_iata_from_city
from fetch_deals.send_emails import send_email
from fetch_deals.config import SHEETY_URL


import requests


def get_users():
    """Fetch users from Google Sheet via Sheety API."""
    response = requests.get(SHEETY_URL)
    if response.status_code == 200:
        return response.json().get("sheet1", [])
    else:
        print("❌ Failed to fetch users")
        return []


def send_deals_to_users():
    """Send best flight deals to all users based on their saved destination."""
    users = get_users()
    for user in users:
        name = user["name"]
        email = user["email"]
        destination_city = user["destination"]

        iata = get_iata_from_city(destination_city)
        if not iata:
            print(f"❌ Destination not recognized: {destination_city}")
            continue

        deals = get_flight_deals(iata)

        if not deals:
            body = f"Hi {name},\n\nSorry, no flight deals were found for {destination_city.title()}."
        else:
            body = f"Hi {name},\n\nHere are the top flight deals to {destination_city.title()}:\n\n"
            for d in deals[:5]:
                body = f"Hi {name},\n\nHere are the top flight deals to {destination_city.title()}:\n\n"
                for d in deals[:5]:
                    body += (
                        f"🔹 {d['origin_city']} → {destination_city.title()} | ₹{d['price']} | "
                        f"{d['airline']} | {d['departure_at'].split('T')[0]}\n"
                    )


        # Send the email
        send_email(email, f"🛫 Flight Deals to {destination_city.title()}", body)
        print(f"✅ Email sent to {email}")



if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else input("Enter mode (runserver/sendemails/both): ").strip().lower()
    print(f"▶️ Mode selected: {mode}")

    if mode == "runserver":
        print("🚀 Running Flask server at http://127.0.0.1:5000")
        app.run(debug=True)
    elif mode == "sendemails":
        send_deals_to_users()
    elif mode == "both":
        print("🚀 Running Flask + sending emails...")
        import threading
        threading.Thread(target=send_deals_to_users).start()
        app.run(debug=True)
    else:
        print("❌ Invalid mode. Use 'runserver', 'sendemails', or 'both'")