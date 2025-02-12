import sqlite3
import datetime
import json

from _dataclasses import Council, ScraperReturn

# TODO: rewrite this with the ScraperReturn and Council dataclasses

def init():
  conn = sqlite3.connect('agendas.db')
  c = conn.cursor()
  c. execute('''CREATE TABLE IF NOT EXISTS agendas
                (id INTEGER PRIMARY KEY, 
                date_scraped TEXT, 
                council TEXT, 
                meeting_date TEXT,
                meeting_time TEXT,
                webpage_url TEXT, 
                download_url TEXT,
                result BLOB)''')
  conn.commit()
  conn.close()
  
def insert(council: Council, scraper_return: ScraperReturn, result: dict):
  date = datetime.datetime.now().strftime("%Y-%m-%d")
  binary_result = json.dumps(result).encode()
  conn = sqlite3.connect('agendas.db')
  c = conn.cursor()
  c.execute('''INSERT INTO agendas (
                date_scraped, council, meeting_date,
                meeting_time, webpage_url, download_url, result) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (date, council.name, scraper_return.date, 
             scraper_return.time, scraper_return.webpage_url, 
             scraper_return.download_url, binary_result))
  conn.commit()
  conn.close()

def check_url(url: str):
  conn = sqlite3.connect('agendas.db')
  c = conn.cursor()
  c.execute('SELECT * FROM agendas WHERE download_url=?', (url,))
  result = c.fetchone()
  conn.close()
  return result