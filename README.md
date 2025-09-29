# Pinyin 2-Choice Listening Game

## Local dev
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn api.index:app --reload --port 8000

## Deploy
vercel --prod
