from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_reg_users(self):
        sql = """CREATE TABLE IF NOT EXISTS Reg_Users (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        phone_number VARCHAR(15) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL UNIQUE
        );
        """

        await self.execute(sql, execute=True)

    async def create_table_signin_users(self):
        sql = """CREATE TABLE IF NOT EXISTS Signin_Users (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        reg_user_id INTEGER NOT NULL,
        phone_number VARCHAR(15) NOT NULL,
        password VARCHAR(255) NOT NULL
        );
        """

        await self.execute(sql, execute=True)
    
    async def create_table_malumotlar(self):
        sql = """CREATE TABLE IF NOT EXISTS Malumotlar (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        reg_user_id INTEGER NOT NULL,
        malumot_text TEXT NULL,
        img text NULL,
        created_at TIMESTAMP DEFAULT NOW()
        );
        """

        await self.execute(sql, execute=True)

    async def add_malumot(self, user_id, reg_user_id, malumot_text=None, img=None):
        sql = "INSERT INTO Malumotlar (user_id, reg_user_id, malumot_text, img) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, user_id, reg_user_id, malumot_text, img, fetchrow=True)
    
    async def select_malumotlar(self, **kwargs):
        sql = "SELECT * FROM Malumotlar WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)
    
    async def select_signin_user(self, **kwargs):
        sql = "SELECT * FROM Signin_Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_signin_user(self, user_id, reg_user_id, phone_number, password):
        sql = "INSERT INTO Signin_Users (user_id, reg_user_id, phone_number, password) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, user_id, reg_user_id, phone_number, password, fetchrow=True)

    async def add_reg_user(self, user_id, phone_number, password):
        sql = "INSERT INTO Reg_Users (user_id, phone_number, password) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, user_id, phone_number, password, fetchrow=True)
    
    async def select_reg_user(self, **kwargs):
        sql = "SELECT * FROM Reg_Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_info_reg_user(self, phone_number, password):
        sql = "SELECT * FROM Reg_Users WHERE phone_number=$1 AND password=$2"
        return await self.execute(sql, phone_number, password, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
