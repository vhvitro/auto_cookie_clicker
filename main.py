import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

#creating a class to not have to deal with global and local differences
class cookie_clicker:
    def __init__(self):
        self.set_initial_variables()
        self.initialize()
    
    #function to initialize variables
    def set_initial_variables(self)->None:
        self.start = 0
        self.max_time = 0
        self.cookies = 0
        self.golden_cookies = 0
        self.cursors = 0
        self.up_cursors = 0
        self.grandmas = 0
        self.up_grandmas = 0
        self.farms = 0
        self.up_farms = 0

    #function to initialize the game
    def initialize(self)->None:
        self.max_time = int(input("Enter the time in seconds to run the script: "))
        bakery_name = str(input("Enter the baker's name: "))
        self.driver = webdriver.Chrome()
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.driver.maximize_window()
        language_selected = False
        while not language_selected:
            try:
                languague_selection = self.driver.find_element(By.ID, 'langSelect-PT-BR')
                languague_selection.click()
                language_selected = True
            except:
                pass
        bakery_named = False
        while not bakery_named:
            try:
                bakery_selection_button = self.driver.find_element(By.ID, 'bakeryName')
                bakery_selection_button.click()
                time.sleep(0.5)
                bakery_selection = self.driver.find_element(By.ID, 'bakeryNameInput')
                bakery_selection.send_keys(bakery_name)
                (self.driver.find_element(By.ID, 'promptOption0')).click()
                bakery_named = True
            except:
                pass
        (self.driver.find_element(By.CLASS_NAME, 'cc_btn_accept_all')).click()
        self.cookie = self.driver.find_element(By.ID, 'bigCookie')
    
    #function to buy cursors when cookies>=15*(1.15^cursors) -> math function by which the price is calculated
    def buy_cursors(self)->None:
        if self.cookies>=round(15*((1.15)**self.cursors)):
            product0 = self.driver.find_element(By.ID, 'product0')
            product0.click()
            self.cursors+=1
    
    #function to buy grandmas when cookies>=100*(1.15^grandmas) -> math function by which the price is calculated        
    def buy_grandma(self)->None:
        if self.cookies>=round(100*((1.15)**self.grandmas)):
            product1 = self.driver.find_element(By.ID, 'product1')
            product1.click()
            self.grandmas+=1
    
    #function to buy farms when cookies>=1100*(1.15^grandmas) -> math function by which the price is calculated 
    def buy_farm(self)->None:
        if self.cookies>=round(1100*((1.15)**self.farms)):
            product2 = self.driver.find_element(By.ID, 'product2')
            product2.click()
            self.farms+=1
    
    #function to buy the first upgrade available        
    def buy_upgrade(self)->bool:
        try:
            upgrade = self.driver.find_element(By.CSS_SELECTOR, '.upgrade.enabled')       
            upgrade.click()
            return True
        except:
            return False
        
    #function to click cookies and try to click golden cookies
    def clicking(self)->None:
        while(time.time()-self.start<self.max_time):
            try:
                golden = self.driver.find_element(By.CLASS_NAME, 'shimmer')
                golden.click()
                self.golden_cookies+=1
            except:
                pass
            self.cookie.click()   
    
    #function to follow the strategy
    def do_strategy(self)->None:
        while(time.time()-self.start<self.max_time):
            self.cookies = int(self.driver.find_element(By.ID, 'cookies').text.split()[0].replace(',', ''))
            #if haven't bought any cursors upgrades yet, buy them first
            if self.up_cursors==0:
                #it requires at least one cursor to buy the first upgrade
                if self.cursors==0:
                    self.buy_cursors()
                elif self.buy_upgrade():
                    self.up_cursors+=1
            #buying the second cursor upgrade (best option because it doubles the cookies by click)
            elif self.up_cursors<2:
                if self.buy_upgrade():
                    self.up_cursors+=1
            #let's buy some more cursors
            elif self.cursors<5 and self.up_cursors==2:
                self.buy_cursors()
            #buying the first grandma to enable the upgrade
            elif self.grandmas==0:
                self.buy_grandma()
            #buying the first grandma upgrade (best option because it doubles the cookies by grandma)
            elif self.up_grandmas==0:
                if self.buy_upgrade():
                    self.up_grandmas+=1
            #buying more grandmas
            elif self.up_cursors>=2 and self.grandmas<=3 and self.up_grandmas>0:
                self.buy_grandma()
            else:
                #the most optimal option is to have around 10 cursors and 10 grandmas in the early game
                if self.cursors<10:
                    self.buy_cursors()
                elif self.grandmas<10:
                    self.buy_grandma()
                #after all that, keeps buying upgrades when available
                elif self.farms==0:
                    self.buy_farm()
                elif self.up_grandmas<2:
                    if self.buy_upgrade():
                        self.up_grandmas+=1
                elif self.farms<3:
                    self.buy_farm()
                elif self.up_cursors<3:
                    if self.buy_upgrade():
                        self.up_cursors+=1
                else:
                    self.buy_farm()
            
    #function that plays the game    
    def play(self)->None:
        self.start = time.time()
        #while the time running the game doesn't exceed the max time set by the user
        click = threading.Thread(target=self.clicking)
        buy = threading.Thread(target=self.do_strategy)
        click.start()
        buy.start()
        click.join()
        buy.join()
        
    #function to get the stats of the game
    def get_stats(self)->None:
        stats_button = self.driver.find_element(By.ID, 'statsButton')
        stats_button.click()
        information = self.driver.find_elements(By.CLASS_NAME, 'listing')
        for i in range(5):
            print(information[i].text)
        print(f'Golden cookies clicked: {self.golden_cookies}')
    #function to close the game
    def quit_game(self)->None:
        self.driver.quit()
        print("Game closed")
        
if __name__ == '__main__':
    bot = cookie_clicker()
    bot.play()
    bot.get_stats()
    bot.quit_game()