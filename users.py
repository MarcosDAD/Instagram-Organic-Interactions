import os
import mysql.connector
from mysql.connector import errorcode

import pytz
from datetime import datetime, timedelta
from datetime import date
import dateutil.parser

from dotenv import load_dotenv

class User(object):
    def __init__(self, id, username, password, regras_perfil, regras_tags, level, follower_limit, perfis, hashtags,
                 loop, index_limitador, genero, leads, lang, last_login, indexLocal):
        """ Initialize the object """
        self.id = id
        self.userdata = [username, password]
        self.r_perfil = regras_perfil
        self.r_tags = regras_tags
        self.ancoras = []
        self.indexLocal = indexLocal
        if len(perfis) > 0:
            for i in perfis:
                if len(i) > 0:
                    self.ancoras.append(i)
        if len(hashtags) > 0:
            for i in hashtags:
                if len(i) > 0:
                    self.ancoras.append(f'explore/tags/{i}')
        self.leads = leads
        self.level = level
        self.perfis = perfis
        self.hashtags = hashtags
        self.loop = loop
        self.velocidade = index_limitador
        self.genero = genero
        self.lang = lang

        self.last_login = last_login

class GetUsers:
    def __init__(self):
        load_dotenv()

        self.users = []
        self.profiles = []

        self.usuario = os.getenv('DB_user')
        self.senha = os.getenv('DB_pass')
        self.ip = os.getenv('DB_ip')
        self.db = os.getenv('DB_db')

    def DefineUsuario(self):
        self.mydb = mysql.connector.connect(user=self.usuario, password=self.senha, host=self.ip, database=self.db)
        self.cursor = self.mydb.cursor()

        if (len(self.users) > 0):
            self.users.clear()
        self.mydb.connect()
        #self.cursor = self.mydb.cursor(buffered=True)
        self.cursor.execute("select * from gerenciamento where velocidade > 0 ORDER BY lastlogin")
        records = self.cursor.fetchall()
        count = 0
        for row in records:
            split_perfis = []
            if row[12] != None:
                split_perfis = row[12].split(";")
            split_hashtags = []
            if row[13] != None:
                split_hashtags = row[13].split(";")
            langs = ""
            if row[20] != None:
                langs = row[20].split(",")
            data = 0
            if row[21] is not None and row[21] != "0":
                data = dateutil.parser.parse(row[21])
            hoje = datetime.now(pytz.utc)
            #data = hoje - timedelta(minutes=5)
            segundos = (hoje.replace(tzinfo=None) - data.replace(tzinfo=None)).total_seconds()
            if segundos:
                newUser = User(row[0], row[1], row[2], [row[3], row[4], row[5]], [row[6], row[7], row[8], row[9], row[10]],
                                row[11], 0, split_perfis, split_hashtags, row[15], row[16], row[17], [row[18], row[19]], langs, data, count)
                self.users.append(newUser)
                self.profiles.append(newUser)
            count+=1
        self.cursor.close()
        self.mydb.close() 

    def Updating(self, userId, userTime):
        minutes = int(os.getenv('Delay_user'))
        delay = userTime + timedelta(minutes=minutes)
        

        self.mydb = mysql.connector.connect(user=self.usuario, password=self.senha, host=self.ip, database=self.db)
        self.cursor = self.mydb.cursor(buffered=True)
        self.mydb.connect()
        sql = """UPDATE gerenciamento SET lastlogin = %s WHERE id = %s"""
        val = (delay, userId,)
        self.cursor.execute(sql, val)
        self.cursor.execute('COMMIT')
        self.cursor.close()
        self.mydb.close()

        print(delay)
    
    def Leveling(self, userId, userLevel):
        if userLevel <= 80:
            userLevelLocal = userLevel + 1
            self.mydb = mysql.connector.connect(user=self.usuario, password=self.senha, host=self.ip, database=self.db)
            self.cursor = self.mydb.cursor(buffered=True)
            self.mydb.connect()
            sql = """UPDATE gerenciamento SET level = %s WHERE id = %s"""
            val = (int(userLevelLocal), userId,)
            self.cursor.execute(sql, val)
            self.cursor.execute('COMMIT')
            self.cursor.close()
            self.mydb.close()
