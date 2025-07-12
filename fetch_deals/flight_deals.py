import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_TOKEN = "946fcb133722302df3eef5114f763e29"

indian_airports = {
    "Delhi": "DEL", "Mumbai": "BOM", "Bengaluru": "BLR", "Hyderabad": "HYD",
    "Chennai": "MAA", "Kolkata": "CCU", "Ahmedabad": "AMD", "Goa (Mopa)": "GOX", "Kochi": "COK"
}

global_airports_by_continent = {
    "Asia": {
        "Dubai": "DXB", "Abu Dhabi": "AUH", "Sharjah": "SHJ", "Doha": "DOH", "Kuwait City": "KWI",
        "Muscat": "MCT", "Riyadh": "RUH", "Jeddah": "JED", "Dammam": "DMM", "Manama": "BAH",
        "Medina": "MED", "Amman": "AMM", "Colombo": "CMB", "Malé": "MLE", "Kathmandu": "KTM",
        "Dhaka": "DAC", "Paro": "PBH", "Yangon": "RGN", "Bangkok": "BKK", "Phuket": "HKT",
        "Chiang Mai": "CNX", "Siem Reap": "REP", "Phnom Penh": "PNH", "Kuala Lumpur": "KUL",
        "Langkawi": "LGK", "Singapore": "SIN", "Jakarta": "CGK", "Bali (Denpasar)": "DPS",
        "Hanoi": "HAN", "Ho Chi Minh City": "SGN", "Hong Kong": "HKG", "Macau": "MFM",
        "Tokyo Narita": "NRT", "Tokyo Haneda": "HND", "Osaka Kansai": "KIX", "Seoul Incheon": "ICN",
        "Beijing": "PEK", "Shanghai": "PVG", "Guangzhou": "CAN", "Tashkent": "TAS",
        "Almaty": "ALA", "Ashgabat": "ASB", "Baku": "GYD", "Tbilisi": "TBS", "Yerevan": "EVN",
        "Tel Aviv": "TLV", "Tehran": "IKA", "Lahore": "LHE", "Karachi": "KHI", "Dushanbe": "DYU",
        "Beirut": "BEY"
    },
    "Europe": {
        "Vienna": "VIE", "Brussels": "BRU", "Copenhagen": "CPH", "Helsinki": "HEL",
        "Paris": "CDG", "Frankfurt": "FRA", "Munich": "MUC", "Athens": "ATH",
        "Reykjavik": "KEF", "Milan": "MXP", "Amsterdam": "AMS", "Warsaw": "WAW",
        "Lisbon": "LIS", "Madrid": "MAD", "Barcelona": "BCN", "Zurich": "ZRH",
        "Geneva": "GVA", "London": "LHR", "Gatwick": "LGW", "Manchester": "MAN",
        "Moscow (Sheremetyevo)": "SVO", "Moscow (Domodedovo)": "DME", "Moscow (Vnukovo)": "VKO",
        "St. Petersburg": "LED", "Sochi": "AER", "Kazan": "KZN", "Yekaterinburg": "SVX"
    },
    "North America": {
        "New York": "JFK", "Newark": "EWR", "Los Angeles": "LAX", "Chicago": "ORD",
        "San Francisco": "SFO", "Dallas/Fort Worth": "DFW", "Atlanta": "ATL", "Vancouver": "YVR",
        "Miami": "MIA", "Washington D.C.": "IAD", "Toronto": "YYZ"
    },
    "South America": {
        "São Paulo": "GRU", "Buenos Aires": "EZE", "Lima": "LIM", "Bogotá": "BOG",
        "Santiago": "SCL", "Rio de Janeiro": "GIG", "Quito": "UIO", "Montevideo": "MVD",
        "Caracas": "CCS", "La Paz": "LPB"
    },
    "Africa": {
        "Johannesburg": "JNB", "Cairo": "CAI", "Nairobi": "NBO", "Addis Ababa": "ADD",
        "Casablanca": "CMN", "Lagos": "LOS", "Accra": "ACC", "Cape Town": "CPT",
        "Tunis": "TUN", "Dakar": "DSS", "Mahé": "SEZ"
    },
    "Oceania": {
        "Sydney": "SYD", "Melbourne": "MEL", "Brisbane": "BNE", "Auckland": "AKL", "Perth": "PER"
    }
}

# 🌍 Ask user for destination city
user_input = input("Enter your destination city (e.g. London, Tokyo): ").strip().lower()

# 🔍 Match to IATA and continent
destination = None
for continent, cities in global_airports_by_continent.items():
    for city, iata in cities.items():
        if city.lower() == user_input:
            destination = {"city": city, "iata": iata, "continent": continent}
            break
    if destination:
        break

if not destination:
    print("❌ Destination not recognized.")
    exit()

print(f"\n🔁 Checking flight deals to {destination['city']} ({destination['continent']}) over the next 6 months...\n")

API_URL = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
today = datetime.today()
all_deals = []

for origin_city, origin_code in indian_airports.items():
    for i in range(6):  # Next 6 months
        depart_month = (today + relativedelta(months=i)).strftime('%Y-%m')
        return_month = (today + relativedelta(months=i+1)).strftime('%Y-%m')

        params = {
            "origin": origin_code,
            "destination": destination["iata"],
            "departure_at": depart_month,
            "return_at": return_month,
            "currency": "INR",
            "token": API_TOKEN,
            "limit": 10,
            "sorting": "price"
        }

        try:
            res = requests.get(API_URL, params=params)
            res.raise_for_status()
            deals = res.json().get("data", [])
            for deal in deals:
                all_deals.append({
                    "origin_city": origin_city,
                    "price": deal['price'],
                    "airline": deal['airline'].upper(),
                    "departure_at": deal['departure_at'],
                    "return_at": deal['return_at']
                })
        except Exception as e:
            print(f"⚠️ Error {origin_code} → {destination['iata']} ({depart_month}): {e}")

# 🔽 Show results
sorted_deals = sorted(all_deals, key=lambda d: d["price"])

print("\n💸 Top 5 Cheapest Deals:\n")
if not sorted_deals:
    print("😕 No flight deals found to this destination.")
else:
    for i, deal in enumerate(sorted_deals[:5], 1):
        print(f"{i}. {deal['origin_city']} → {destination['city']} | ₹{deal['price']} | {deal['airline']} | {deal['departure_at']} → {deal['return_at']}")