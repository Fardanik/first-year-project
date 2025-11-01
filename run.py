from app import create_app
from app.database.main import create_database

app = create_app()

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
