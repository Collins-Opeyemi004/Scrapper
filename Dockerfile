# 1. Use the official Playwright Python base image
FROM mcr.microsoft.com/playwright/python:latest

# 2. (Optional) Create a non-root user for security
RUN useradd -m myuser
USER myuser

# 3. Create a working directory
WORKDIR /home/myuser/app

# 4. Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy your entire project code
COPY . .

# 6. Expose the port your Flask app runs on
EXPOSE 10000

# 7. Run your Flask app
CMD ["python", "app.py"]
