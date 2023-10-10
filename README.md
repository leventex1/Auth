# Auth service

This is a basic implementation of a auth microservice. 
<br><br><br>

## Project overview:
This api register users in a database, and handles the authentication and authorization process with access- and refresh- token pairs. <b>Only one refresh token can reference a user at a time.</b>



## Project dependencies:

1. install requirements:
<code>pip install -r requirements.txt</code>
<br><br>

2. Create a database that has at least these tables with at least these column types:
```python
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    refresh_token: Mapped['RefreshToken'] = relationship(back_populates='user')

class RefreshToken(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=True, default=None)
    valid_until: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None, onupdate=get_expiration_refresh_token)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='refresh_token')
```
The whole api is operate on these data models.
<br><br>

3. Configure the application: <br>
<li>
    Set the config file's path relative to the .srvice module in an enviroment variable as AUTH_SERVICE_CONFIG
</li>
<li>
    Enviroment variables should contain at least: <br>
    SQLALCHEMY_DATABASE_URI: database uri <br>
    SECRET_KEY: app secret key <br>
    ACCESS_EXP_MINUTES: access token expiration in minutes <br>
    REFRESH_EXP_DAYS: refresh token expiration in days
</li>
<br><br>



## API endpoints:

### 1. Register user in database <code>/auth/user POST</code>

> | request data | constrains |
> | ------------ | ---------- |
> | email        | string     |
> | password     | string     |

Generates a user row in a database if the email is not exists in it. Hashes the password.

> | response data | value        | http code  |
> | ------------- | ----------   | ---------- |
> | message       | Invalid data | 400        |
> | message       | User already exists | 409 |
> | message       | User created | 200 |
<br>



### 2. Log in user <code>/auth/user/ PUT</code>

> | request data | constrains |
> | ------------ | ---------- |
> | email        | string     |
> | password     | string     |

Checks if the user exsits and the parameters are correct.
Issues access/refresh token pair.

> | response data | value        | http code  |
> | ------------- | ----------   | ---------- |
> | message       | Invalid data | 400        |
> | message       | User not found | 404 |
> | (1) message, (2) access_token, (3) refresh_token       | (1) User logged in, (2) str, (3) str | 200 |
<br>



### 3. Validate access token <code>/auth/user/access_token/{access_token} GET</code>

> | request param | constrains |
> | ------------- | ---------- |
> | access_token  | string     |

Checks if the access token is valid and return the referenced user_id.

> | response data | value        | http code  |
> | ------------- | ----------   | ---------- |
> | message       | Access token is not valid | 401 |
> | (1) message, (2) user_id       | (1) Access token is valid, (2) int | 200 |
<br>



### 4. Issue new access/refresh token pair <code>/auth/user/refresh_token/{refresh_token} GET</code>

> | request param  | constrains |
> | -------------- | ---------- |
> | refresh_token  | string     |

Checks if the refresh_token is valid and issue a new access/refresh token pair referencing the user and update the refresh token in the database.

> | response data | value        | http code  |
> | ------------- | ----------   | ---------- |
> | message       | Refresh token is not valid | 401 |
> | (1) message, (2) access_token, (3) refresh_token | (1) New access/Refresh token pair issued, (2) int, (3) int | 200 |