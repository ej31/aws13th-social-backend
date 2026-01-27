from fastapi import HTTPException

def get_all_posts(db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM posts")
            return cursor.fetchall()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
       db.rollback()
       print(f"Service Error: {e}")
       raise HTTPException(status_code=500, detail="Internal Server Error")

def get_post_by_id(db,post_id):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
            return cursor.fetchone()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
       db.rollback()
       print(f"Service Error: {e}")
       raise HTTPException(status_code=500, detail="Internal Server Error")

