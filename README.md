# Casting-Agency
##### Casting Agency Api that handles the creation of Movie and Actor Objects. Api also links Actor and Movie objects and shows the relationship. 
#### Author: Joseph Mugo

## Getting Started
> Base Url: https://josephmugo-casting-agency.herokuapp.com/

> Authentication: not implemented 

### Pre-requisites and local Development
<b>Required:</b>
- python3
- pip

### Running Application
> export FLASK_APP=app

> export FLASK_ENV=development

> export DATABASEURL=<i>urlOfDatabase</i>

## Error 
##### 400
##### 403
##### 404
##### 410
##### 500

## Endpoints

| Method     | Path| Info     | Parameters | Request |
| :---        |    :----:   |           :----:   |           :----:   |         ---: |
| GET | /movies | gets all movies in database | N/A | GET /movies | 
| POST | /movies | post new movie to database | title, date | POST /movies | 
| GET | /actors | gets all actors in database | N/A | GET /actors |
| POST | /actors | post new actor to database | name, age, gender, movie_id | POST /actors | 
| PATCH | /actors/<i>id</i> | update specified actor object in database | <i>property of actor being updated</i> | PATCH /movies | 
| DELETE | /actors/<i>id</i> | delete specified actor object in database | N/A | DELETE /actors | 
