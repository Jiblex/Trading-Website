from application import app

if __name__ == '__main__':
    # local host occupied so running through different port
    app.run(host='0.0.0.0', port=30006, debug=True)
