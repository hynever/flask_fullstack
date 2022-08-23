import random

from flask import Flask, redirect, request, render_template
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, select, create_engine
import aiohttp
import asyncio
import time
import requests
from asgiref.wsgi import WsgiToAsgi


ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./book.db"
async_engine = create_async_engine(ASYNC_DATABASE_URL,echo=False)
async_session = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()

app = Flask(__name__)
app.jinja_env.is_async = True


# @app.before_first_request
# async def before_first_request():
#   async with async_engine.begin() as conn:
#     await conn.run_sync(Base.metadata.drop_all)
#     await conn.run_sync(Base.metadata.create_all)
#
#   fake = Faker(locale="zh_CN")
#   async with async_session() as session:
#     async with session.begin():
#       for x in range(10000):
#         name = fake.text()
#         author = fake.name()
#         price = random.random() * 100
#         book = Book(name=name, author=author, price=price)
#         session.add(book)

@app.teardown_appcontext
async def teardown_appcontext(f):
  await async_engine.dispose()



class Book(Base):
  __tablename__ = "books"
  id = Column(Integer, primary_key=True)
  name = Column(String(200), nullable=False)
  author = Column(String(200), nullable=False)
  price = Column(Float, default=0)


async def get_all_books():
  async with async_session() as session:
    stmt = select(Book)
    result = await session.execute(stmt)
    books = result.scalars().all()
    return books

app.jinja_env.globals["books"] = get_all_books


@app.route('/')
def index():
  return render_template("index.html")

async def fetch_url(session,url):
  response = await session.get(url)
  return {'url': response.url, 'status': response.status}


@app.route("/website/async")
async def website_async():
  start_time = time.time()
  urls = [
    "https://www.python.org/",
    "https://www.php.net/",
    "https://www.java.com/",
    "https://dotnet.microsoft.com/",
    "https://www.javascript.com/"
  ]
  async with aiohttp.ClientSession() as session:
    tasks = []
    for url in urls:
      tasks.append(fetch_url(session,url))
    sites = await asyncio.gather(*tasks)

  response = '<h1>URLs: </h1>'
  for site in sites:
    response += f"<p>URL: {site['url']}, Status Code: {site['status']}</p>"

  end_time = time.time()
  print("time:%.2f"%(end_time-start_time))
  return response


@app.route("/website/sync")
def website_sync():
  start_time = time.time()
  urls = [
    "https://www.python.org/",
    "https://www.php.net/",
    "https://www.java.com/",
    "https://dotnet.microsoft.com/",
    "https://www.javascript.com/"
  ]
  sites = []
  for url in urls:
    response = requests.get(url)
    sites.append({'url': response.url, 'status': response.status_code})

  response = '<h1>URLs: </h1>'
  for site in sites:
    response += f"<p>URL: {site['url']}, Status Code: {site['status']}</p>"

  end_time = time.time()
  print("time:%.2f"%(end_time-start_time))
  return response


@app.post('/books/add')
async def add_books():
  name = request.form.get('name')
  author = request.form.get("author")
  price = request.form.get('price')
  async with async_session() as session:
    async with session.begin():
      book = Book(name=name, author=author, price=price)
      session.add(book)
      await session.flush()
  return "success"


wsgi_app = WsgiToAsgi(app)

# if __name__ == '__main__':
#   app.run(debug=True, host="0.0.0.0")
