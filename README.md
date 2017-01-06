# Marten, Http Chaos Monkey Server

Marten provides a way to test your upstream application or proxy server by randomly returning HTTP codes with a predefined
probability.

## Requirements
    eve
    eve-swagger
    eve-sqlalchemy
    
## Setup
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Config
    
### CLI
    export AUTO_RELOAD=False
    export DEBUG=False
    export HOST=127.0.0.1
    export PORT=5000

### HTTP Return Code Bingo

    cp example/marten.yaml .
    cat marten.yaml
    ---
    - status_code: 200
      payload: ok
      probability: 0.7
    - status_code: 300
      payload: moved
      probability: 0.1
    - status_code: 400
      payload: your fault
      probability: 0.1
    - status_code: 500
      payload: my fault
      probability: 0.1

If you provide a marten.yaml in the same directory as run.py, the contents is
imported at bootstrap, otherwise the defaults from the example get bootstrapped).

These return codes can also be changed on the fly while viewing the dashboard or using the API endpoints.

## Run

    ./run.py
    
## Endpoints

    http://$HOST:$PORT/* => HTTP Return Code Bingo.
    http://$HOST:$PORT/marten/v1 => API to change config on the fly.
    http://$HOST:$PORT/marten/api-docs => Swagger json definition.
    http://$HOST:$PORT/marten/static => Css, img, js endpoint.
    http://$HOST:$PORT/marten/status => Usage dashboard.
   
## Known Issues

    - Marten doesnt provide a way to set Response Headers
