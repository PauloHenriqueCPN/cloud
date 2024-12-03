from app.routes import create_app

# Crie o app usando a função do routes.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
