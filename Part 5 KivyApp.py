# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:38:01 2020

@author: User
"""

import pandas as pd
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
#from kivycalendar3 import DatePicker
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

class MyApp(App):
    def update_value(self, inst):
        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.ti.text = self.text
    
    def show_calendar(self, temp):
        datePicker = DatePicker()
        datePicker.show_popup(1, .3)
        
    def show_selected_value(spinner, txt, temp):
        if (temp == "01" or temp == "02" or temp == "03" or temp == "04" or
            temp == "05" or temp == "06" or temp == "07" or temp == "08" or
            temp == "09" or temp == "10" or temp == "11" or temp == "12" or
            temp == "13" or temp == "14" or temp == "15" or temp == "16" or
            temp == "17" or temp == "18" or temp == "19" or temp == "20" or
            temp == "21" or temp == "22" or temp == "23" or temp == "24" or
            temp == "25" or temp == "26" or temp == "27" or temp == "28" or
            temp == "29" or temp == "30" or temp == "31"):
            spinner.lblDay.text = temp
        
        switcher={
                'Jan':'01',
                'Feb':'02',
                'Mar':'03',
                'Apr':'04',
                'May':'05',
                'Jun':'06',
                'Jul':'07',
                'Aug':'08',
                'Sep':'09',
                'Oct':'10',
                'Nov':'11',
                'Dec':'12'}
        if (temp == 'Jan' or temp == 'Feb' or temp == 'Mar' or temp == 'Apr' or
            temp == 'May' or temp == 'Jun' or temp == 'Jul' or temp == 'Aug' or
            temp == 'Sep' or temp == 'Oct' or temp == 'Nov' or temp == 'Dec'):
            spinner.lblMth.text = switcher.get(temp, '')
        
        if (temp == '2000' or temp == '2001' or temp == '2002' or temp == '2003' or
            temp == '2004' or temp == '2005' or temp == '2006' or temp == '2007' or
            temp == '2008' or temp == '2009' or temp == '2010' or temp == '2011' or
            temp == '2012' or temp == '2013' or temp == '2014' or temp == '2015' or
            temp == '2016' or temp == '2017' or temp == '2018'):
            spinner.lblYr.text = temp
        
        if (spinner.lblDay.text != "" and spinner.lblMth.text != "" and spinner.lblYr.text != ""):
            dt = spinner.lblYr.text + '-' + spinner.lblMth.text + '-' + spinner.lblDay.text
            
            df = pd.read_csv('D:\Edison\Masters\Data Mining\Group\mbb2.csv')
            df2 = pd.read_csv('D:\Edison\Masters\Data Mining\Group\klse2.csv')
            
            mbb = df[df['date'] == dt]['close']
            klse = df2[df2['date'] == dt]['close']
            if (mbb.size != 0):
                spinner.lblMBB2.text = str("{:.2f}".format(mbb.values[0]))
            else:
                spinner.lblMBB2.text = ''
            if (klse.size != 0):
                spinner.lblKLSE2.text = str("{:.2f}".format(klse.values[0]))
            else:
                spinner.lblKLSE2.text = ''
        
    
    def build(self):
        self.grid = GridLayout(cols=1)
        self.boxDt = BoxLayout(orientation='horizontal')
        self.boxStock = BoxLayout(orientation='horizontal')
        self.boxPrice = BoxLayout(orientation='horizontal')
        
        self.lblTitle = Label(text='Maybank Share Price VS KLSE Index (2000 to 2018)', bold=True)
        self.lblBlank = Label(text='')
        self.imgChart = AsyncImage(source='https://github.com/wqd190038/Data-Mining-Assignment/blob/master/stockchart.png?raw=true', allow_stretch=True, size_hint_x=5)
        #self.btnSelect = Button(text='Pick a date', size_hint=(.1,.1), on_press=self.show_calendar)
        self.lblSelect = Label(text='Select a Date')
        spinnerD = Spinner(id='spinD',
                text='Day',
                values=('01','02','03','04','05','06','07','08','09','10',
                        '11','12','13','14','15','16','17','18','19','20',
                        '21','22','23','24','25','26','27','28','29','30','31'),
                size_hint=(None, None),
                size=(100, 44),
                pos_hint={'center_x': .5, 'center_y': .5}
                )
        spinnerD.bind(text=self.show_selected_value)
        spinnerM = Spinner(
                text='Month',
                values=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct',
                        'Nov','Dec'),
                size_hint=(None, None),
                size=(100, 44),
                pos_hint={'center_x': .5, 'center_y': .5}
                )
        spinnerM.bind(text=self.show_selected_value)
        spinnerY = Spinner(
                text='Year',
                values=('2000','2001','2002','2003','2004','2005','2006','2007','2008',
                        '2009','2010','2011','2012','2013','2014','2015','2016','2017',
                        '2018'),
                size_hint=(None, None),
                size=(100, 44),
                pos_hint={'center_x': .5, 'center_y': .5}
                )
        spinnerY.bind(text=self.show_selected_value)
        self.lblBlank2 = Label(text='')
        self.lblMBB = Label(text='MBB', color=[1,0,0,1], bold=True, size_hint_y=None, height=44)
        self.lblKLSE = Label(text='KLSE', color=[0,0,1,1], bold=True, size_hint_y=None, height=44)
        self.lblMBB2 = Label(id='lblMBB2', size_hint_y=None, height=44)
        self.lblKLSE2 = Label(id='lblKLSE2', size_hint_y=None, height=44)
        self.lblDay = Label(id='lblDay')
        self.lblMth = Label(id='lblMth')
        self.lblYr = Label(id='lblYr')
        
        self.grid.add_widget(self.lblTitle)
        #self.grid.add_widget(self.lblBlank)
        self.grid.add_widget(self.imgChart)
        self.boxDt.add_widget(self.lblSelect)
        self.boxDt.add_widget(spinnerD)
        self.boxDt.add_widget(spinnerM)
        self.boxDt.add_widget(spinnerY)
        self.boxDt.add_widget(self.lblBlank)
        self.grid.add_widget(self.boxDt)
        #self.grid.add_widget(self.lblBlank2)
        self.boxStock.add_widget(self.lblMBB)
        self.boxStock.add_widget(self.lblKLSE)
        self.grid.add_widget(self.boxStock)
        self.boxPrice.add_widget(self.lblMBB2)
        self.boxPrice.add_widget(self.lblKLSE2)
        self.grid.add_widget(self.boxPrice)
        return self.grid
    
if __name__ == "__main__":
    MyApp().run()