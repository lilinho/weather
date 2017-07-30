import urllib.parse
import json
import urllib.request
import tkinter.messagebox

"""
Lists and dictionaries for:
translate voivodeships to Polish
translate days to Polish
translate months to Polish
directions for wind in Polish
general conditions in Polish (ordered as they appear in Yahoo Weather API)
"""

days = {'Mon': 'Poniedziałek',
        'Tue': 'Wtorek',
        'Wed': 'Środa',
        'Thu': 'Czwartek',
        'Fri': 'Piątek',
        'Sat': 'Sobota',
        'Sun': 'Niedziela'}

months = {'Jan': 'stycznia',
          'Feb': 'lutego',
          'Mar': 'marca',
          'Apr': 'kwietnia',
          'May': 'maja',
          'Jun': 'czerwca',
          'Jul': 'lipca',
          'Aug': 'sierpnia',
          'Sep': ' września',
          'Oct': 'października',
          'Nov': 'listopada',
          'Dec': 'grudnia'}

voivodeship = {' Lower Silesia': 'dolnośląskie',
               ' Kuyavia-Pomerania': 'kujawsko-pomorskie',
               ' Lodz': 'łódzkie',
               ' Lublin': 'lubelskie',
               ' Lubusz': 'lubuskie',
               ' Lesser Poland': 'małopolskie',
               ' Masovian': 'mazowieckie',
               ' Subscarpathia': 'podkarpackie',
               ' Pomerania': 'pomorskie',
               ' Silesia': 'śląskie',
               ' Warmia-Masuria': 'warmińsko-mazurskie',
               ' Greater Poland': 'wielkopolskie',
               ' West Pomerania': 'zachodniopomorskie'}

wind_compass = ('północ', 'północ-północny wschód', 'północny wschód', 'wschód-północny wschód', 'wschód',
                'wschód-południowy wschód', 'południowy wschód', 'południe-południowy wschód', 'południe',
                'południe-południowy zachód', 'południowy zachód', 'zachód-południowy zachód', 'zachód',
                'zachód-północny zachód', 'północny zachód', 'północ-północny zachód')

conditions = ('tornado', 'burza tropikalna', 'huragan', 'częste burze', 'burze', 'deszcz ze śniegiem',
              'deszcz ze śniegiem', 'deszcz ze śniegiem', 'marznąca mżawka', 'mżawka', 'marznący deszcz',
              'opady deszczu', 'opady deszczu', 'delikatne opady śniegu', 'delikatne opady śniegu',
              'śnieg z podmuchami', 'śnieg', 'grad', 'mżawka', 'dust', 'mgliście', 'słaba mgła', 'smog',
              'porywy wiatru', 'wietrznie', 'zimno', 'pochmurnie', 'przeważnie pochmurna noc',
              'przeważnie pochmurny dzień', 'częściowo pochmurna noc', 'częściowo pochmurno', 'bezchmurna noc',
              'słonecznie', 'bezchmurna noc', 'słonecznie', 'deszcz z gradem', 'gorąco', 'burze', 'przelotne burze',
              'przelotne burze', 'przelotny deszcz', 'intensywne opady śniegu', 'przelotne opady śniegu', 'zamiecie',
              'częściowe zachmurzenie', 'burze', 'opady śniegu', 'przelotne burze')

"""
Function definition for finding WOEID of given city. If city wasn't found it returns False value, 
in other case it returns WOEID of given city
"""


def find_city(city_text):
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "SELECT woeid, placeTypeName FROM geo.places(1) WHERE text=\"" + city_text + \
                "\" and placetype = \"Town\""
    try:
        yql_url = base_url + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
        result = urllib.request.urlopen(yql_url).read()
        raw = json.loads(result)['query']['results']
        if raw is None:
            return False
        else:
            return raw['place']['woeid']

    except Exception as e:
        tkinter.messagebox.askokcancel(title="Błąd", message="Coś poszło nie tak. \n Kod błędu: " + str(e))
        print(e)


"""
Function definition for finding actual weather and forecast for given WOEID
"""


def load_weather(city_woeid):
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid=" + str(city_woeid) + " and u='c'"

    try:
        yql_url = base_url + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
        result = urllib.request.urlopen(yql_url).read()
        return json.loads(result)['query']['results']
    except Exception as e:
        print(e)


def translate_month(date):
    day, month, year = date.split(' ')
    month_polish = months[month]
    return day + " " + month_polish + " " + year

