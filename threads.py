import os
import threading
import time
import pytz
from datetime import datetime, timedelta
from datetime import date
import dateutil.parser
import random

from users import GetUsers
from discord import Discord

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.remote import switch_to
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

profile_path = r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\y1uqp5mi.default'
options=Options()
#options.set_preference('profile', profile_path)
options.headless = False
service = Service(__location__+"\Gecko\geckodriver.exe")

link_local = "https://instagram.com/accounts/login/"

class NewThread (threading.Thread):
    def __init__(self, queue):
        self.queue = queue

    def Single(self):
        while len(self.queue) > 0:
            localLevel = self.queue[0].level

            self.username = self.queue[0].userdata[0]

            self.multiplicador = max(10, localLevel * 0.35)
            self.interacao_atual = 0
            self.interacaoMax = random.randint(int(self.multiplicador * 0.9), int((self.multiplicador + 1) * 1.1))
            print(self.interacaoMax)

            self.index_tags = 0
            self.ancoras = self.queue[0].ancoras

            self.hashtags = 0

            self.history = []

            print(f'Starting the user {self.queue[0].userdata[0]}')

            self.Login()
            self.lastLike = time.time()
            time.sleep(2)

            for i in range(self.index_tags, len(self.ancoras)):
                if self.interacao_atual < self.interacaoMax:
                    #DiscordConexao(f"{self.username} está vasculhando {self.ancoras[i]}")
                    try:
                        self.Target(self.ancoras[i])
                    except Exception as e:
                        print(e)
                    #self.somado += 1
                    time.sleep(8)

            print(f'Closing the user {self.queue[0].userdata[0]}')

            self.driver.close()
            localUsers = GetUsers()
            localUsers.Leveling(self.queue[0].id, self.queue[0].level)
            time.sleep(2)
            del self.queue[0]
            print(f'Current queue size: {len(self.queue)}')
            time.sleep(120)
        print(f'Thread finalizada')
        return

    def Login(self):
        self.driver = Firefox(service=service, options=options)
        self.driver.get(link_local)
        time.sleep(2)

        #lblUser = driver.find_element_by_xpath("//input[@name='username']")
        lblUser = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
            )
        lblUser.click()
        lblUser.clear()
        lblUser.send_keys(self.queue[0].userdata[0])
        time.sleep(2)
        #lblPass = driver.find_element_by_xpath("//input[@name='password']")
        lblPass = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
            )
        lblPass.click()
        lblPass.clear()
        lblPass.send_keys(self.queue[0].userdata[1])
        time.sleep(1)

        lblPass.send_keys(Keys.RETURN)

        logo = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img"))
            )

        localUsers = GetUsers()
        localUsers.Updating(self.queue[0].id, self.queue[0].last_login)

        self.discord = Discord()
        msg = f'{self.username} has connected'
        self.discord.LoginLog(msg)

    def Target(self, alvo):
        self.alvo = alvo
        driver = self.driver
        driver.get("https://www.instagram.com/" + alvo + "/")

        if 'explore' in alvo:
            self.tipo = 1
            rnd = random.randint(16, 38)
            time.sleep(rnd)
            if self.interacao_atual < self.interacaoMax:
                self.Hashtag()
    
    def Like(self):
        driver = self.driver

        #btnLike = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button")
        btnLike = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "._aamw > button:nth-child(1)"))
        )
        #btnLike = driver.find_elements_by_css_selector("button.fr66n > button:nth-child(1)")
        btnLike.click()

        timeToLike = time.time() - self.lastLike
        print(f'{self.username} - Like {self.interacao_atual} - {int(timeToLike)} secs')
        self.lastLike = time.time()
        
    def Hashtag(self):
        driver = self.driver
        alvo = self.alvo

        #hrefs = driver.find_elements_by_tag_name('a')
        hrefs = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        pics_hrefs = [elem.get_attribute('href')for elem in hrefs]
        pics_filter = [n for n in pics_hrefs if '/p/' in n]
        rnd = random.randint(0, 2)
        i = 9
        contador = 0
        max_contador = 30
        print(f'Posts dessa hashtag {len(pics_filter)}')
        while i < 29:
            driver.get(pics_filter[i])
            rnd = random.randint(10, 15)
            time.sleep(rnd)

            idioma = 'None'
            prof = 0
            frases = []

            # try:
            #     teste = driver.find_elements_by_tag_name('span')
            #     autor = teste[0].text
            #     if autor == "":
            #         autor = teste[1].text
            #     desc = teste[10].text
            #     cont = 0
            #     index = 0
            #     for z in range (len(teste)):
            #         if teste[z].text == autor:
            #             if (cont == 1):
            #                 index = z + 1
            #             cont += 1
            #     if index > 0:
            #         desc = teste[index].text
            #         lang = detect_langs(desc)
            #         lang = str(lang[0])
            #         idioma = lang[:2]
            #         prof = float(lang[3:]) * 100
            #         for index_comments in range (len(self.lst_comments)):
            #             if self.lst_comments[index_comments][idioma] != "":
            #                 frases.append(self.lst_comments[index_comments][idioma])
            # except Exception as e:
            #     erro = e

            if self.interacao_atual >= self.interacaoMax:
                i = 1000
            if self.interacao_atual < self.interacaoMax:
                rnd = random.randint(5, 12)
                time.sleep(rnd)
                curtido = False
                self.hashtags += 1

                if self.queue[0].r_tags[0]:
                    #btnLike = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button")
                    btnLike = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "._aamw > button:nth-child(1) > div:nth-child(1)"))
                    )
                    #print(btnLike.get_property("class"))
                    color = btnLike.get_property("innerHTML")
                    if "Unlike" in color or "unlike" in color:
                        curtido = True
                    if curtido:
                        i += 5
                    if not curtido:
                        self.Like()
                        self.interacao_atual += 1
                        self.ultima_interacao = time.time()
                        msg = f"{self.username} liked the post [{pics_filter[i][28:]}]. More {self.interacaoMax - self.interacao_atual} to finish ({self.interacao_atual})"
                        self.discord.thread1_webhook(msg)
                        #op = driver.find_element_by_css_selector(".e1e1d > span:nth-child(1) > a:nth-child(1)")
                        op = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "a.qi72231t"))
                        )
                        usuario = op.get_attribute('href')[26:]
                        newusr = usuario.replace("/", "")
                        self.history.append(newusr)
                        rnd = random.randint(13, 19)
                        #self.Dispose()

                        time.sleep(rnd)
                # if self.queue[0].r_tags[1]:
                #     if not users[self.index_user].r_tags[0] or (users[self.index_user].r_tags[0] and not curtido and len(frases) > 0):
                #         self.Comentar(frases)
                #         self.interacao_atual += 1
                #         self.ultima_interacao = time.time()
                #         self.Dispose()
                #         DiscordMessage(f"{self.username} fez um comentário na postagem [{pics_filter[i]}]", self.tipo_id)

                
                ##c_name = driver.find_elements_by_css_selector("a._2dbep.qNELH.kIKUG")
                c_name = []
                try:
                    #c_name = EC.presence_of_all_elements_located(By.CLASS_NAME, "._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abbh._abcm")
                    c_content = driver.find_elements(By.CSS_SELECTOR, "ul._a9ym")
                    c_name = []
                    for i in range (0, len(c_content)):
                        c_name.extend(c_content[i].find_elements(By.CSS_SELECTOR, "a.qi72231t"))
                except TimeoutException as e:
                    print('Nothing found in the table.')
                lista = []
                # print name
                for x in range(0, len(c_name)):
                    usuario = c_name[x].get_attribute('href')[26:]
                    newstr = usuario.replace("/", "")
                    if newstr not in self.history and newstr != self.username:
                        lista.append(newstr)
                lista = list(dict.fromkeys(lista))
                self.Perfil(lista)
                contador += 1
                if contador >= max_contador:
                    i = 1000
            i += 1
    def Perfil(self, lista):
        driver = self.driver
        for i in range(len(lista)):
            tempo = time.time()
            self.history.append(lista[i])
            driver.get("https://www.instagram.com/" + lista[i] + "/")
            rnd = random.randint(8, 16)
            time.sleep(rnd)
            #hrefs = driver.find_elements_by_tag_name('a')
            hrefs = driver.find_elements(By.TAG_NAME, "a")
            pics_hrefs = [elem.get_attribute(
                'href')for elem in hrefs if lista[i] not in hrefs]
            pics_filter = [n for n in pics_hrefs if '/p/' in n]
            b_interagiu = False
            if len(pics_filter) >= 10 and self.interacao_atual < self.interacaoMax:
                followers = driver.find_elements(By.CSS_SELECTOR, "li.Y8-fY:nth-child(2) > a:nth-child(1) > span:nth-child(1)")
                corrige_flw = 10
                if len(followers) > 0:
                    corrige_flw = followers[0].get_attribute(
                        'title').replace(",", "")
                
                if (self.f_limit == 0 or int(corrige_flw) <= self.f_limit) and int(corrige_flw) >= 15:
                    rnd = random.randint(9, 30)
                    time.sleep(rnd)
                    if self.queue[0].r_perfil[0]:
                        self.Follow()
                        # timer pra seguir uma ação após dar follow
                        rnd = random.randint(7, 15)
                        time.sleep(rnd)

                    # random pra começar a partir de um post random no feed
                    rnd = random.randint(5, 8)
                    contador = 0
                    j = rnd
                    while j >= 0 and contador < 3:
                        if self.interacao_atual >= self.interacaoMax:
                            return
                        driver.get(pics_filter[j])
                        # timer para troca de posts de um mesmo perfil
                        rnd = random.randint(10, 26)
                        time.sleep(rnd)
                        if self.interacao_atual >= self.interacaoMax:
                            return
                        if self.interacao_atual < self.interacaoMax:
                            btnLike = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button")
                            color = btnLike.get_property("innerHTML")
                            curtido = False
                            if "Unlike" in color or "unlike" in color:
                                curtido = True
                            if (self.tipo == 0):
                                if self.queue[0].r_perfil[1] and not curtido:
                                    self.Like()
                                    self.interacao_atual += 1
                                    self.ultima_interacao = time.time()
                                    #self.Dispose()
                                    #DiscordMessage(f"{self.username} deu um like na postagem [{pics_filter[j]}]", self.tipo_id)
                                    b_interagiu = True
                                if self.queue[0].r_perfil[2]:
                                    self.Comentar(self.lst_comments)
                                    self.interacao_atual += 1
                                    self.ultima_interacao = time.time()
                                    #self.Dispose()
                                    #DiscordMessage(f"{self.username} fez um comentário na postagem [{pics_filter[j]}]", self.tipo_id)
                                    b_interagiu = True
                            if (self.tipo == 1):
                                if self.queue[0].r_tags[3] and not curtido:
                                    self.Like()
                                    self.interacao_atual += 1
                                    self.ultima_interacao = time.time()
                                    #self.Dispose()
                                    #DiscordMessage(f"{self.username} deu um like na postagem [{pics_filter[j]}]", self.tipo_id)
                                    b_interagiu = True
                                if self.queue[0].r_tags[4]:
                                    self.Comentar()
                                    self.interacao_atual += 1
                                    self.ultima_interacao = time.time()
                                    #self.Dispose()
                                    #DiscordMessage(f"{self.username} fez um comentário na postagem [{pics_filter[j]}]", self.tipo_id)
                                    b_interagiu = True
                            if (b_interagiu):
                                time.sleep(3)
                        rnd = random.randint(1, 3)
                        contador += 1
                        j -= rnd
            if self.interacao_atual >= self.interacaoMax:
                return
            if time.time() - self.ultima_interacao >= 420:
                return
            if self.interacao_atual < self.interacaoMax:
                rnd = random.randint(14, 33 - int(self.multiplicador * 1.5))
                if (not b_interagiu):
                    # se não houver interação, sleep mais curto
                    rnd = random.randint(4, 12 - int(self.multiplicador))
                time.sleep(rnd)

class Threads:
    def __init__(self):
        self.queue = []
        self.currentThreads = 0

        self.queue_1 = []
        self.queue_2 = []
        self.queue_3 = []
        self.queue_4 = []

    def SetThreads(self, users):
        if len(users) <= 3:
            self.currentThreads = 1
        if len(users) >= 4 and len(users) <= 6:
            self.currentThreads = 2
        if len(users) >= 7 and len(users) <= 9:
            self.currentThreads = 3
        if len(users) >= 10:
            self.currentThreads = 4

        atual = 1
        localUsers = users
        while len(localUsers) > 0:
            if atual == 1:
                self.queue_1.append(localUsers[0])
            if atual == 2:
                self.queue_2.append(localUsers[0])
            if atual == 3:
                self.queue_3.append(localUsers[0])
            if atual == 4:
                self.queue_4.append(localUsers[0])
            
            del localUsers[0]

            atual += 1

            if atual > self.currentThreads:
                atual = 1

        for i in range(self.currentThreads):
            localQueue = []
            if i == 0:
                localQueue = self.queue_1
            if i == 1:
                localQueue = self.queue_2
            if i == 2:
                localQueue = self.queue_3
            if i == 3:
                localQueue = self.queue_4

            localThread = NewThread(localQueue)
            startThread = threading.Thread(target=localThread.Single, args=())
            startThread.start()
        
        threadsList = threading.enumerate()
        while len(threadsList) > 1:
            threadsList = threading.enumerate()