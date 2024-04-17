from database import Database


from dbconfig import host, user, password, db_name, port


database_ = Database(
            host=host,
            user=user,
            password=password,
            db_name=db_name,
            port=port)


a = database_.get_ids()

print(a)