import requests

data = {
  "name": "三国演义",
  "author": "罗贯中",
  "price": 99
}

# resp = requests.post("http://127.0.0.1:5000/books/add",data=data)
# print(resp.text)

resp = requests.get("http://127.0.0.1:5000/books/async")
print(resp.text)