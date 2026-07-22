
# fastapi-auth-demo

I created this project for the sake of learning JWT authentication, and how to containerize the FastAPI app using docker.
If you want to test the endpoints, i suggest you to do it in postman instead.



## Installation

Here's how to install my project 

```bash
# Clone my repository
git clone https://github.com/Paxie-Backend/fastapi-auth-demo.git
cd fastapi-auth-demo
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file.
I intentionally include the .env file in the .gitignore and .dockerignore files to follow best practice.

`SECRET_KEY=3c8d64fb5fa1d85a3ef5e691035f7c67`
`JWT_SECRET_KEY=ATNE1jPTjgfKdU4qULWDSgA647VYQ73WCNutUk3i6jI`
`JWT_ALGORITHM=HS256`

`ACCESS_TOKEN_EXPIRE_MINUTES=15`
`REFRESH_TOKEN_EXPIRE_DAYS=7`

`POSTGRES_USER=postgres`
`POSTGRES_PASSWORD=password`
`POSTGRES_DB=mydb`

`DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/mydb`


## Docker

Run my project with Docker Compose:

```bash
docker-compose up --build -d
```
## API Reference

#### Authenticate user

```http
  POST http://127.0.0.1:8000/api/auth/login
```

| form-data | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Email Required**. The "username" field is intentional because of FastAPi swagger UI|
| `password` | `string` | **Required**. |

#### Register user creds

```http
  POST http://127.0.0.1:8000/api/auth/register
```

| raw-JSON | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `first_name`      | `string` | **Required**.|
| `last_name`      | `string` | **Not Required**.|
| `password`      | `string` | **Required**.|
| `email`      | `string` | **Required**.|


#### Refresh Access Token

```http
  POST http://127.0.0.1:8000/api/auth/refresh
```

| raw-JSON | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh_token`      | `string` | **Required**.|


#### Get Current User

```http
  GET http://127.0.0.1:8000/api/auth/me
```

| Authorization | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Bearer <accessToken>`      | `string` | **Required**.|
