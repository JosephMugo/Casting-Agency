# Casting-Agency
##### Casting Agency Api that handles the creation of Movie and Actor Objects. Api also links Actor and Movie objects and shows the relationship. 
#### Author: Joseph Mugo

## Getting Started
> Base Url: https://josephmugo-casting-agency.herokuapp.com/

> Authentication: implemented
Login: https://dev-8bzdf01x.us.auth0.com/authorize?audience=casting&response_type=token&client_id=kcqDRJaQO1VsrHAR9zzWiYb4upMADUdI&redirect_uri=http://localhost:5000/login
login with credentials and copy access token in url

Logout Page: https://dev-8bzdf01x.us.auth0.com/v2/logout?client_id=kcqDRJaQO1VsrHAR9zzWiYb4upMADUdI&returnTo=http://localhost:5000/logout
logout in order to logout current session and then use the link for login to access another account

### Pre-requisites and local Development
<b>Required:</b>
- python3
- pip

### Running Application
> pip install -r requirements.txt

> export FLASK_APP=app

> export FLASK_ENV=development

> export DATABASEURL=<i>urlOfDatabase</i>

## Error 
##### 400
##### 403
##### 404
##### 410
##### 500

## Roles & Permissions
#### Casting Assistant
movie casting assistant
###### permissions
- GET /movies
- GET /actors
#### Casting Director
movie casting director
###### permissions
- GET /movies
- GET /actors
- POST /actors
- PATCH /actors
- DELETE /actors
#### Executive Producer
movie executive producer
###### permissions
###### - ALL ENDPOINTS

## Endpoints
endpoints require Authorization - Bearer Token with correct permission
| Method     | Path| Info     | Parameters | Request |
| :---        |    :----:   |           :----:   |           :----:   |         ---: |
| GET | /movies | gets all movies in database | N/A | GET /movies | 
| POST | /movies | post new movie to database | title, date | POST /movies | 
| GET | /actors | gets all actors in database | N/A | GET /actors |
| POST | /actors | post new actor to database | name, age, gender, movie_id | POST /actors | 
| PATCH | /actors/<i>id</i> | update specified actor object in database | <i>property of actor being updated</i> | PATCH /movies | 
| DELETE | /actors/<i>id</i> | delete specified actor object in database | N/A | DELETE /actors | 

## Testing
#### Start with fresh database
#### SET ENV variables below for test
##### DATABASEPASS
##### ASSISTANT_TOKEN
##### DIRECTOR_TOKEN
##### EXECUTIVE_TOKEN
#### Manually input atleast one movie/actor record in database in order to pass tests
___
##### Movie Record - Manual Entry
##### id: 1
##### title: Movie Test
##### release_date: 4/2/2020
___
##### Actor Record - Manual Entry
##### id: 1
##### title: Actor Test
##### gender: male
##### movie_id: 1
