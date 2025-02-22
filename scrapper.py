import requests
from bs4 import BeautifulSoup
import schedule
import time
from flask import Flask, jsonify
import threading

app = Flask(__name__)

# Make.com Webhook URL
WEBHOOK_URL = 'https://hook.us2.make.com/8ng1v9fw7x63kfsrw4siix8a7jdyybqi'  # Replace with your actual webhook URL

leaderboard_data = []

def scrape_leaderboard():
    global leaderboard_data
    url = 'https://kolscan.io/leaderboard'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to retrieve page, status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    leaderboard = []
    entries = soup.select('.leaderboard_leaderboardUser__8OZpJ')

    if not entries:
        print("⚠️ No leaderboard data found. The page structure might have changed.")
        return

    for index, entry in enumerate(entries, start=1):
        profile_icon = entry.select_one('div[style*="border-radius:1000px;"] img')
        name = entry.select_one('a h1')
        profile_url = entry.select_one('a[href]')
        wallet = entry.select_one('p.cursor-pointer.remove-mobile')
        wins = entry.select_one('div.remove-mobile p:first-child')
        losses = entry.select_one('div.remove-mobile p:nth-child(2)')
        sol_amount = entry.select_one('.leaderboard_totalProfitNum__HzfFO h1:first-child')
        dollar_amount = entry.select_one('.leaderboard_totalProfitNum__HzfFO h1:nth-child(2)')

        leaderboard.append({
            "rank": index,
            "profileIcon": profile_icon['src'] if profile_icon else "N/A",
            "name": name.text.strip() if name else "Unknown",
            "profileURL": f"https://kolscan.io{profile_url['href']}" if profile_url else "N/A",
            "wallet": wallet.text.strip() if wallet else "N/A",
            "wins": wins.text.strip() if wins else "0",
            "losses": losses.text.strip() if losses else "0",
            "solAmount": sol_amount.text.replace(' Sol', '').strip() if sol_amount else "0",
            "dollarAmount": dollar_amount.text.replace('($)', '').strip() if dollar_amount else "0"
        })

    leaderboard_data = leaderboard
    
    # Send extracted data to Make.com webhook
    try:
        response = requests.post(WEBHOOK_URL, json={"leaderboard": leaderboard})
        print('✅ Data sent successfully:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('❌ Failed to send data:', e)

# Schedule the scraper to run every 6 hours
schedule.every(6).hours.do(scrape_leaderboard)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check the schedule every minute

# Start scheduler in a background thread
threading.Thread(target=run_scheduler, daemon=True).start()

@app.route('/scrape', methods=['GET'])
def manual_scrape():
    scrape_leaderboard()
    return jsonify({"message": "Scraping triggered!", "data": leaderboard_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Use Render's assigned PORT
