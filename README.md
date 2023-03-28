# PasswordManager
This password manager takes users' Master Password and username as input to access the users' database.
---
When the user has access, it can utilize different functionalities:
- Show all passwords
- Enter an existing password to the database
- Create a new password, randomly generated and secure
- Update an existing password
- Update a username
- Delete an entry
---
The passwords are encrypted with SHA-256, the key being generated with the hash of the master password, meaning that entries can only be decrypted if the user has access to the master password.
If someone malicious happened to gain access to the locally stored .db file, they would not be able to decrypt any of the entries due to them not having access to the master password.
The GUI is simple and intuitive, created with Tkinter.
In order to store passwords and master passwords I used a SQLite database for simplicity, on account of the fact that this won't need to scale much, since it is not likely to have many users on the same database.
---
In order to install it and use it, one can clone the repository and create an executable file with main.py.
