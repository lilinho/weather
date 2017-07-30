import weatherfunctions
from tkinter import *
import math
import tkinter.messagebox


class MainWindow:

    def __init__(self, main):

        # definition for main window and layout parts

        search_frame = Frame(main)
        weather_frame = Frame(main)
        self.forecast_frame = Frame(main)
        sep_frame = Frame(main)
        search_frame.pack(pady=10)
        sep_frame.pack(padx=5, fill=X)
        weather_frame.pack(fill=BOTH, pady=10, padx=5)
        self.forecast_frame.pack(fill=BOTH, pady=10, padx=5)
        self.orient_window(main)

        self.searchInput = Entry(search_frame)
        self.searchButton = Button(search_frame, text='Szukaj', command=self.set_weather)
        self.searchInput.pack(side=LEFT)
        self.searchButton.pack(side=LEFT)

        self.location_label = Label(weather_frame, text="Lokalizacja")

        self.temperature_label = Label(weather_frame, text="Temperatura")
        self.conditions_label = Label(weather_frame, text="Ogólne warunki pogodowe")
        self.humidity_label = Label(weather_frame, text="Wilgotność")
        self.pressure_label = Label(weather_frame, text="Ciśnienie")
        self.sunrise_label = Label(weather_frame, text="Wschód słońca")
        self.sunset_label = Label(weather_frame, text="Zachód słońca")

        self.wind_direction_label = Label(weather_frame, text="Kierunek wiatru")
        self.wind_speed_label = Label(weather_frame, text="Prędkość wiatru")

        self.forecast_label = Label(self.forecast_frame, text="Prognoza")

        self.location_label.grid(row=0, sticky=E)
        self.temperature_label.grid(row=2, sticky=E)
        self.conditions_label.grid(row=3, sticky=E)
        self.humidity_label.grid(row=4, sticky=E)
        self.pressure_label.grid(row=5, sticky=E)
        self.sunrise_label.grid(row=6, sticky=E)
        self.sunset_label.grid(row=7, sticky=E)
        self.wind_direction_label.grid(row=10, sticky=E)
        self.wind_speed_label.grid(row=11, sticky=E)

        self.location = Label(weather_frame, text="")
        self.temperature = Label(weather_frame, text="")
        self.conditions = Label(weather_frame, text="")
        self.humidity = Label(weather_frame, text="")
        self.pressure = Label(weather_frame, text="")
        self.sunrise = Label(weather_frame, text="")
        self.sunset = Label(weather_frame, text="")
        self.windd = Label(weather_frame, text="")
        self.winds = Label(weather_frame, text="")

        self.location.grid(row=0, column=1, sticky=W)
        self.temperature.grid(row=2, column=1, sticky=W)
        self.conditions.grid(row=3, column=1, sticky=W)
        self.humidity.grid(row=4, column=1, sticky=W)
        self.pressure.grid(row=5, column=1, sticky=W)
        self.sunrise.grid(row=6, column=1, sticky=W)
        self.sunset.grid(row=7, column=1, sticky=W)
        self.windd.grid(row=10, column=1, sticky=W)
        self.winds.grid(row=11, column=1, sticky=W)
        main.update_idletasks()
        print(main.winfo_width())
        self.forecast_frame.columnconfigure(0, minsize=int(main.winfo_width()))
        self.forecast_label.grid(sticky=N+S+W+E, columnspan=2)

    @staticmethod
    def orient_window(main):
        sw = main.winfo_screenwidth()
        sh = main.winfo_screenheight()
        x = (sw / 2) - (400 / 2)
        y = (sh / 2) - (400 / 2)
        main.geometry('%dx%d+%d+%d' % (400, 550, x, y))

    def set_weather(self):
        try:
            if weatherfunctions.find_city(self.searchInput.get()) is False:
                tkinter.messagebox.askokcancel(title="Błąd", message="Nie znaleziono miasta")
            else:
                weather_dictionary = weatherfunctions.load_weather(weatherfunctions.find_city(self.searchInput.get()))
                self.location.config(text=self.searchInput.get() + ", " + weatherfunctions.voivodeship[
                    weather_dictionary['channel']['location']['region']])
                self.temperature.config(text=weather_dictionary['channel']['item']['condition']['temp'] + "C")
                self.conditions.config(text=str(weatherfunctions.conditions[
                                            int(weather_dictionary['channel']['item']['condition']['code'])]))
                self.humidity.config(text=weather_dictionary['channel']['atmosphere']['humidity'] + "%")
                press = float(weather_dictionary['channel']['atmosphere']['pressure']) / 33.76
                self.pressure.config(text=str(math.ceil(press*100/100)) + "hPa")
                self.sunrise.config(text=weather_dictionary['channel']['astronomy']['sunrise'])
                self.sunset.config(text=weather_dictionary['channel']['astronomy']['sunset'])
                index = int(weather_dictionary['channel']['wind']['direction']) // 22.5
                self.windd.config(text=weatherfunctions.wind_compass[int(index)])
                self.winds.config(text=weather_dictionary['channel']['wind']['speed'] + "km/h")

                days_list = []
                forecast_list = []
                index = 1
                days_list.append(Label(self.forecast_frame, text=""))
                forecast_list.append(Label(self.forecast_frame, text=""))
                while index < 6:
                    days_list.append(Label(
                        self.forecast_frame, text=weatherfunctions.days[
                                                      weather_dictionary['channel']['item']['forecast'][index]['day']]
                                                  + ', ' + weatherfunctions.translate_month(
                            weather_dictionary['channel']['item']['forecast'][index]['date'])))
                    forecast_list.append(Label(self.forecast_frame, text=str(weatherfunctions.conditions[
                                                                             int(weather_dictionary['channel']['item'][
                                                                                     'forecast'][index]['code'])])
                                                                     + ", Max: " +
                                                                     weather_dictionary['channel']['item']['forecast'][
                                                                         index]['high']
                                                                     + "C, Min: " +
                                                                     weather_dictionary['channel']['item']['forecast'][
                                                                         index]['low']
                                                                     + "C"))
                    days_list[index].grid(row=index*2-1, column=0)
                    forecast_list[index].grid(row=index*2, column=0)
                    index += 1


                print(weather_dictionary)
        except Exception as e:
            print(e)
