from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import psycopg2
import aiohttp

app = Flask(__name__)

# Elasticsearch client
es = Elasticsearch("http://elasticsearch:9200")

# SQL connection
db_conn = psycopg2.connect(
    dbname="datadungeons", user="dm", password="secret", host="db"
)

# LLM API call
async def query_llm(prompt):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://llm-service:8000/query", json={"prompt": prompt}) as resp:
            return await resp.json()

@app.route('/')
def dashboard():
    # Fetch player stats from SQL
    cursor = db_conn.cursor()
    cursor.execute("SELECT name, damage_dealt FROM players")
    players = cursor.fetchall()
    
    # Index data to Elasticsearch
    for player in players:
        es.index(index="player-stats", body={"name": player[0], "damage": player[1]})
    
    return render_template('dashboard.html', players=players)

@app.route('/ask-dm', methods=['POST'])
def ask_dm():
    question = request.form['question']
    response = asyncio.run(query_llm(question))
    return render_template('response.html', question=question, answer=response['answer'])

if __name__ == "__main__":
    app.run()