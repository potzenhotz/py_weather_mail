#!/usr/bin/env python3
#Python script for rss feed read of weather data

import time
import pyowm
import useful_stuff as us
from pyowm import timeutils
import datetime as dt


#-----------------------------------------------------------------------
#Useful functions
#-----------------------------------------------------------------------
def change_time_format(input):
  output =  dt.datetime.fromtimestamp(input).strftime('%d-%m-%Y %H:%M')
  return output

#function to remove '{}'
def pp(input_dict):
  for keys in sorted(input_dict):
    if str(input_dict[keys]) != '{}':
      print(keys + ': ' + str(input_dict[keys]))

def pp_str(input_dict):
  output = ''
  i = 0
  for keys in sorted(input_dict):
  #for keys in input_dict:
    if str(input_dict[keys]) != '{}':
      if i == 0:
        output +=  str(keys + ': ' + str(input_dict[keys]))
      else:
        output += '\n' + str(keys + ': ' + str(input_dict[keys]))
    i += 1
  return output


#-----------------------------------------------------------------------
#Weather function
#-----------------------------------------------------------------------

def current_weather(input_city):
  
  #-----------------------------------------------------------------------
  #Extract City name
  #-----------------------------------------------------------------------
  city = input_city.split(',', 1)[0]  #input needs to modify with split

  #-----------------------------------------------------------------------
  #Use open weather map key
  #-----------------------------------------------------------------------
  owm = pyowm.OWM('770bab8b8abf5696883cf53b96333e9f')
  
  #-----------------------------------------------------------------------
  #Setup the observation(obs) and forecasts for a certain location
  #-----------------------------------------------------------------------
  obs = owm.weather_at_place(input_city)
  #forecast objects
  fc_object_3h = owm.three_hours_forecast(input_city)  
  fc_object_daily = owm.daily_forecast(input_city)  
  
  time_of_obs_unix = obs.get_reception_time()
  time_of_obs =  change_time_format(time_of_obs_unix)
  
  location_raw = obs.get_location()
  location_name = location_raw.get_name()
  location_id = location_raw.get_ID()
  lat = location_raw.get_lat()
  lon = location_raw.get_lon()
  
  #-----------------------------------------------------------------------
  #Set some time strings for output
  #-----------------------------------------------------------------------
  today_06 = str(time.strftime("%Y-%m-%d")) + ' 06:00:00+00'
  today_09 = str(time.strftime("%Y-%m-%d")) + ' 09:00:00+00'
  today_12 = str(time.strftime("%Y-%m-%d")) + ' 12:00:00+00'
  today_15 = str(time.strftime("%Y-%m-%d")) + ' 15:00:00+00'
  today_18 = str(time.strftime("%Y-%m-%d")) + ' 18:00:00+00'
  tomorrow_06=str(timeutils.tomorrow(6,00)) + '+00'
  tomorrow_09=str(timeutils.tomorrow(9,00)) + '+00'
  tomorrow_12=str(timeutils.tomorrow(12,00)) + '+00'
  tomorrow_15=str(timeutils.tomorrow(15,00)) + '+00'
  tomorrow_18=str(timeutils.tomorrow(18,00)) + '+00'

  fc_times_today = [today_06
                    ,today_09
                    ,today_12
                    ,today_15
                    ,today_18]
  fc_times_tomorrow = [tomorrow_06
                    ,tomorrow_09
                    ,tomorrow_12
                    ,tomorrow_15
                    ,tomorrow_18]

  fcd_vec = [dt.datetime.today().date()
            ,dt.datetime.today().date() + dt.timedelta(days=1)
            ,dt.datetime.today().date() + dt.timedelta(days=2)
            ]

  #-----------------------------------------------------------------------
  #Information of observation/forecast city
  #-----------------------------------------------------------------------
  week_number = us.week_number()
  output ='\n' + '%s(%s, %s), Woche: %s, Datum: %s' % (city,lat,lon,week_number,time_of_obs)


  #define weather from objects (observations and forecast scenarios)
  observat = obs.get_weather()
  f_3h = fc_object_3h.get_forecast()
  f_daily = fc_object_daily.get_forecast()

  #-----------------------------------------------------------------------
  #Actually start with the setup of observation and forecast
  #-----------------------------------------------------------------------

 
  weather_dict = {'forecast3':f_3h,'forecast_daily': f_daily,'observation': observat}
  #for weather in weather_list: 
  for key in sorted(weather_dict):
    weather = weather_dict[key]
    if key == 'observation':
      wind = weather.get_wind()
      wind_speed = wind['speed']
      try:
        wind_deg = wind['deg']
      except:
        wind_deg = 'no_data'
      temp = weather.get_temperature(unit='celsius')
      temp_max = temp['temp_max']
      temp_min = temp['temp_min']
      temperature = temp['temp']
      dew_point = weather.get_dewpoint()
      pressure = weather.get_pressure()
      press_local = pressure['press']
      press_sea = pressure['sea_level']
      sunrise_unix = weather.get_sunrise_time()
      sunrise = change_time_format(sunrise_unix)
      sunset_unix = weather.get_sunset_time()
      sunset = change_time_format(sunset_unix)

      #print(weather.get_visibility_distance())
      

      #Different logical specified weather dicts 
      wind_dict = {'Wind speed' : str(wind_speed) + ' m/s'
                   ,'Wind direction' : str(wind_deg) + u'\N{DEGREE SIGN}'
                  }
      
      sky_condition = {'Cloud cover': str(weather.get_clouds()) + '%'
                       ,'Sky' : weather.get_detailed_status()
                      }
      
      precipitation_dict = {'Humidity' : str(weather.get_humidity()) + '%'
                           ,'Rain volume last 3h' : weather.get_rain()
                           ,'Snow volume last 3h' : weather.get_snow()
                          }
      temp_dict = {'Temperature' : str(temperature) + u'\N{DEGREE SIGN}' + 'C'
                    #,'Dew point' : str(dew_point)  + u'\N{DEGREE SIGN}' + 'C'
                  }
      
      sun_dict = {'Sunrise' : sunrise
                  ,'Sunset' : sunset
                  }
      
      pressure_dict = {'Pressure' : str(press_local) + ' hPa'
                        ,'Pressure at sea level' : str(press_sea) + ' hPa'
                      }

    #end of observation if    
  
    #-----------------------------------------------------------------------
    #FORECAST
    #-----------------------------------------------------------------------
    today_fc_3h = 'Forecast for today:'
    tomorrow_fc_3h = 'Forecast for tomorrow:'
    seven_days_fc = 'Forecast for the next 3 days:'

    if key == 'forecast3':
      for weather_part in weather:
        for times in fc_times_today:
          if weather_part.get_reference_time('iso') == times: 
            time_string = str(weather_part.get_reference_time('iso'))
            fc3_datetime = dt.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S+%f")
            #str
            today_fc_3h += '\n' + str(fc3_datetime) + ' '+ str(weather_part.get_detailed_status())
        for times in fc_times_tomorrow:
          if weather_part.get_reference_time('iso') == times:
            time_string = str(weather_part.get_reference_time('iso'))
            fc3_datetime = dt.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S+%f")
            #str
            tomorrow_fc_3h += '\n' + str(fc3_datetime) + ' ' + str(weather_part.get_detailed_status())
            
    if key == 'forecast_daily':
      for weather_part in weather:
        time_string = weather_part.get_reference_time('iso')
        fcd_datetime = dt.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S+%f")
        fcd_date = fcd_datetime.date()
        for days in fcd_vec:
          if str(days) in str(fcd_date): 
            #STATUS
            caption = '[STATUS] '
            caption_bold = us.color.BOLD + '[STATUS] ' + us.color.END
            caption_red = us.color.RED + caption_bold  + us.color.END
            #str
            seven_days_fc += '\n' + caption_bold + str(fcd_date) 
            seven_days_fc += '\nForecast: '+ str(weather_part.get_detailed_status())
            seven_days_fc += '\nCloud cover: '+ str(weather_part.get_clouds()) + '%'
              
            #TEMP
            fc_temp_daily = weather_part.get_temperature(unit='celsius')
            fc_temp_daily_morn = str(fc_temp_daily['morn']) + u'\N{DEGREE SIGN}' + 'C'
            fc_temp_daily_day = str(fc_temp_daily['day']) + u'\N{DEGREE SIGN}' + 'C'
            fc_temp_daily_eve = str(fc_temp_daily['eve']) + u'\N{DEGREE SIGN}' + 'C'
            fc_temp_daily_night = str(fc_temp_daily['night']) + u'\N{DEGREE SIGN}' + 'C'
            fc_temp_daily_max = str(fc_temp_daily['max']) + u'\N{DEGREE SIGN}' + 'C'
            fc_temp_daily_min = str(fc_temp_daily['min']) + u'\N{DEGREE SIGN}' + 'C'
            caption = '[TEMP] '
            caption_bold = us.color.BOLD + '[TEMP] ' + us.color.END
            caption_red = us.color.RED + caption  + us.color.END
            #str
            seven_days_fc += '\n' + caption_bold +'\nMorning: %s \nDay: %s \nEvening: %s \nNight: %s' \
                            % (fc_temp_daily_morn, fc_temp_daily_day, fc_temp_daily_eve, fc_temp_daily_night)

            #WIND
            fc_wind_daily = weather_part.get_wind()
            fc_wind_speed_daily = fc_wind_daily['speed']
            caption = '[WIND] '
            caption_bold = us.color.BOLD + '[WIND] ' + us.color.END
            caption_red = us.color.RED + caption  + us.color.END
            #str
            seven_days_fc += '\n' + caption_bold  +'\n' + 'Average: ' + str(fc_wind_speed_daily) + ' m/s'

            #RAIN
            fc_rain_daily_raw = weather_part.get_rain()
            caption = '[PRECIPITATION] '
            caption_bold = us.color.BOLD + '[PRECIPITATION] ' + us.color.END
            caption_red = us.color.RED + caption  + us.color.END
            try:
              fc_rain_daily = fc_rain_daily_raw['all']
              #str
              seven_days_fc += '\n' + caption_bold  + '\n' + 'Rain: ' + str(fc_rain_daily) + ' mm'
            except:
              fc_rain_daily = 'No rain :)'
              #str
              seven_days_fc += '\n' + caption_bold  + '\n' + 'Rain: ' + str(fc_rain_daily)  

            seven_days_fc += '\n'+'-----------------------------------------------------------------'

    #test=fc_object_daily.when_starts('iso')
    #print(owm.weather_history_at_place('London, uk'))
    #-----------------------------------------------------------------------
    #Create output for message
    #-----------------------------------------------------------------------
    if key == 'forecast3':
      output += '\n'+'#################################################################'
      output += '\n' + today_fc_3h
      #output += '\n'+'-----------------------------------------------------------------'
      #output += '\n' + tomorrow_fc_3h
    if key == 'forecast_daily':
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n' + seven_days_fc
      output += '\n'+'#################################################################'
    if key == 'observation':
      output +='\n' + 'Weather observations %s %s(%s, %s):' % (time_of_obs,city,lat,lon)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+pp_str(sun_dict)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+pp_str(temp_dict)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+pp_str(pressure_dict)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+pp_str(wind_dict)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+pp_str(precipitation_dict)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+pp_str(sky_condition)
      output += '\n'+'-----------------------------------------------------------------'
      output += '\n'+'#################################################################'
 #output += '\n' + str(test1)
  #output += '\n' + str(test2)
  #output += '\n' + str(test3)
  #output += '\n' + str(test4)
  return output
