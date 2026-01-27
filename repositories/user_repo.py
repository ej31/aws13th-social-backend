
from fastapi import HTTPException

def get_user_by_id(db, user_id):
    try:
       with db.cursor() as cursor:
            cursor.execute("SELECT user_id, email, nickname, profile_image_url FROM users WHERE user_id = %s", (user_id,))
            return cursor.fetchone()

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
       db.rollback()
       print(f"Service Error: {e}")
       raise HTTPException(status_code=500, detail="Internal Server Error")



