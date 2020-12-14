from application import application, routes

if __name__ == '__main__':
    application.run(host="localhost", port=8000, debug=True) #Disable this
    #application.run(host='localhost:8000') 
