from fastapi import FastAPI
from app.scraper import scrape_leaderboard
from app.scheduler import start_scheduler  # ✅ Import start_scheduler instead of run_scheduler

app = FastAPI()

# Start the background scheduler in a separate thread
start_scheduler()  # ✅ Start the scheduler properly

@app.get("/")
def home():
    return {"message": "Leaderboard Scraper is running."}

@app.get("/leaderboard")
def get_leaderboard():
    from app.scraper import leaderboard_data
    return {"leaderboard": leaderboard_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
