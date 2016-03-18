# post
One more study project

#### How to deploy
Install dependencies:

    pip install -r requirements.txt


Set environment variables:

    export POST_DATABASE=postgresql://user:pass@host:port/database # you can use any database
    export PORT=80 # port on which app will be deployed, otherwise it will use 5000

Create database schema:

    python migrate.py db init
    python migrate.py db migrate
    python migrate.py db upgrade

run:

    python run.py
