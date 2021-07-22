import aiosqlite

import config


class SQL:
    def __init__(self):
        self.connection = aiosqlite.connect(config.database_name)

    async def create(self, add_mass):
        """ Создает новую строку в таблице """
        async with self.connection as db:
            if not add_mass[0]:
                await db.executemany(
                    "INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?);".format('passwords_table'),
                    [(None, add_mass[1], add_mass[2], add_mass[3], add_mass[4], add_mass[5], add_mass[6])]
                )
                await db.commit()
            else:
                await db.execute(
                    "UPDATE {} SET name=?, nickname=?, email=?, password=?, links=?, tags=? WHERE id = ?".format('passwords_table'),
                    [(add_mass[1], add_mass[2], add_mass[3], add_mass[4], add_mass[5], add_mass[6])])
                await db.commit()

            async with db.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1;".format('passwords_table')) as cursor:
                async for row in cursor:
                    return row[0]

    async def delete(self, where_id):
        """ Удаляем строку """
        async with self.connection as db:
            await db.execute("DELETE FROM {} WHERE {} = {};".format('passwords_table', 'id', where_id))
            await db.commit()

            async with db.execute('select rowid, * from passwords_table;') as cursor:
                async for row in cursor:
                    print(row)
