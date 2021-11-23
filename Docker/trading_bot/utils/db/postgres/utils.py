from sqlalchemy.sql import func as sa_func
from sqlalchemy import select, insert, values, delete, update


async def db_max_id(conn, Table, default=0, max_plus_one=False):
    """
    if no rows use default
    else max id of rows (max + 1 if max_plus_one)
    """
    id = (await (await conn.execute(select(sa_func.max(Table.id)))).fetchone())[0]
    if id:
        return id if not max_plus_one else id + 1
    else:
        return default