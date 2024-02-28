import sqlite3
import os

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('travel_agency.db')
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Locations (
        LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
        City VARCHAR(100),
        Country VARCHAR(100),
        Description TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Packages (
        PackageID INTEGER PRIMARY KEY AUTOINCREMENT,
        LocationID INTEGER,
        PackageName VARCHAR(255),
        Price DECIMAL(10, 2),
        DurationDays INTEGER,
        Description TEXT,
        FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        PackageID INTEGER,
        BookingDate DATE,
        TravelDate DATE,
        Status VARCHAR(50),
        FOREIGN KEY (PackageID) REFERENCES Packages(PackageID)
    );
    ''')

    # Populate Tables with Example Data
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Paris', 'France', 'The City of Light');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Tokyo', 'Japan', 'The bustling capital of Japan with a unique blend of traditional and modern.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('London', 'England', 'A vibrant city rich in history and culture.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Rome', 'Italy', 'The Eternal City, known for its historical landmarks, art, and cuisine.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('New York City', 'USA', 'The city that never sleeps, offering iconic attractions and diverse experiences.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Rio de Janeiro', 'Brazil', 'A city known for its stunning beaches, vibrant culture, and lively atmosphere.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Bali', 'Indonesia', 'An island paradise known for its beautiful beaches, temples, and unique culture.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Prague', 'Czech Republic', 'The City of a Hundred Spires, known for its stunning architecture, medieval charm, and rich history.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Barcelona', 'Spain', 'A vibrant city offering cultural delights, world-class architecture, and beautiful beaches.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Dubai', 'United Arab Emirates', 'A city of luxury, innovation, and architectural marvels, offering a unique blend of modern and traditional experiences.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Cape Town', 'South Africa', 'A beautiful city surrounded by stunning natural landscapes, offering diverse activities, from exploring wineries to visiting penguins.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Marrakesh', 'Morocco', 'A captivating city known for its bustling medina, colorful souks, and traditional riads, offering a unique cultural experience.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Budapest', 'Hungary', 'A city known for its thermal baths, stunning architecture, and rich history, offering a blend of Eastern European charm and Danube River cruises.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Amsterdam', 'Netherlands', 'A city famous for its canals, museums, and relaxed atmosphere, offering unique experiences like cycling tours and visiting flower markets.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Berlin', 'Germany', 'A vibrant city steeped in history, offering cultural attractions, world-class museums, and a dynamic nightlife scene.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Singapore', 'Singapore', 'A clean and modern city-state known for its diverse culture, delicious food scene, and iconic landmarks like Gardens by the Bay.');")
    cursor.execute("INSERT INTO Locations (City, Country, Description) VALUES ('Los Angeles', 'USA', 'The City of Angels, known for its Hollywood glamour, beaches, and diverse neighborhoods, offering experiences from movie studio tours to exploring theme parks.');")

 
    # Assuming LocationID 1 is Paris and 2 is Tokyo
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (1, 'Paris in Spring', 1200.00, 7, 'Experience the romantic spring of Paris.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (2, 'Tokyo Adventure', 1500.00, 5, 'Explore the vibrant culture of Tokyo.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (3, 'London Explorer', 1500.00, 5, 'Explore the iconic landmarks of London, including Buckingham Palace, Big Ben, and the Tower of London.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (4, 'Rome Delights', 2000.00, 10, 'Experience the best of Italy, from exploring the Colosseum in Rome to indulging in delicious food and wine.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (5, 'NYC Lights & Broadway', 1800.00, 7, 'Experience the magic of New York City, from seeing a Broadway show to exploring Times Square and iconic landmarks.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (6, 'Rio Carnival Experience', 2500.00, 8, 'Immerse yourself in the excitement of the Rio Carnival, including attending parades, experiencing the vibrant nightlife, and enjoying the beautiful beaches.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (7, 'Bali Relaxation Retreat', 1800.00, 10, 'Unwind and rejuvenate in the paradise of Bali, with yoga classes, spa treatments, and exploration of the islands natural beauty.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (8, 'Prague Castle Tour', 120.00, 1, 'Explore the majestic Prague Castle, a UNESCO World Heritage Site, and learn about its rich history and cultural significance.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (9, 'Barcelona Tapas & Flamenco', 800.00, 4, 'Immerse yourself in the culture of Barcelona with delicious tapas tours, a flamenco show, and exploration of iconic landmarks like Sagrada Familia.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (10, 'Dubai Desert Safari & Burj Khalifa', 1500.00, 3, 'Experience the thrill of a desert safari, enjoy breathtaking views from the top of the Burj Khalifa, and explore the modern marvels of Dubai.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (11, 'Cape Town Winelands & Table Mountain', 1000.00, 5, 'Explore the scenic vineyards of Cape Towns winelands, take a cable car ride to the top of Africa.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (12, 'Marrakesh Medina & Cooking Class', 700.00, 3, 'Explore the vibrant souks and hidden gems of the Marrakesh medina, and learn to cook traditional Moroccan cuisine with a local cooking class.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (13, 'Budapest Danube Cruise & Castle Tour', 850.00, 2, 'Enjoy a scenic cruise along the Danube River, followed by a guided tour of the Buda Castle, offering stunning views and rich historical insights.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (14, 'Amsterdam Canal Cruise & Van Gogh Museum', 900.00, 4, 'Experience Amsterdam from a unique perspective with a canal cruise, and delve into the world of art with a visit to the renowned Van Gogh Museum.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (15, 'Berlin Wall & Museum Tour', 600.00, 2, 'Learn about the history of the Berlin Wall with a guided tour, and visit museums like the Topography of Terror to gain deeper insights into this significant period.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (16, 'Singapore Gardens by the Bay & Night Safari', 1100.00, 3, ' Explore the futuristic Supertree Grove at Gardens by the Bay, and embark on an exciting night safari adventure to see nocturnal animals in their natural habitat.');")
    cursor.execute("INSERT INTO Packages (LocationID, PackageName, Price, DurationDays, Description) VALUES (17, 'LA Delights', 2000.00, 10, 'Experience the best of LA, from exploring the Colosseum in Rome to indulging in delicious food and wine.');")
    
    # Save (commit) the changes
    conn.commit()

    # Close the connection
    conn.close()

def connect_database():
    # Connect to the database
    conn = sqlite3.connect('travel_agency.db')
    return conn

import sqlite3

def execute_query(sql_query):
    """
    Executes a SQL query on the database and returns the results.
    
    :param sql_query: The SQL query string to be executed.
    :return: The result of the query execution.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('travel_agency.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        
        # If the query is a SELECT statement, fetch and return the results
        if sql_query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        else:
            # For non-SELECT queries, commit changes and return a success message
            conn.commit()
            return "Query executed successfully."
    except Exception as e:
        # Return the error message if query execution fails
        return f"An error occurred: {e}"
    finally:
        # Close the connection
        conn.close()

import openai
from openai import OpenAI

def nl_to_sql(question, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    schema_info = """
    1. Locations Table:
        - LocationID (INT PRIMARY KEY): A unique identifier for each location.
        - City (VARCHAR(100)): The name of the city.
        - Country (VARCHAR(100)): The name of the country.
        - Description (TEXT): A brief description of the location.

    2. Packages Table:
        - PackageID (INT PRIMARY KEY): A unique identifier for each travel package.
        - LocationID (INT): References LocationID in Locations table.
        - PackageName (VARCHAR(255)): The name of the travel package.
        - Price (DECIMAL(10, 2)): The price of the package.
        - DurationDays (INT): The duration of the trip in days.
        - Description (TEXT): A brief description of the package.

    3. Bookings Table:
        - BookingID (INT PRIMARY KEY): A unique identifier for each booking.
        - UserID (INT): References a user.
        - PackageID (INT): References PackageID in Packages table.
        - BookingDate (DATE): The date when the booking was made.
        - TravelDate (DATE): The date when the travel is scheduled.
        - Status (VARCHAR(50)): The status of the booking (e.g., "Confirmed", "Cancelled").
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": f"You are a helpful assistant that can covert query to SQL. return just the SQL for query.Given following tables in sql schema: <schemaInfo> "},
        #     {"role": "user", "content": question}
        # ]
        messages=[
        {"role": "system", "content": """You are a helpful assistant that can covert query to SQL. return just the SQL for query.Given following tables in sql schema: <schemaInfo> 
        1. Locations 
             Purpose: Stores information about various travel destinations.
            Key Data: Includes LocationID, city names, countries, and descriptions of each location.
        2. Packages 
             Purpose: Details of pre-arranged travel packages.
             Key Data: Includes PackageID, LocationID, names, descriptions, durationdays and prices.
        3. Bookings 
             Purpose: Records of bookings made by users.
             Key Data: Contains BookingID, references to UserID and PackageID, and dates of booking and travel.
        DDL for the tables is given below: 
         
        CREATE TABLE IF NOT EXISTS Locations (
            LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
            City VARCHAR(100),
            Country VARCHAR(100),
            Description TEXT
        );
         
        CREATE TABLE IF NOT EXISTS Packages (
            PackageID INTEGER PRIMARY KEY AUTOINCREMENT,
            LocationID INTEGER,
            PackageName VARCHAR(255),
            Price DECIMAL(10, 2),
            DurationDays INTEGER,
            Description TEXT,
            FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
        );
            
        CREATE TABLE IF NOT EXISTS Bookings (
            BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER,
            PackageID INTEGER,
            BookingDate DATE,
            TravelDate DATE,
            Status VARCHAR(50),
            FOREIGN KEY (PackageID) REFERENCES Packages(PackageID)
        );

        Relationships:
        the PackageDetails table acts as a junction table, connecting TravelPackages with ModesOfTravel, Activities, and ServiceProviders.
        The Bookings table links Users to their chosen TravelPackages,</schemaInfo> instruction to follow 1. Only return SQL query 2. use fields names specified for the table in schemaInfo. 3 use tables name speicified in the schemaInfo.; 5. recheck that the column names used are correct and matches with the schema passed
        for eg. if query to find out list of user names-> return SELECT `Name` FROM TravelPlannerDB.Users;  """},
        {"role": "user", "content": "Ensure that the column names used are only those which is passed. check that the column names and table names used are right.  {}".format(question)}
        ]
    )

    # Extracting the SQL query from the response
    # import pdb;pdb.set_trace()
    sql_query = completion.choices[0].message.content.strip()
    return sql_query

import os
from openai import OpenAI

def format_answer(question, answer):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=openai_api_key)

    # Prepare the prompt for GPT-3 to generate a user-friendly response
    prompt = f"Translate the following database answer into a detailed, user-friendly response based on the original question:\nQuestion: {question}\nAnswer from database: {answer}\nFormatted Answer:"

    print("\n\n\n")
    print(answer)
    if answer:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an insightful assistant, skilled in transforming raw data responses into clear, understandable language."},
                {"role": "user", "content": prompt}
            ]
        )
        formatted_response = completion.choices[0].message.content.strip()
    else:
        formatted_response = "It appears that the database did not provide a specific answer to your question. Let me Look that up online.\n"
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a travel agent."},
                {"role": "user", "content": prompt}
            ]
        )
        formatted_response += completion.choices[0].message.content.strip()

    return formatted_response


# Example usage

# openai_api_key = os.getenv("OPENAI_API_KEY")
# question = "What's the package cost in Paris?"
# sql_query = nl_to_sql(question, openai_api_key)
# print(sql_query)

# ss = execute_query(sql_query=sql_query)
# print(ss)

# formatted_response = format_answer(question=question, answer=ss)
# print(formatted_response)

