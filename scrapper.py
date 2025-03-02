# import requests
# from bs4 import BeautifulSoup
# import schedule
# import threading
# from flask import Flask, jsonify
# import time

# app = Flask(__name__)

# WEBHOOK_URL = "https://hook.us2.make.com/8ng1v9fw7x63kfsrw4siix8a7jdyybqi"  # Replace with actual Make.com webhook URL

# leaderboard_data = []

# def scrape_leaderboard():
#     global leaderboard_data
#     url = "https://kolscan.io/leaderboard"

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         print(f"❌ Failed to fetch page: {response.status_code}")
#         return

#     soup = BeautifulSoup(response.text, "html.parser")

#     leaderboard = []
#     players = soup.select(".leaderboard_leaderboardUser__8OZpJ")  # Adjust selector if needed

#     if not players:
#         print("⚠️ No leaderboard data found. The page structure might have changed.")
#         return

#     for index, player in enumerate(players, start=1):
#         try:
#             profile_icon = player.select_one("img")["src"]
#             profile_url = player.select_one("a")["href"]
#             wallet_address = profile_url.split("/account/")[-1] if "/account/" in profile_url else "N/A"

#             name_element = player.select_one("a h1")
#             name = name_element.text.strip() if name_element else "Unknown"

#             stats = player.select(".remove-mobile p")
#             sol_number = player.select_one(".leaderboard_totalProfitNum__HzfFO h1:nth-child(1)").text.strip()
#             dollar_value = player.select_one(".leaderboard_totalProfitNum__HzfFO h1:nth-child(2)").text.strip()

#             leaderboard.append({
#                 "rank": index,
#                 "profile_icon": profile_icon,
#                 "name": name,
#                 "profile_url": f"https://kolscan.io{profile_url}",
#                 "wallet_address": wallet_address,
#                 "wins": stats[0].text.strip() if len(stats) > 0 else "0",
#                 "losses": stats[1].text.strip() if len(stats) > 1 else "0",
#                 "sol_number": sol_number,
#                 "dollar_value": dollar_value
#             })

#         except Exception as e:
#             print(f"❌ Error extracting data for rank {index}: {e}")

#     leaderboard_data = leaderboard

#     # Send extracted data to Make.com webhook
#     try:
#         response = requests.post(WEBHOOK_URL, json={"leaderboard": leaderboard})
#         response.raise_for_status()
#         print("✅ Data sent successfully:", response.status_code)
#     except requests.exceptions.RequestException as e:
#         print("❌ Failed to send data:", e)

# # Schedule the scraper to run every 6 hours
# schedule.every(6).hours.do(scrape_leaderboard)

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(60)  # Check the schedule every minute

# # Start scheduler in a background thread
# threading.Thread(target=run_scheduler, daemon=True).start()

# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"message": "Welcome to your scraping API! Add /scrape to trigger scraping."})

# @app.route("/scrape", methods=["GET"])
# def manual_scrape():
#     scrape_leaderboard()
#     return jsonify({"message": "Scraping triggered!", "data": leaderboard_data})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000, debug=True)
