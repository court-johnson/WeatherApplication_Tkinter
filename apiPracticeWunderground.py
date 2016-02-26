import requests
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import urllib.request
import base64
import time
#--------------------------------------
#calls api to retrieve information for area needed and key to be used 
r = requests.get("http://api.wunderground.com/api/4a3ef595ef7429f9/forecast/q/TX/Austin.json")
data = r.json()
#--------------------------------------
class WeatherApp():
    def __init__(self, master):
        #master variable to destroy and refresh later
        self.myMaster = master
        self.myMaster.title('Austin 3-day Weather Update')
        self.myMaster.resizable(False, False)

        #styling of the frame
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#444444')
        self.frame = ttk.Frame(master, style = 'TFrame')
        self.frame.pack()

    
        #label reflecting Austin weather is being generated 
        self.label_header = ttk.Label(self.frame, text = "Austin, Texas Forecast:",
                                      background = '#444444',foreground = '#c2c2a3', font = ('Helvetica', 10, 'bold'))
        
        #creating the box the populates the weather forecast and styling
        self.forecast_box = Text(self.frame, height = 15, width = 19, background = '#35424D', foreground = '#c2c2a3')
        
        #creating the button that refreshes the weather application
        self.refresh_button = tkinter.Button(self.frame, text = 'REFRESH', command=self.refreshed, relief = RAISED,
                                activebackground = '#c2c2a3', background = '#35424D', foreground = '#c2c2a3')
        
        #populates api data by reviewing data for each day in the forecast (generates four days worth of data)
        for day in data['forecast']['simpleforecast']['forecastday']:
            days_pop = day['date']['weekday_short'] + "-"
            con = "Conditions: " + day['conditions']
            temp_high = "High: " + day['high']['fahrenheit'] + "F, "
            temp_low = "Low: " + day['low']['fahrenheit'] + "F"
            #presents all the data for each day, not just the last day 
            if days_pop:
                #referencing how the data will be outputted and inserted into the forecast_box
                output = days_pop + "\n" + con + "\n" + temp_high + temp_low + "\n" + "\n"
                self.forecast_box.insert(END, output)

                
        #disabling forecast box after data is inserted so it cannot be manipulated 
        self.forecast_box.config(state = DISABLED)

        #referencing the weather radar url to connect to
        image_url = "http://api.wunderground.com/api/4a3ef595ef7429f9/radar/q/TX/Austin.gif?width=280&height=280&newmaps=1&width=243&height=243"

        #reading the url data and encoding it to be reflected in the radar_label widget
        image_read = urllib.request.urlopen(image_url)
        imager = image_read.read()
        b64_data = base64.encodestring(imager)
        radar_image = PhotoImage(data=b64_data)

        #inserting the image from the url to the label widget
        radar_label = ttk.Label(self.frame, image = radar_image)
        radar_label.image = radar_image

        #organizing widgets into a grid
        radar_label.grid(row=1, column = 2, padx = 5, pady = 5)
        self.refresh_button.grid(row = 2, column = 2, sticky = 'w',  pady = 10)
        self.label_header.grid(row = 0, column = 0, sticky = 'w', padx = 20, pady = 10)
        self.forecast_box.grid(row = 1, column = 0, padx = 5, pady = 5)
        
    #exiting the window and re-populating the new data when the refresh button is clicked    
    def refreshed(self):
        self.myMaster.destroy()
        time.sleep(1)
        main()
        print('refreshed')

#--------------------------------------
def main():
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
