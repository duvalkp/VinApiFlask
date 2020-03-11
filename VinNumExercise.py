from flask import Flask, render_template
import json, requests

app = Flask(__name__)

@app.route('/')
def home():
        return "Please type 'Default address'/api/'Your Vin number here' in the address bar to return information about a Vin #."

@app.route('/api/<vin>', methods=['GET'])
def lookupVin(vin):
    try:
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/%s?format=json' % vin
        #Vin number is obtained through the url entered into the browser
        print("This VIN number was requested: ", vin)
        results = requests.get(url)
        print("Got results from this url: ", url)
        data = json.loads(results.text)
        #Converts the response object to a dictionary
        for i in data['Results']:
                if i['ErrorCode'][0] != '0':
                #Looks at the first character in the ErrorCode entry. In the json data provided from the website, 
                #the entry has a number to go with the error that was found. Any number other than zero is an error.
                        print("Error found: " + i['ErrorCode'])
                        return "The API was unable to find all the vehicle's information. Refer to the following error information and check that the VIN number is entered correctly: " + i['ErrorCode'], 400
                        #Returns code 400 (Bad Request) with the error code from the website
                print("Successfully returned Make, Model, Year:", i['Make'], i['Model'], i['ModelYear'],sep=' ')
                return render_template('vin.html',vin = vin ,year = i['ModelYear'], make = i['Make'], model = i['Model']), 200
                #return "Year: " + i['ModelYear'] + "\nMake: " + i['Make'] + "\nModel: " + i['Model'], 200
                #Return and print to console the Year Make and Model with 200 OK code

    except Exception as e: 
            print("Error found: see below")
            print(e)
            return str(e) + " Check the VIN number you entered in the Url"
            #Generic exception: will diplay on page and in console
            

if __name__ == '__main__':
    app.run()
