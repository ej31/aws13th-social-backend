from repositories.user_repo import get_all_users_db

con=get_all_users_db()
for user in con:
    print(user)