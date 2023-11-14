from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

a = Builder.load_file('hs.kv')
b = Builder.load_file('rs.kv')
c = Builder.load_file('pros.kv')
d = Builder.load_file('popup.kv')
unit_size_list = ['5x5', '5x10', '5x15', '10x10', '12x10', '10x15', '12x15', '10x20', '10x30', '12x25', '12x30']

one_month_price_list = [55, 96, 110, 130, 140, 145, 155, 160, 200, 210, 220]

six_month_price_list = [210, 356, 460, 500, 560, 590, 650, 680, 920, 980, 1040]

current_date = datetime.now()
day_of_month = current_date.day
current_month = current_date.month
next_month = current_month + 1
if next_month > 12:
    next_month = next_month - 12

current_year = current_date.year
next_year = current_year + 1
year_due = current_year

months_with_30_days = [4, 6, 9, 11]
months_with_31_days = [1, 3, 5, 7, 8, 10, 12]
february = 28
months_list = [months_with_31_days, months_with_30_days, february]
if current_month in months_with_30_days:
    days_in_month = 30
elif current_month in months_with_31_days:
    days_in_month = 31
else:
    days_in_month = 28

days_left_in_month = days_in_month - day_of_month

prorate = 0
sub_total = 0
grand_total = 0
tax = 0
base_price = 0
m_v = 0
unit_size = ''
unit_index = 0
pro_rate_out_price = 0
wrong_size = False


def all_calcs():
    global prorate
    prorate = (base_price / (m_v * days_in_month)) * days_left_in_month

    global sub_total
    sub_total = prorate + base_price

    global tax
    tax = sub_total * .0635

    global grand_total
    grand_total = tax + sub_total
    prorate = round(prorate, 2)
    sub_total = round(sub_total, 2)
    tax = round(tax, 2)
    grand_total = round(grand_total, 2)
    prorate = str(prorate)
    sub_total = str(sub_total)
    tax = str(tax)
    grand_total = str(grand_total)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.ids.think_b.disabled = True
        self.ids.pr_b.disabled = True

    okay_pay = [1, 6]
    payment = NumericProperty()
    unit_size = StringProperty('')
    rs_prorate = StringProperty()
    rs_subtotal = StringProperty()
    rs_tax = StringProperty()
    rs_grand_total = StringProperty()
    rs_base_price = StringProperty()
    rs_payment_due = StringProperty()
    rs_payment_year = StringProperty()
    pros_pro_price = StringProperty()

    def set_pay_val(self, month):

        self.payment = month
        global m_v
        m_v = self.payment
        print(self.payment)
        self.ids.think_b.disabled = False

    def set_unit_size(self):
        self.unit_size = self.ids.input_box.text
        if self.unit_size not in unit_size_list or self.payment not in self.okay_pay:
            self.unit_size = 'WRONG!'
            pop = Popup(title='WRONG!', content=d)
            pop.size = (400, 400)
            pop.background_color = (7/255, 197/255, 250/255, 1)
            pop.open()
            self.ids.think_b.disabled = True

        else:
            global unit_index
            unit_index = unit_size_list.index(self.unit_size)
            print(self.unit_size)
            self.ids.think_b.disabled = False
            self.ids.pr_b.disabled = False

    def set_base_price(self):
        global m_v
        global base_price
        global unit_index
        global year_due
        if m_v == 1:
            base_price = one_month_price_list[unit_index]
            self.rs_base_price = str(base_price)
            next_payment = next_month + 1
            if next_payment > 12:
                next_payment = next_payment - 12
                global year_due
                year_due = next_year

            self.rs_payment_year = str(year_due)
            self.rs_payment_due = str(next_payment)
        else:
            base_price = six_month_price_list[unit_index]
            self.rs_base_price = str(base_price)
            next_payment = next_month + 6
            if next_payment > 12:
                next_payment = next_payment - 12
                year_due = next_year
            self.rs_payment_year = str(year_due)
            self.rs_payment_due = str(next_payment)

    def set_calc_vals(self):
        all_calcs()
        self.rs_prorate = str(prorate)
        self.rs_subtotal = str(sub_total)
        self.rs_tax = str(tax)
        self.rs_grand_total = str(grand_total)
        print(prorate)

    def pro_rate_out(self):
        global unit_index
        global base_price
        global pro_rate_out_price
        base_price = one_month_price_list[unit_index]
        pro_rate_out_price = day_of_month * (base_price / days_in_month)
        pro_rate_out_price = round(pro_rate_out_price, 2)
        self.pros_pro_price = str(pro_rate_out_price)



class PROScreen(Screen):
    def __init__(self, **kwargs):
        super(PROScreen, self).__init__(**kwargs)

    prop = StringProperty()

    def on_enter(self, *args):
        home_screen = self.manager.get_screen('home_screen')
        self.prop = home_screen.pros_pro_price


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)

    rs_prorate = StringProperty()
    rs_subtotal = StringProperty()
    rs_tax = StringProperty()
    rs_grand_total = StringProperty()
    rs_base_price = StringProperty()
    rs_next_payment = StringProperty()
    rs_payment_year = StringProperty()

    def on_enter(self, *args):
        home_screen = self.manager.get_screen('home_screen')
        self.rs_prorate = home_screen.rs_prorate
        self.rs_subtotal = home_screen.rs_subtotal
        self.rs_tax = home_screen.rs_tax
        self.rs_grand_total = home_screen.rs_grand_total
        self.rs_base_price = home_screen.rs_base_price
        self.rs_next_payment = home_screen.rs_payment_due
        self.rs_payment_year = home_screen.rs_payment_year


class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.font_size = '20sp'
        self.color = 0, 0, 0, 1


class MyButton(Button):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.font_size = '20sp'
        self.background_color = (7/255, 197/255, 250/255, 1)
        self.background_normal = ''
        self.border = (0, 0, 0, 0)



class StorageApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(ResultScreen(name='result_screen'))
        sm.add_widget(PROScreen(name='pro_screen'))
        return sm


if __name__ == '__main__':
    StorageApp().run()
