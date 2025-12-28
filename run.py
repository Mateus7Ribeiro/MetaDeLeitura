import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Em produção, use Gunicorn: gunicorn "app:create_app()"
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
