# Eatsee DB

Welcome to Eatsee DB

## Set-up instructions

1. Set up the postgreSQL database with the `.sql` file

    > Tested on postgreSQL 15.2

2. Fill up the configuration values in `config.config`, make sure the config file path in test.py corresponds to the path of your config file

    ```
    database_host = empty
    database_name = empty
    database_user = empty
    password = empty
    ```

3. Set up your venv

    > Tested on python 3.10.11
    ```
    python -m venv venv
    venv\scripts\activate
    pip install -r requirements.txt
    ```

4. Run `uvicorn main:app --reload`

    `main` refers to the name of the script `main.py`
    `app` refers to the name of the FastAPI object `app`
    `--reload` means that the API will reload automatically when the code changes, useful for development, DO NOT DEPLOY


5. Refer to the IP addresses provided in terminal for SwaggerUI API Documentation 

Contribution Instructions:

- Write compact testable code with unit tests
- Atomic Commits (Small git commits that are well named)
- Follow format and naming conventions


