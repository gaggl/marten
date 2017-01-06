# Marten

Http chaos monkey server.

## Requirements
    eve
    eve-swagger
    eve-sqlalchemy
    
## Setup
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## CONFIG
    
    export AUTO_RELOAD=True
    export DEBUG=True
    export HOST=127.0.0.1
    export PORT=5000
    
## RUN

    ./run.py