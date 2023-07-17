import sqlite3 as sq


class DataBaseFeedback:
    @staticmethod
    async def db_start():
        global db, cur

        db = sq.connect("feedback.db")
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, email TEXT, message TEXT)")
        db.commit()

    @staticmethod
    async def create_feedback(user_id):
        user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
        if not user:
            cur.execute("INSERT INTO profile VALUES(?, ?, ?)", (user_id, '', ''))
            db.commit()

    @staticmethod
    async def edit_feedback(state, user_id):
        async with state.proxy() as data:
            cur.execute(
                "UPDATE profile SET email = '{}', "
                "message = '{}' WHERE user_id == '{}'".format(data['email'], data['message'], user_id)
            )
            db.commit()
