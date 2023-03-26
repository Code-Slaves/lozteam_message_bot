cd ..
if not exist venv\Scripts\activate.bat (
    python -m venv venv
)
cd C:\venv\Scripts
activate
cd script
pip install -r requirements.txt
python bot.py

