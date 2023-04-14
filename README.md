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

4. Run `test.py`



Contribution Instructions:

- Write compact testable code with unit tests
- Atomic Commits (Small git commits that are well named)
- Follow format and naming conventions


