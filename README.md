
K7*9TYZh9#aIqATIZ6

###  
| URL                             | Что произойдёт        |
|----------------------------------|------------------------|
| http://localhost:8000/          | Лендинг WordPress     |
| http://localhost:8000/order     | FastAPI (API и формы) |
| http://localhost:8000/static/   | Статика FastAPI       |

###  Launch the server host="0.0.0.0", port=5000
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000