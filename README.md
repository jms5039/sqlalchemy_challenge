# Honolulu Vacation Planner

Congratulations on deciding to treat yourself to a long holiday vacation in Honolulu, Hawaii! This project is designed to assist you in planning your trip by providing a climate analysis and exploration of the area.

## Part 1: Climate Analysis and Data Exploration

### Jupyter Notebook Database Connection

- **Connect to SQLite Database:**
  - Use the `create_engine()` function from SQLAlchemy to connect to your SQLite database.
  
- **Reflect Tables into Classes:**
  - Use `automap_base()` to reflect your tables (station and measurement) into classes.
  - Save references to these classes.

- **Create a Session:**
  - Create a session to link Python to the database.

- **Close the Session:**
  - Remember to close the session at the end of your notebook.

### Precipitation Analysis

- **Find the Most Recent Date:**
  - Write a query to find the most recent date in the dataset.

- **Get Last 12 Months of Precipitation Data:**
  - Using the most recent date, query the previous 12 months of precipitation data.
  - Select only "date" and "prcp" values.

- **Load Data into Pandas DataFrame:**
  - Load the query results into a Pandas DataFrame, explicitly setting column names.

- **Sort DataFrame:**
  - Sort the DataFrame values by "date".

- **Plot Results:**
  - Use the DataFrame plot method to plot the results.

- **Print Summary Statistics:**
  - Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

- **Calculate Total Number of Stations:**
  - Design a query to calculate the total number of stations.

- **Find Most Active Station:**
  - List stations and observation counts in descending order.
  - Identify the station with the greatest number of observations.

- **Calculate Temperature Statistics:**
  - Design a query to calculate the lowest, highest, and average temperatures for the most-active station.

- **Get Last 12 Months of TOBS Data:**
  - Design a query to get the previous 12 months of temperature observation (TOBS) data for the most-active station.

- **Plot Histogram:**
  - Plot the results as a histogram with bins=12.

- **Close the Session:**
  - Close your session.

## Part 2: Design Your Climate App

### SQLite Connection & Landing Page

- **Generate Engine:**
  - Correctly generate the engine to the correct SQLite file.

- **Reflect Database Schema:**
  - Use `automap_base()` to reflect the database schema.

- **Save References to Tables:**
  - Save references to the tables in the SQLite file (measurement and station).

- **Create and Bind Session:**
  - Create and bind the session between the Python app and the database.

- **Display Available Routes:**
  - Display the available routes on the landing page.

### Static Routes

- **Precipitation Route:**
  - Return JSON with date as the key and precipitation as the value.
  - Only return the JSONified precipitation data for the last year in the database.

- **Stations Route:**
  - Return JSONified data of all the stations in the database.

- **TOBS Route:**
  - Query the dates and temperature observations of the most-active station for the previous year of data.
  - Return a JSON list of temperature observations for the previous year.

### Dynamic Route

- **Start Route:**
  - Accept the start date as a parameter from the URL.
  - Return the min, max, and average temperatures calculated from the given start date to the end of the dataset.

- **Start/End Route:**
  - Accept the start and end dates as parameters from the URL.
  - Return the min, max, and average temperatures calculated from the given start date to the given end date.

## Coding Conventions and Formatting

- **Code Formatting:**
  - Place imports at the top of the file.
  - Name functions and variables with lowercase characters, using underscores.
  - Follow DRY principles and use concise logic.

## Deployment and Submission

- **GitHub Repository:**
  - Submit a link to a GitHub repository that's cloned to your local machine and contains your files.
  - Use the command line to add your files to the repository.
  - Include appropriate commit messages in your files.

## Comments

- **Well-commented Code:**
  - Ensure that your code is well-commented with concise, relevant notes that other developers can understand.
