# onlinebooks

## Description

This web application provides a simple interface for users to search for books and add them to a list, utilizing the Google Books API to fetch book information. It serves as a practical tool for learning agile development and automated deployment. This project is part of a team assignment for the "Software Engineering" course at the Technological University of the Shannon (TUS).






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

- [x] Add swagger documentation
- [ ] Add user authentication JWT
- [ ] user own search history
- [ ] download book (pdf,zlibary)
- [x] deploy to aws
- [x] CI/CD (use github actions)
- [x] Add tests
- 

 
