# eGator-face-id
eGator financeverification system
## Running the development environment

> Note:: Ensure you have docker and docker-compose installed.

### 1. Clone the repository

```bash
git clone https://github.com/eGator-finance/eGator-verification-system
```

### 2. Build the docker image
cd into the project directory and run the following command

```bash
docker-compose build
```

### 3. Run the docker container

```bash
docker-compose up
```

### 4. Open frontend in browser
Go to http://localhost:3000

### 5. Open backend documentation in browser
Go to http://localhost:8000/docs#/

General Notes:
1. Frontend is built using Next.js. See https://nextjs.org/docs for more information.
2. Backend is built using FastAPI. See https://fastapi.tiangolo.com/ for more information.
3. The backend is configured to run on port 8000. If you want to change this, you can do so in the docker-compose.yml file.
4. The frontend is configured to run on port 3000. If you want to change this, you can do so in the docker-compose.yml file.
5. Auto-reload is enabled for both the frontend and backend. This means that any changes you make to the code will be reflected in the browser without having to restart the docker container. The backend will reload automatically as soon as you save a file.
