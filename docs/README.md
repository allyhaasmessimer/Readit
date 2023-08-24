# READIT

Readit is an application that leverages the capabilities of a third-party API, specifically the Google Books API. Users visiting the site can effortlessly explore a wide variety of books using the extensive resources offered by the Google Books API. By creating an account and logging in, users unlock the ability to build two distinct lists: a wish list cataloging books they aspire to read, and a comprehensive record of books they have already read. This personalized environment allows users to manage their literary interests with ease and precision.

## Design

-   [API design](api-design.md)
-   [Data model](data-model.md)
-   [Integrations](integrations.md)
-   [GHI](ghi.md)

## Intended market

ReadIt is your go-to app for all things related to books. Designed to enhance your reading experience, ReadIt allows you to seamlessly explore a vast collection of books using the Google Books API. Whether you're an avid reader or just starting your literary journey, ReadIt is here to make your reading adventures more enjoyable and organized.

Key Features:

Discover and Explore: Dive into the world of literature by searching for books using the Google Books API. Explore a wide range of genres, authors, and titles to find your next captivating read.

Personalized Accounts: Create your own ReadIt account to unlock a personalized reading journey. With your account, you can build a collection of books you've read and ones you're eager to explore.

Read Log: Keep track of your reading accomplishments by adding books to your read log. Easily see a history of books you've completed, allowing you to reflect on your reading journey.

Want to Read List: Never forget a book you're excited to read! Maintain a dynamic "Want to Read" list that keeps all your desired books in one convenient location.

Effortless Book Management: ReadIt provides a user-friendly interface to manage your read log and want to read list. Mark books as "read" with a simple click or tap.

Stay Organized: ReadIt ensures your reading experience is organized and enjoyable. No matter your reading pace or preferences, you can manage your literary adventures effortlessly.

Whether you're a book enthusiast, a casual reader, or simply want to stay connected with the world of literature, ReadIt is your ultimate companion. Download ReadIt now and embark on a journey of literary exploration like never before. Happy reading!

## Functionality

For Guests:

Signup & Login: Create an account to access personalized reading and literary treasures.
Google Book Search: Explore a vast collection of books using Google Books API.

For Logged-In Users:

Google Book Search: Discover books matching your interests using the Google Books API.
Personal Reading Lists: Organize with "Want to Read" and "Read" lists.
Add to Lists: Easily add books from search results to your lists.
Move Between Lists: Transition books from "Want to Read" to "Read."
Delete from Lists: Remove books effortlessly from your lists.
Logout: Ensure privacy and return whenever you're ready.
Add a Book Review: Write what you thought about a book.
Delete a Book Review.

## Project Initialization

To fully enjoy this application on your local machine, please make sure to follow these steps:

1. Clone the repository down to your local machine
2. CD into the new project directory
3. Create the database with postgres
4. python manage.py runserver
