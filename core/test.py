from repositories.user_repo import get_users_db

con=get_users_db()
for user in con:
    print(user)