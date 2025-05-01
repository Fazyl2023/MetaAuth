from sys import version
import time
import os
from fake_useragent import FakeUserAgent
from playwright.sync_api import sync_playwright
import shutil
import pyperclip
import json
from password_generator import PasswordGenerator

#Веедите сой идентификатор
ident = 'your identificator' 
your_name = 'your name'
version = '12.16.1_0'
path = f'/Users/{your_name}/Library/Application Support/Google/Chrome/Default/Extensions/{ident}/{version}/'
s_phrase = {}
pwo = PasswordGenerator()
passwd = pwo.generate()
pass_json = {}
pass_json['password'] = passwd
with sync_playwright() as p:
    # Удаление сохраненных данных     
    shutil.rmtree('/tmp/metamask-profile', ignore_errors=True)
    #Проверка пути до расширения
    print("Manifest exists:", os.path.exists(os.path.join(path, "manifest.json")))
    
    browser = p.chromium.launch_persistent_context(
        user_data_dir="/tmp/metamask-profile",
        user_agent= FakeUserAgent().random,
        headless=False,
        args=[
            f"--disable-extensions-except={path}",
            f"--load-extension={path}"
        ],
    )


    # Открытие страницы MetaMask
    metamask_page = browser.new_page()
    metamask_page.goto(f"chrome-extension://{ident}/home.html")
    time.sleep(4)
    for page in browser.pages:
        print("Page title:", page.title(), "| URL:", page.url)
        if "MetaMask" in page.title():
            metamask_page = page
            break
    
        time.sleep(2)
        # Галочка на "я соглашаюсь итд"
        metamask_page.click('label[for="onboarding__terms-checkbox"]') # #onboarding__terms-checkbox
        # Кнопка Начала регистрации
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > ul > li:nth-child(2) > button')
        time.sleep(2)
        # Отменить отправку данных для анализа клик
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div'
        '.mm-box.onboarding-metametrics__buttons.mm-box--display-flex.mm-box--gap-4.mm-box--flex-direction-row'
        '.mm-box--width-full > button.mm-box.mm-text.mm-button-base.mm-button-base--size-lg.mm-button-secondary'
        '.mm-text--body-md-medium.mm-box--padding-0.mm-box--padding-right-4'
        '.mm-box--padding-left-4.mm-box--display-inline-flex.mm-box--justify-content-center'
        '.mm-box--align-items-center.mm-box--color-primary-default.mm-box--background-color-transparent'
        '.mm-box--rounded-pill.mm-box--border-color-primary-default.box--border-style-solid.box--border-width-1')
        
        # Ввод пароля
        metamask_page.fill('input[data-testid="create-password-new"]', passwd)
        metamask_page.fill('input[data-testid="create-password-confirm"]', passwd)
        
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > div.mm-box.mm-box--margin-top-4.mm-box--margin-bottom-4.mm-box--justify-content-space-between.mm-box--align-items-center > label > span.mm-checkbox__input-wrapper > input')
        # Я понимаю что метамаск
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > button')
        # Защита аккаунта сид-фразой (да)
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.secure-your-wallet__actions.mm-box--margin-bottom-8.mm-box--display-flex.mm-box--gap-4.mm-box--flex-direction-column.mm-box--sm\:flex-direction-row.mm-box--justify-content-space-between.mm-box--width-full > button.mm-box.mm-text.mm-button-base.mm-button-base--size-lg.mm-button-base--block.mm-button-primary.mm-text--body-md-medium.mm-box--padding-0.mm-box--padding-right-4.mm-box--padding-left-4.mm-box--display-inline-flex.mm-box--justify-content-center.mm-box--align-items-center.mm-box--color-primary-inverse.mm-box--background-color-primary-default.mm-box--rounded-pill')
        # Посмотреть сид-фразу
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.recovery-phrase__footer > button')
        # Копировать сид-фразу в буфер
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.recovery-phrase__footer > div > div > a.button.btn-link.recovery-phrase__footer__copy-and-hide__button.recovery-phrase__footer__copy-and-hide__button__copy-to-clipboard')
        
        # Сохранение в config.json сид-фразы
        with open('config.json', 'a') as f:    
            # Запись в словарь пароля
            s_phrase['password'] = passwd
            for i in range(12):
                # Запись с буфера в словарь пароля и сид фразы   
                slovo = pyperclip.paste().split(" ")[i]
                s_phrase[i] = slovo
            
            json.dumps(s_phrase)
            f.write(f'{json.dumps(s_phrase)} \n')
            

        # Кнопка продолжить (Переход на проверку сид фразы)
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.recovery-phrase__footer > div > button')
      
        # Ввод секретной фразы
        metamask_page.fill('input[data-testid="recovery-phrase-input-2"]', s_phrase[2])#3
        metamask_page.fill('input[data-testid="recovery-phrase-input-3"]', s_phrase[3]) #4
        metamask_page.fill('input[data-testid="recovery-phrase-input-7"]', s_phrase[7])#8
        # Подтвердить клик
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.recovery-phrase__footer__confirm > button')
        time.sleep(1)
        # Выполенно клик
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.creation-successful__actions.mm-box--margin-top-6.mm-box--display-flex.mm-box--flex-direction-column.mm-box--justify-content-center.mm-box--align-items-center > button')
        time.sleep(1)
        # Далее клик
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.onboarding-pin-extension__buttons > button')
        # Выполнено клик
        time.sleep(1)
        metamask_page.click('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.onboarding-pin-extension__buttons > button')            

        time.sleep(90)