from distutils.util import execute
import json
from msilib import text
import os
import platform
from twilio.rest import Client
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton
from twilio.base.exceptions import TwilioRestException
from selenium import webdriver
from config import CHROME_PROFILE_PATH
import subprocess
import time

String_Builder = """
Screen:
    ScreenManager: 
        id: screen_manager
        MainScreen:

<MainScreen>
    name: "main"
    MDNavigationLayout:
        ScreenManager:
            Screen:
                id: main
                MDLabel:
                    text: "Nanostation Wifi Password Changer"
                    pos_hint: {"center_y": 0.7}
                    halign: 'center'
                    font_style: "H1"
                MDTextFieldRound:
                    id: message
                    hint_text: "Enter Message"
                    size_hint: 0.75, 0.06
                    pos_hint: {"center_x": 0.5,"center_y": 0.3}
                    normal_color: 1,1,1,0.1
                    line_color: 1,1,1,0.1
                    color_active: 1,1,1,1
                    line_color_focus: 1,1,1,1
                    theme_text_color: "Custom"
                    text_color: 1,1,1,1
                MDRoundFlatIconButton:
                    text: "Change Password"
                    size_hint: 0.85, None
                    pos_hint: {"center_x": 0.5,"center_y": 0.2}
                    line_color: 1,1,1,1
                    text_color: 1,1,1,1
                    icon_color: 1,1,1,1
                    icon: "send"
                    on_release: app.changePassword()
                                                
"""

class MainScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))


class TheBadjie(MDApp):
    def build(self):
        self.theme_cls.theme_style='Dark'
        AppBuilder = Builder.load_string(String_Builder)
        return AppBuilder

    def changePassword(self):
        pass
        try:
            text_message = self.root.ids.screen_manager.get_screen("main").ids.message.text
            options = webdriver.ChromeOptions()
            options.add_argument(CHROME_PROFILE_PATH)
            platformFinder = platform.system()
            pwd = os.getcwd()
            

            if platformFinder == "Windows":
                subprocess.run(f'netsh interface ipv4 set address name="Ethernet" static 192.168.1.30 mask=255.255.255.0', capture_output=True,shell=True, text=True)
                path = pwd + "\Message_sender\chromedriver.exe" #This should be redited
                browser = webdriver.Chrome(executable_path=os.path.realpath(path), options=options)

                time.sleep(2)
                #Automating the browser
                browser.get('http://192.168.1.20/')
                time.sleep(10)
                browser.find_element_by_name('username').send_keys('ubnt')
                time.sleep(1)
                browser.find_element_by_name('password').send_keys('AllahuAkbar')
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/input').click()
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[1]/a[3]').click()
                time.sleep(1)
                browser.find_element_by_name('wpa_key').clear()
                time.sleep(1)
                browser.find_element_by_name('wpa_key').send_keys(text_message)
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="this_form"]/table/tbody[3]/tr/td/input').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="apply_button"]').click()
                time.sleep(1)
            subprocess.run(f'netsh interface ipv4 set address name="Ethernet" source=dhcp', capture_output=True,shell=True, text=True)

            dismisser = MDFlatButton(text="Dismiss",
                                        on_release=self.dismiss)
            self.dialog = MDDialog(title="Password Changed Successfully!",
                                text=f"Congratulations you have changed your password successfully!",
                                buttons=[dismisser],
                                size_hint=(0.75, 0.5)
                                )
            self.dialog.open()

        except Exception as e:
            splitter = str(e).split(':')
            if 'This version of ChromeDriver only supports' in str(e):
                dismisser = MDFlatButton(text="Dismiss",
                                        on_release=self.dismiss)
                self.dialog = MDDialog(title="Chrome Driver Error!",
                                    text=f"UPDATE YOUR CHROME DRIVER: {splitter[2]}",
                                    buttons=[dismisser],
                                    size_hint=(0.75, 0.5)
                                    )
                self.dialog.open()
            else:
                dismisser = MDFlatButton(text="Dismiss",
                                        on_release=self.dismiss)
                self.dialog = MDDialog(title="Error Message!",
                                    text=str(e),
                                    buttons=[dismisser],
                                    size_hint=(0.75, 0.5)
                                    )
                self.dialog.open()

    def dismiss(self, obj):
        pass
        self.dialog.dismiss()



TheBadjie().run()
