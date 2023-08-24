# Data models
### User

| name         | type           | unique | optional |
| ------------ | -------------- | ------ | -------- |
| id           | SERIAL         | yes    | no       |
| email        | EMAILFIELD     | yes    | no       |
| username     | CHARFIELD(150) | yes    | no       |
| hashed pwd   | CHARFIELD(150) | no     | no       |


The `users` table contains the data about a specific user.

### Book

| name             | type           | unique | optional |
| ---------------- | -------------- | ------ | -------- |
| id               | SERIAL         | yes    | no       |
| title            | CHARFIELD(200) | no     | no       |
| author           | CHARFIELD(100) | no     | no       |
| cover_image_url  | CHARFIELD      | no     | yes      |
| description      | CHARFIELD(600) | no     | no       |
| external_id      | CHARFIELD(100) | no     | yes      |

The `books` table contains the data about a specific book.

### UserProfile

| name               | type           | unique | optional |
| ------------------ | -------------- | ------ | -------- |
| user               | FOREIGN KEY    | yes    | no       |
| books_read         | MANYTOMANY     | no     | yes      |
| books_want_to_read | MANYTOMANY     | no     | yes      |

The `user profile` table contains the data about a specific user profiles reading list. user is a foreign key.

### review

| name         | type          | unique | optional |
| ------------ | ------------- | ------ | -------- |
| id           | SERIAL        | yes    | no       |
| review_text  | TextField     | no     | no       |
| date_posted  | DateTimeField | no     | yes      |
| book         | FOREIGN KEY   | no     | no       |
| user         | FOREIGN KEY   | no     | no       |

The `review` table contains the data about a specific users book review. Foreign Keys to book and user.
