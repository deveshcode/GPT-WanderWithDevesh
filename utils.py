import mysql.connector
import openai
import os

import requests
GPT_MODEL = "gpt-3.5-turbo-0613"
openai.api_key = os.getenv("OPENAI_API_KEY")

def function(temp):
    print(temp)

def connectionDB(user,password,host,database, query=""):
    config = {
        'user': user,
        'password': password,
        'host': host,
        'database':database,
        'raise_on_warnings': True
    }
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        res1 = cursor.execute('use {}'.format(database))
        if query:
            cursor.execute(query)
            result = cursor.fetchall()
            print('--------------',result)
            cnx.close()
            return result
        cnx.close()
        return True, cnx
    except Exception as e :
        return False, e

def setupOpenAI(openAI_passkey, ModelName):
    openai.api_key = openAI_passkey
    try:
        completion = openai.ChatCompletion.create(
        model=ModelName,
        messages=[
            {"role": "system", "content": "Testing connection"},
            {"role": "user", "content": "checking connection to openai"}
        ],
        temperature = 0.2,
        top_p = 0.1   
        )
        return True, completion.choices[0].message.content
    except Exception as e:
        return False, e 


def run_conversation(messages):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_to_sql",
                "description":'''
                            The function decides if the prompt needs access to database to answer query 
                            related to travel information, the db contains information for travel planning 
                            in following tables locations , ModeOfTravel , Activities ,ServiceProviders,TravelPackages 
                            ,PackageDetails,Users and booking
                            ''' 
                #'''if access to db is needed return true or False, for access to db which contains tables like locations , ModeOfTravel , Activities ,ServiceProviders,TravelPackages ,PackageDetails,Users and booking '''
            ,
            "parameters": {
                "type": "object",
                "properties":{
                    "query":{
                        "type":"string",
                        "description":"The query which needs to be converted to SQL to get the answer for eg. list all the travel packages",
                    },
                    
                    }
                },
                "required":["query"]
            }
            }
    ]

    chat_response = chat_completion_request(
        messages,
        tools= tools
    )
    print(chat_response.json())
    try:
        assistant_message = chat_response.json()["choices"][0]["message"]
        return assistant_message
    except Exception as e:
        print('___'* 10)
        print(messages,e)
        print('___'* 10)
        return {"content":"retry"}
    
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    import pdb;pdb.set_trace()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})

    json_data.update({"tool_choice": "auto"})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        print('-chatgpt Response -'*9)
        print('---'*9)
        return response
    except Exception as e:
        print('-chatgpt Response error-'*9)
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def question_to_sql(question):
    print('---->',question)
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": """You are a helpful assistant that can covert query to SQL. return just the SQL for query.Given following tables in sql schema: <schemaInfo> 
         1. Locations 
             Purpose: Stores information about various travel destinations.
            Key Data: Includes LocationID, city names, countries, and descriptions of each location.
        2. ModesOfTravel 
             Purpose: Details the different modes of travel between locations.
             Key Data: Contains TravelID, mode of travel (e.g., flight, train), travel class, associated costs, and references to start and end locations from the Locations table.
        3. Activities 
             Purpose: Lists activities available at each location.
            Key Data: Includes ActivityID, LocationID (linked to the Locations table), name and type of activity, descriptions, and costs.
        4. ServiceProviders 
             Purpose: Information about companies and individuals offering services related to travel.
            Key Data: Contains ProviderID, names, service types (e.g., accommodation, local guide), and contact information.
        5. TravelPackages 
             Purpose: Details of pre-arranged travel packages.
             Key Data: Includes PackageID, package names, descriptions, and prices.
        6. PackageDetails 
             Purpose: Connects travel packages with specific modes of travel, activities, and service providers.
             Key Data: Links PackageID to TravelID, ActivityID, and ProviderID from respective tables.
        7. Users 
             Purpose: Stores information about users of the service.
             Key Data: Includes UserID, user names, and email addresses.
        8. Bookings 
             Purpose: Records of bookings made by users.
             Key Data: Contains BookingID, references to UserID and PackageID, and dates of booking and travel.
        DDL for the tables is given below: 
         
CREATE TABLE Locations (
    LocationID INT PRIMARY KEY,
    City VARCHAR(100),
    Country VARCHAR(100),
    Description TEXT
);

-- ModesOfTravel Table
CREATE TABLE ModesOfTravel (
    TravelID INT PRIMARY KEY,
    Mode VARCHAR(50),
    Class VARCHAR(50),
    StartLocationID INT,
    EndLocationID INT,
    Duration VARCHAR(50),
    Cost DECIMAL(10, 2),
    FOREIGN KEY (StartLocationID) REFERENCES Locations(LocationID),
    FOREIGN KEY (EndLocationID) REFERENCES Locations(LocationID)
);

-- Activities Table
CREATE TABLE Activities (
    ActivityID INT PRIMARY KEY,
    LocationID INT,
    Name VARCHAR(100),
    Type VARCHAR(100),
    Description TEXT,
    Cost DECIMAL(10, 2),
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);

-- ServiceProviders Table
CREATE TABLE ServiceProviders (
    ProviderID INT PRIMARY KEY,
    Name VARCHAR(100),
    ServiceType VARCHAR(50),
    ContactInfo VARCHAR(100)
);

-- TravelPackages Table
CREATE TABLE TravelPackages (
    PackageID INT PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    Price DECIMAL(10, 2)
);

-- PackageDetails Table
CREATE TABLE PackageDetails (
    PackageID INT,
    TravelID INT,
    ActivityID INT,
    ProviderID INT,
    FOREIGN KEY (PackageID) REFERENCES TravelPackages(PackageID),
    FOREIGN KEY (TravelID) REFERENCES ModesOfTravel(TravelID),
    FOREIGN KEY (ActivityID) REFERENCES Activities(ActivityID),
    FOREIGN KEY (ProviderID) REFERENCES ServiceProviders(ProviderID)
);

-- Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100)
);

-- Bookings Table
CREATE TABLE Bookings (
    BookingID INT PRIMARY KEY,
    UserID INT,
    PackageID INT,
    BookingDate DATE,
    TravelDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (PackageID) REFERENCES TravelPackages(PackageID)
);

         Relationships:
         the PackageDetails table acts as a junction table, connecting TravelPackages with ModesOfTravel, Activities, and ServiceProviders.
         The Bookings table links Users to their chosen TravelPackages,</schemaInfo> instruction to follow 1. Only return SQL query 2. use fields names specified for the table in schemaInfo. 3 use tables name speicified in the schemaInfo.; 5. recheck that the column names used are correct and matches with the schema passed
         for eg. if query to find out list of user names-> return SELECT `Name` FROM TravelPlannerDB.Users;  """},
        {"role": "user", "content": "Ensure that the column names used are only those which is passed. check that the column names and table names used are right.  {}".format(question)}
      ],
     temperature = 0.2,
    top_p = 0.1   
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    run_conversation("list all the travel packages")

    