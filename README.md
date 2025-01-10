## Overview
The **Board Game Cafe** project is a Django-based application made for managing reservations at a board game cafe and browsing available games. This application tries to simplify the reservation process by providing users with an easy to read interface and comfortable tools for admins.

## Why This Application Was Created
From my personal experience, I have always found the need to manually call a cafe just to reserve a table troublesome and needless. My application was designed to address this problem by offering:
- A simple and user-friendly interface to make reservations and browse available games with their details
- A straightforward backend to handle game and table availability
- Admin tools to simplify the management of reservations and games in the database

## Features
- **User Authentication**: Users can register, log in, and log out
- **Game Catalog**: Users can browse available board games with detailed information, eg. player count
- **Reservations**: Users can reserve a table and a specific games online via a simple form
- **Admin Panel**: Admins can manage games, tables, and reservations in an easy way

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd board_game_cafe
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database settings in `settings.py` to connect to PostgreSQL
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser for admin:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Access the application in your browser at `http://127.0.0.1:8000/`
2. Register as a new user or log in if your user already exists
3. Browse the game list to see available board games
4. Go to the reservation page to book a table and a game
5. Admins can log in to the admin panel at `http://127.0.0.1:8000/admin` to manage the cafe

## FAQ
**Q: Can I use a different database backend?**
A: PostgreSQL is recommended, but you can change the settings in `settings.py` to use SQLite for example

**Q: How can I reset my password?**
A: Contact the admin, the reset password feature is not available yet

## Structure
- **board_game_cafe**: Core Django settings and URLs
- **cafe_website**: Main folder with models, views etc.
- **templates**: HTML templates for the interface
- **static**: Static files with CSS for styling

## API Documentation
This application uses BGG XML API2 for adding games easily. For more information go to: (https://boardgamegeek.com/wiki/page/BGG_XML_API2)

## Requirements
- Python 3.10+
- Django 4.x
- PostgreSQL

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE).


