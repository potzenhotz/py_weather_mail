#useful stuff


def read_certain_line(file_name,file_loc,linenumber):
  pwd_file = file_loc + file_name
  open_file = open(pwd_file)
  pwd_read = open_file.readlines()
  #pwd_mail = "".join(pwd_read.split())
  open_file.close()
  return pwd_read[linenumber]


def send_mail(to_addr, subject, body,password, text_format):
  import smtplib
  from email.mime.text import MIMEText
  from email.mime.multipart import MIMEMultipart
  
  from_addr = 'python.mailing.bot@gmail.com'

  msg = MIMEMultipart()
  msg['From'] = from_addr
  msg['To'] = to_addr
  msg['Subject'] = subject 
  if text_format == 'plain':
    msg.attach(MIMEText(body,'plain','utf-8'))
  elif text_format == 'html':
    msg.attach(MIMEText(body,'html'))
  msg_final = msg.as_string().encode('ascii')


  # Credentials (if needed)
  username = 'python.mailing.bot@gmail.com'

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(from_addr, to_addr, msg_final)
  server.quit()

def week_number():
  import datetime as dt
  
  today = dt.datetime.today()
  year = dt.datetime.date(today).isocalendar()[0]
  week_number = dt.datetime.date(today).isocalendar()[1]
  day_of_week = dt.datetime.date(today).isocalendar()[2]

  return week_number

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


