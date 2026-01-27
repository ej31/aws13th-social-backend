from fastapi import HTTPException


def get_all_comments_db(db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM comments")
            return cursor.fetchall()

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
       db.rollback()
       print(f"Service Error: {e}")
       raise HTTPException(status_code=500, detail="Internal Server Error")


def get_comment_by_id(db,comment_id):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE comment_id = %s", (comment_id,))
            return cursor.fetchone()

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
       db.rollback()
       print(f"Service Error: {e}")
       raise HTTPException(status_code=500, detail="Internal Server Error")
