## Test task for Python Automation Masters company

Used:

```
- requests
- selenium
- bs4
```

faster.py - use requests sessions
wlogin.py - use selenium

!!!Create your own .env file with this variables:
```
TELEGRAM_BOT_TOKEN=
YOUR_CHAT_ID=
EMAIL=
PASSWORD=
```

Run faster.py:
```
python -m venv venv
# activate venv
pip install -r requirements.txt
python faster.py
```

Run wlogin:
```
python -m venv venv
# activate venv
pip install -r requirements.txt
# chromedriver.exe may be required
# browser = webdriver.Chrome(executable_path=r"C:\path\to\chromedriver.exe")
# or place chromedriver in your System Path
python wlogin.py
```

Run wlogin.py with Docker:
```
docker-compose up --build
```
