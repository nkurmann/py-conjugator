from arbol.routes import create_app
# A very simple Flask Hello World app for you to get started with...


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
