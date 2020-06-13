#!/usr/bin/env python3
#Weather program using OpenWeatherMap

import weather_script as ws
import useful_stuff as us
import os
import sys
import time

#-----------------------------------------------------------------------
#Dictionaries for Cities and Users(Email)
#-----------------------------------------------------------------------


city_dict = {'Dortmund': 'Dortmund' + ', ger'
            ,'Hamburg': 'Hamburg' + ', ger'
            ,'Luebeck': 'Luebeck' + ', ger'
            ,'Koeln': 'Koeln' + ', ger'
            ,'Duesseldorf': 'Duesseldorf' + ', ger'
            ,'Essen': 'Essen' + ', ger'
            ,'Muenchen': 'Muenchen' + ', ger'
            ,'Madison': 'Madison' + ', us'
            ,'Oslo': 'Oslo' + ', no'
            ,'Noordwijk': 'Noordwijk' + ', nl'
            ,'Osnarbrueck': 'Osnarbrueck' + ', ger'
            ,'Frankfurt': 'Frankfurt' + ', ger'
            ,'Karlsruhe': 'Karlsruhe' + ', ger'
            }

email_dict = {'Lukas': 'lukasmuessle@gmail.com'
              ,'Alex': 'a.craemer@gmail.com' 
              ,'LukasWork': 'lukas.muessle@nttdata.com' 
              ,'Florian': 'florian@mail-arends.de' 
              ,'Frederic': 'frederic.krehl@nttdata.com' 
              ,'Micha': 'michael.menzel@nttdata.com' 
              ,'Friedel': 'sagzero@gmx.de' 
              ,'Jonathan': '' 
              ,'Jobst': 'jobstmuesse@gmail.com' 
              ,'Tim': 'tim.muessle@gmx.de' 
              }

#lukas_cities = ['Koeln', 'Duesseldorf','Dortmund']
lukas_cities = ['Luebeck']
lukas_work_cities = ['Karlsruhe']
alex_cities = ['Luebeck']
florian_cities = ['Osnarbrueck', 'Frankfurt']
frederic_cities = ['Muenchen']
micha_cities = ['Koeln']
friedel_cities = ['Noordwijk']
jonathan_cities = ['Oslo']
jobst_cities = ['Madison']
tim_cities = ['Essen']

user_cities = {'Lukas': lukas_cities
            ,'Alex': alex_cities
            ,'LukasWork': lukas_work_cities
            ,'Florian': florian_cities
            ,'Frederic': frederic_cities
            ,'Micha': micha_cities
            ,'Friedel': friedel_cities
            ,'Jonathan': jonathan_cities
            ,'Jobst': jobst_cities
            ,'Tim': tim_cities
            }

users = ['Lukas'
        , 'Alex'
        , 'LukasWork'
        , 'Florian'
        , 'Frederic'
        , 'Micha'
        , 'Friedel'
        #, 'Jonathan'
        , 'Jobst'
        , 'Tim'
        ]
#users = ['Lukas', 'LukasWork', 'Alex', 'Florian']
users = ['Lukas', 'LukasWork', 'Florian']
#users = ['Lukas']

for user in users:
 
  #-----------------------------------------------------------------------
  #Email configuration
  #-----------------------------------------------------------------------
  pwd_file_name = 'python_mailing_bot.txt'
  pwd_file_loc = os.environ['HOME'] + '/Documents/'
 
  #reads first line of the file 
  pwd_mail = us.read_certain_line(pwd_file_name,pwd_file_loc,0)
  
  #email addr
  email_dict_keys_list = list(email_dict.keys())
  to_addrs  = email_dict[user]

  #setup the content of the email 
  
  #---------------------------------------------------------------------
  #test_flag is email_on=0
  email_on=1
  #---------------------------------------------------------------------

  #format of email
  if email_on == 1:
    text_format = 'html'
  else:
    text_format = 'plain'
  subject = 'Wetterbericht fuer ' + str(user) + ' [PROTOTYP]'

  #body of email with error handling
  if email_on == 0:
  #no error handling for testing
    for cities_var in user_cities[user]:
      body_msg = 'Einen schoenen guten Morgen, %s!' % (str(user))
      body_msg += str(ws.current_weather(city_dict[cities_var]))
      body_msg += '\n'
  else:
    retries = 4
    for i in range(retries):
      try:
        body_msg = 'Einen schoenen guten Morgen, %s!' % (str(user))
        body_msg += '\nDiese Staedte hast du abonniert:'
        for cities_var in user_cities[user]:
          body_msg += str(ws.current_weather(city_dict[cities_var]))
          body_msg += '\n'
      except OSError as err:
        print("OS error: {0}".format(err))
        raise
      except ValueError:
        print("%%%Value Error.%%%")
        raise
      except KeyError:
        print("%%%City name error.%%% \n", sys.exc_info())
        print("%%%Variable Information.%%% \n", user, cities_var)
        raise
      except:
        #for what ever reason it fails sometimes 
        #we will try 3 times
        if i < retries-1:
          time.sleep(5) # delays for 5 seconds
          continue
        elif i ==  retries-1:
          print('Es wurden %s Versuche unternommen!' %(i))
          print("Unexpected error:", sys.exc_info()[0])
          raise
      break

  body_msg += '\nBeste Gruesse,'
  body_msg += '\nLukas'
  
  #converts \n into html code
  if text_format == 'html':
    body_msg = body_msg.replace("\n", "<br />")
    bold_open='<b>'
    bold_close='</b>'
    body_msg = body_msg.replace(us.color.BOLD, bold_open)
    body_msg = body_msg.replace(us.color.END, bold_close)


  #send actual mail in html oder plain text 
  if email_on == 1:
    us.send_mail(to_addrs, subject, body_msg, pwd_mail, text_format)
  else:
    print(body_msg)
    #print(ws.current_weather(city_dict['Noordwijk']))


