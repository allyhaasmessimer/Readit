### «Human-readable of the endpoint»

### Sign up

-   Endpoint path: signup/
-   Endpoint method: POST

-   Request shape (form):

    -   email: string
    -   username: string
    -   password: string

-   Response: True
-   Response shape (JSON):
    ```json
    {
      "token": string
    }
    ```

### Log in

-   Endpoint path: login/
-   Endpoint method: POST

-   Request shape (form):

    -   username: string
    -   password: string

-   Response: Account information and a token
-   Response shape (JSON):
    ```json
    {
      "token": string
    }
    ```

### Log out

-   Endpoint path: logout/
-   Endpoint method: POST

-   Headers:

    -   Authorization: Bearer token

-   Response: Always true
-   Response shape (JSON):
    ```json
    {
        "message": "Logged out successfully."
    }
    ```

### Add User Profile

-   Endpoint path: add_user_profile/
-   Endpoint method: POST

-   Headers:

    -   Authorization: Bearer token

-   Request shape (JSON):

    ```json
    {
        "user": "",
        "books_read": [""],
        "books_want_to_read": [""]
    }
    ```

-   Response: True

-   Response shape (JSON):
    ```json
    {
        "message": "User profile updated successfully."
    }
    ```

### User Profile List

-   Endpoint path: list/
-   Endpoint method: GET

-   Headers:

    -   Authorization: Bearer token

-   Response: List of books read and list of books want to read

-   Response shape (JSON):

        ```json
        {
        "username": "t",
        "books_read": [
        	{
        		"id": int,
        		"title": ""
        	},
        	{
        		"id": int,
        		"title": ""
        	},
        ],
        "books_want_to_read": [
        	{
        		"id": int,
        		"title": ""
        	},F
        ]

    }

    ```

    ```

### Google Book API Search

-   Endpoint path: search/
-   Endpoint method: GET
-   Query parameters:

    -   q: the book(s) to search for by topic, author, title, keyword, ect.

-   Headers:

    -   None - you do not need an account for this view

-   Response: Book details that meet filter parameters

-   Response shape (JSON):

    ```json
    {
    	"id": "",
    	"volumeInfo": {
    		"title": "",
    		"authors": [
    			""
    		],
    		"description": "",
    		"imageLinks": {
    			"smallThumbnail": "",
    		},
    	},

    	"searchInfo": {
    		"textSnippet": ""
    	}
    },
    ```

    ### Add Book To Want to Read List

-   Endpoint path: want_to_read/<str:book_id>/
-   Endpoint method: POST

-   Headers:

    -   Authorization: Bearer token

-   Response: Add book to list

-   Response shape (JSON):

    ```json
    {
        "message": "Book added to your teetee 'want to read' list."
    }
    ```

    ### Add or Move Book To Read List

-   Endpoint path: read/<str:book_id>/
-   Endpoint method: POST

-   Headers:

    -   Authorization: Bearer token

-   Response: Add or move book to read list

-   Response shape (JSON):
    ```json
    {
        "message": "Book marked as 'read' and moved to your 'read' list."
    }
    ```

### Delete Book From Want To Read List

-   Endpoint path: delete_want_to_read/<int:pk>/
-   Endpoint method: POST

-   Headers:

    -   Authorization: Bearer token

-   Response: Remove book from want to read list

-   Response shape (JSON):
    ```json
    {
        "message": "{book title} removed from {user profile}"
    }
    ```

### Delete Book From Read List

-   Endpoint path: delete/<int:pk>/
-   Endpoint method: POST

-   Headers:

    -   Authorization: Bearer token

-   Response: Remove book from read list

-   Response shape (JSON):
    ```json
    {
        "message": "{book title} removed from {user profile}"
    }
    ```
