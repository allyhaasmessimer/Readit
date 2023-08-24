### «Human-readable of the endpoint»

### Log in

-   Endpoint path: /login/
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

-   Endpoint path: /token
-   Endpoint method: DELETE

-   Headers:

    -   Authorization: Bearer token

-   Response: Always true
-   Response shape (JSON):
    ```json
    true
    ```
