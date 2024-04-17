# Django TechCrunch Scraper 

This project is a web application built with Django, utilizing the requests and Beautiful Soup 4 (bs4) libraries for web scraping. It allows users to sign up, log in, and enter a specific Goodreads URL. The application then scrapes 
post, category, author information from the techcrunch website and store the to database and user can see them in django admin panel. 
## Features

- Scraping Articles: Extracts articles from the TechCrunch website, including titles, URLs, authors, categories, images, and descriptions.
- Scraping Authors: Retrieves information about authors, including their names, positions, and avatars.
- Scraping Categories: Collects data about article categories for better organization and analysis.
- Keyword-based Search: Allows users to perform searches based on keywords, fetching relevant articles and providing insights into trending topics.
- User Authentication: Supports user authentication to ensure secure access to the application.
- Admin Interface: Provides an admin interface for managing articles, authors, categories, and search requests.
- Data Visualization: Generates visualizations such as charts and graphs to help users analyze the scraped data effectively.
- Daily Updates: Automatically updates article, category, and author data on a daily basis, ensuring that users have access to the latest information.
- Export and Import: Supports exporting and importing data in various formats, facilitating data exchange and backup.

## Install the required dependencies:

1. Clone the repository:

        git clone https://github.com/rezaty76/techcrunch_scraper_django.git

2. Install the required dependencies:

         pip install -r requirements.txt 

3. Set up the database configuration in the local_setting.py file.

## Configuration:
Before running the application, ensure that you have configured the database connection settings in the
local_setting.py file.

## Logging
The application logs information, errors, and other messages to both a file (celery.log) in logs directory and the console.

## Setting Up the Database
Run the following commands to set up your database: 

      python manage.py makemigrations


      python manage.py migrate


## Running the Application 
To start the server, run: 

      python manage.py runserver

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License
TechCrunch Scraper is licensed under the MIT License.

