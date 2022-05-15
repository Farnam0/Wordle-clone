# Microservice Implementation with FastAPI

<!-- ABOUT THE PROJECT -->
## Contributors
- **Ramon Amini**
- **Evan**
- **Farnam Keshavarzian**

### Built With

* [FastAPI](https://fastapi.tiangolo.com/)
* [Foreman](https://pypi.org/project/foreman/)
* [SQLite](https://www.sqlite.org/index.html)
* [Uvicorn](https://www.uvicorn.org/)
* [Sqlite-Utils](https://pypi.org/project/sqlite-utils/)
* [MultipleDispatch](https://pypi.org/project/multipledispatch/)
* [Redis](https://redis.io/docs/getting-started/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

* Make sure to have python3 and pip installed on your computer.
  ```sh
    sudo apt update
    sudo apt install --yes python3-pip ruby-foreman sqlite3 httpie
  ```

* Install FastAPI and other tools
  ```sh
    python3 -m pip install 'fastapi[all]' sqlite-utils uvicorn multipledispatch pydantic
  ```
* Install Redis
  ```sh
    sudo apt install --yes redis
    sudo apt install --yes python3-hiredis
  ```
* Files missing
  ```sh 
  There are two major files missing and this is due to github file size limitations.
  traefik requires to be downloaded and placed within the proxy folder. https://github.com/traefik/traefik/releases
  statistics.db can be requested from us and must be placed within the db folder. 
  ```
### Final Steps

1. Clone the repo
   ```sh
   git clone https://github.com/Farnam0/Wordle-clone.git
   ```
2. In the root directory of the app folder, create a .env and set values for CHECKING_PORT and VALIDATION_PORT
    ```
    CHECKING_PORT=5000
    VALIDATION_PORT=5500
    TRACKER_PORT=5600
    ```
3. Seed the database! (you may need to change permissions on your local machine)
   ```sh
   cd db/
   ./db_seed.sh
   ```    
4. Run either the checkings or validation service (or both!)
   ```sh
   cd ../
   foreman start
   ```
5. Currently our standalone python script which updates the redis cache needs to be manually executed,
   to do so please make sure MaterilizeScript.py is in the root directory of the project 
     ```sh
   python3 MaterilizeScript.py
   ```
6. Travel to http://127.0.0.1:9999/api/checkings/docs or http://127.0.0.1:9999/api/statistics/docs or http://127.0.0.1:9999/api/validations/docs or http://127.0.0.1:9999/api/trackers/docs (depends on the values inputted for which service you wish to test)
7. Once there you can test out the routes!







