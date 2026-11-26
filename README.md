# CineTicket - CS50x Final Project

#### Video Demo: https://youtu.be/jypJSmFjGGo

#### Description:
CineTicket is a comprehensive, full-stack web application designed for cinema management and online ticket booking, built from scratch as the final capstone project for CS50x using Python, Flask, Jinja2 templates, Bootstrap 5, and a robust SQLite database named cinema.db. The application provides secure user authentication and role-based access control, supporting distinct user roles for regular customers and a pre-configured administrator.

Authorized administrators have exclusive access to management tools allowing them to dynamically insert new movie titles, descriptions, and durations into the database, as well as schedule new screenings specifying showtimes, pricing, and format tags such as 2D or 3D. Regular customers are greeted with a dynamic dashboard showcasing all currently available movie screenings complete with descriptions, showtimes, format badges, and ticket prices. Users can seamlessly book seats by selecting their preferred row ranging from A to Z and their seat number ranging from 1 to 35. Furthermore, the backend includes automated double-booking prevention ensuring that no two users can claim the exact same seat for the same screening. Customers can also review all their past and active ticket reservations at any time through a dedicated history page displaying comprehensive details including movie titles, screen types, seat assignments, prices, and purchase timestamps.

Regarding design choices, Flask was chosen for its lightweight and flexible nature, making it ideal for a medium-scale web application. SQLite was selected as the database backend due to its simplicity and seamless integration with Python via standard libraries or lightweight wrappers. Bootstrap 5 was integrated to ensure a clean, modern, and fully responsive user interface across all devices.

As for the file structure and implementation details, each component plays a crucial role in the application:
- `app.py`: Contains all the core Flask routes, backend business logic, session handling, user authentication, and custom decorators like login_required and admin_required.
- `cinema.db`: The SQLite relational database storing tables for users, movies, screenings, and booked tickets.
- `templates/layout.html`: The base layout template containing the navigation bar, footer, and common Bootstrap imports.
- `templates/index.html`: The home page displaying the list of available movies and upcoming screenings for users to browse and book.
- `templates/login.html`: The user login page with form validation.
- `templates/register.html`: The user registration page allowing new accounts to be created securely.
- `templates/history.html`: Displays the booking history and ticket reservations for logged-in customers.
- `templates/add_movie.html`: An admin-only interface for adding new movies into the database.
- `templates/add_screening.html`: An admin-only interface for scheduling new movie screenings with specific showtimes, prices, and formats.
- `templates/apology.html`: Renders friendly error messages whenever an invalid request or unauthorized access occurs.

//venv\Scripts\activate
//python -m flask run