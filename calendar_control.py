import calendar
import datetime

import flet as ft
from dateutil import relativedelta


class FletCalendar(ft.UserControl):

    def __init__(self, page, width=355, height=300, on_date_click=None, mark_days: list[tuple[int, int, int]] = None):
        super().__init__()
        today = datetime.datetime.today()
        self.now_month = today.month
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year
        self.text_color = None
        self.mark_day_color = None
        self.border_color = None
        self.page = page
        self.set_theme()
        self.width = width
        self.height = height
        self.on_date_click = on_date_click
        self.calendar_container = ft.Container(width=width, height=height,
                                               padding=ft.padding.all(2),
                                               border=ft.border.all(2, self.border_color),
                                               border_radius=ft.border_radius.all(10),
                                               alignment=ft.alignment.bottom_center)
        self.mark_days = [] if mark_days is None else mark_days
        self.build()


    def set_current_date(self):
        """Set the calendar to the current date."""
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year
        self.build()
        self.calendar_container.update()

    def get_next(self, _e):
        """Move to the next month."""
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month

        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_prev(self, _e):
        """Move to the previous month."""
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_calendar(self):
        """Get the calendar from the calendar module."""
        cal = calendar.HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)

    def set_theme(self, border_color=ft.colors.CYAN_600,
                  text_color=ft.colors.CYAN_600,
                  current_day_color=ft.colors.GREY_300):
        self.border_color = border_color
        self.text_color = text_color
        self.mark_day_color = current_day_color

    def build(self):
        """Build the calendar for flet."""
        current_calendar = self.get_calendar()

        str_date = '{0} {1}, {2}'.format(calendar.month_name[self.current_month], self.current_day, self.current_year)

        date_display = ft.Text(str_date, text_align='center', size=20, color=self.text_color)
        next_button = ft.Container(ft.Text('>', text_align='right', size=20, color=self.text_color),
                                   on_click=self.get_next)
        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)
        prev_button = ft.Container(ft.Text('<', text_align='left', size=20, color=self.text_color),
                                   on_click=self.get_prev)

        calendar_column = ft.Column(
            [ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER, height=40, expand=False), div],
            spacing=2, width=self.width, height=self.height, alignment=ft.MainAxisAlignment.START, expand=False)

        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_mark_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day)
                    if len(str(display_day)) == 1: display_day = '0%s' % display_day
                    if day == self.current_day and self.now_month == self.current_month:
                        is_current_day_font = ft.FontWeight.BOLD
                    if (day, self.current_month, self.current_year) in self.mark_days:
                        is_mark_day_bg = self.mark_day_color
                    day_button = ft.Container(
                        content=ft.Text(str(display_day), weight=is_current_day_font, color=self.text_color,
                                        size=self.width // 20),
                        on_click=self.on_date_click, data=(self.current_month, day, self.current_year),
                        width=self.width // 10, height=self.width // 9, ink=True, alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(10),
                        bgcolor=is_mark_day_bg)
                else:
                    day_button = ft.Container(width=self.width // 10, height=self.width // 9,
                                              border_radius=ft.border_radius.all(10))

                week_row.controls.append(day_button)

            calendar_column.controls.append(week_row)

        self.calendar_container.content = calendar_column
        return self.calendar_container
