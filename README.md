# wortspark_app

This template contains a simple python app served by [fastapi](https://github.com/tiangolo/fastapi).
It shows you how to move a robot with the [wandelbots python API client](https://pypi.org/project/wandelbots-api-client/) and the [python api](https://github.com/wandelbotsgmbh/wandelbots-python).

Use the following steps for development:

* install all dependencies with `poetry install`
* ensure proper environment variables are set in `.env`
    * note: you might need to set/update `NOVA_ACCESS_TOKEN` and `NOVA_API`
* use `poetry run serve` to run the the server
    * access the example on `http://localhost:3000`
* install the app with `nova app install`