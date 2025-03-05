FROM mcr.microsoft.com/playwright/python:latest

# Optional: create a non-root user
RUN useradd -m myuser
USER myuser

WORKDIR /home/myuser/app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["python", "app.py"]
