# onlinebooks

## Description

This is a simple web application that allows users to search for books and save them to a list. The application uses the
Google Books API to retrieve book information.

## Setup

1. Clone the repository
2. Install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set the environment variables

```
export MONOGO_URI = <MongoDB URI>
export GOOGLE_BOOKS_API_KEY=<Google Books API Key>

```

Or touch config.py and add the following

```
MONGO_URI = <MongoDB URI>
GOOGLE_BOOKS_API_KEY=<Google Books API Key>
``` 

4. Run the application

```
python main.py
```

4.1. Run the application in uvicorn server

```
uvicorn main:app --reload
```

5. Open http://localhost:8000 in your browser

## Tech Stack

- FastAPI
- MongoDB
- Bootstrap
- HTML
- CSS

## thing to do

- [ ] Add swagger documentation
- [ ] Add user authentication
- [ ] deploy to heroku
- [ ] CI/CD (use github actions)
- [ ] Add tests

 
