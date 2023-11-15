from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.lang.builder import Builder
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from datetime import datetime
from kivymd.uix.button import MDRaisedButton
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

Builder.load_file('mdd.kv')

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


class MyLayout(MDFloatLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)


class CalcButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super(CalcButton, self).__init__(**kwargs)
        self.payment = NumericProperty()
        self.unit_size = StringProperty()
        self.prorate = ObjectProperty()
        self.base_price = NumericProperty()
        self.sub_total = NumericProperty()
        self.tax = NumericProperty()
        self.grand_total = NumericProperty()
        self.dis_prorate = StringProperty('')
        self.unit_size_list_button = unit_size_list
        self.next_payment = 0
        self.year_due = year_due
    def find_base_price(self):
        unit_index = unit_size_list.index(self.unit_size)
        if self.payment == 1:
            self.base_price = one_month_price_list[unit_index]
            self.next_payment = next_month + 1
            if self.next_payment > 12:
                self.next_payment = self.next_payment - 12
                self.year_due = next_year
        else:
            self.base_price = six_month_price_list[unit_index]
            self.next_payment = next_month + 6
            if self.next_payment > 12:
                self.next_payment = self.next_payment - 12
                self.year_due = next_year
    def all_calculations(self):
        self.prorate = (self.base_price / (self.payment * days_in_month)) * days_left_in_month
        self.prorate = round(self.prorate, 2)
        self.sub_total = self.prorate + self.base_price
        self.sub_total = round(self.sub_total, 2)
        self.tax = self.sub_total * .0635
        self.tax = round(self.tax, 2)
        self.grand_total = self.tax + self.sub_total
        self.grand_total = round(self.grand_total, 2)

        print(f'{self.base_price}')

    def display_results(self):
        self.parent.ids.prorate_lbl.text = f'Prorate: ${self.prorate}'
        self.parent.ids.base_price_lbl.text = f'Base price: ${self.base_price}'
        self.parent.ids.sub_total_lbl.text = f'SubTotal: ${self.sub_total}'
        self.parent.ids.tax_lbl.text = f'Tax: ${self.tax}'
        self.parent.ids.grand_total_lbl.text = f'GrandTotal: ${self.grand_total}'
        self.parent.ids.next_payment_lbl.text = f'Next payment due: {self.next_payment}/1/{self.year_due}'

    def check(self):
        u_size = f'{self.unit_size}'
        acceptable_payments = [1, 6]
        if u_size in unit_size_list and self.payment in acceptable_payments:
            return True
        else:
            return False

    def handle_button(self):
        if self.check():
            self.find_base_price()
            self.all_calculations()
            self.display_results()
        else:
            pass
class MyToggle(MDFlatButton, MDToggleButton):

    def __init__(self, *args, **kwargs):
        super(MyToggle, self).__init__(*args, **kwargs)
        self.background_down = self.theme_cls.primary_color

        self.payment = NumericProperty()

    def set_payment(self, pay_value):
        self.payment = pay_value
        self.parent.ids.calc_button.payment = self.payment
        print(self.parent.ids.calc_button.payment)


class MyTextField(MDTextField):
    def __init__(self, **kwargs):
        super(MyTextField, self).__init__(**kwargs)

        self.unit_size = StringProperty()

    def set_unit_size(self):
        self.unit_size = self.text
        self.parent.ids.calc_button.unit_size = self.unit_size
        print(self.parent.ids.calc_button.unit_size)

    def check(self):
        if self.unit_size not in unit_size_list:
            self.parent.ids.calc_button.disabled = True
        else:
            self.parent.ids.calc_button.disabled = False

class MyLabel(MDLabel):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.theme_text_color = 'Custom'
        self.text_color = 'indigo'
        self.halign = 'center'

class AltLabel(MDLabel):
    def __init__(self, **kwargs):
        super(AltLabel, self).__init__(**kwargs)
        self.theme_text_color = 'Custom'
        self.text_color = 'black'
        self.halign = 'center'
class MDStorageApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.theme_style = 'Dark'
        return MyLayout()


if __name__ == '__main__':
    MDStorageApp().run()
