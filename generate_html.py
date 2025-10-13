from datetime import datetime
from json import loads as parse
import pytz
import os
import re
import sys
BJTIME=pytz.timezone('Asia/Shanghai')
def detect_encoding(file_path):
  encodings=['utf-8', 'gbk', 'ansi']
  for encoding in encodings:
    try:
      with open(file_path,'r',encoding=encoding) as f:
        f.read()
      return encoding
    except UnicodeDecodeError:
      continue
  return 'utf-8'
with open("birthday.json",encoding=detect_encoding('birthday.json')) as f:
  birthday=parse(f.read())
def read_file_content(file_path):
  encoding=detect_encoding(file_path)
  try:
    with open(file_path, 'r', encoding=encoding) as f:
      content='\n'.join(f"<li>{line[2:]}</li>" if line[0]=='-' else f"<h2>{line}</h2>" for line in f.readlines())
      content=re.sub(r'(<h2>.*?</h2>)\s*(<li>.*?</li>(?:\s*<li>.*?</li>)*)',r'\1\n<ul>\n\2\n</ul>',content.strip(),flags=re.DOTALL)
    return content
  except Exception as e:
    return str(e)
def parse_date_from_filename(filename):
  try:
    base_name=os.path.splitext(filename)[0]
    if len(base_name)==6 and base_name.isdigit():
      year=int("20"+base_name[:2])
      month=int(base_name[2:4])
      day=int(base_name[4:6])
      return datetime(year, month, day)
  except (ValueError, IndexError):
    pass
  return None
def getExtra():
  datenow=datetime.now().astimezone(BJTIME).strftime("%m%d")
  if datenow in birthday:
    with open("birthday.html.part") as f:
      return f.read().replace('[[person]]',birthday[datenow])
  return ""
def formattime(date):
  date=date.astimezone(BJTIME)
  if os.name=='nt':
    return date.strftime("%Y年%#m月%#d日")
  else:
    return date.strftime("%Y年%-m月%-d日")
def formattimeDetail(date):
  date=date.astimezone(BJTIME)
  if os.name=='nt':
    return date.strftime("%Y年%#m月%#d日%H时%M分")
  else:
    return date.strftime("%Y年%-m月%-d日%H时%M分")
def read():
  homework_dir = "homework"
  files_with_dates = []
  for filename in os.listdir(homework_dir):
    file_path=os.path.join(homework_dir, filename)
    if os.path.isfile(file_path):
      date=parse_date_from_filename(filename)
      if date:
        files_with_dates.append((date,filename,file_path,f'<div id="top" class="top"><div id="topmiddle"><span class="linkButton" id="home">{formattime(date)}</span></div></div>'))
  files_with_dates.sort(key=lambda x: x[0],reverse=True)
  recent_files=files_with_dates[:5]
  output='\n'.join([f'{parseddate}\n<div class="block alignmiddle">{read_file_content(file_path)}</div>\n' for date, filename, file_path, parseddate in recent_files])
  return output
with open("template.html","r",encoding=detect_encoding('template.html')) as f,open("style.css","r",encoding=detect_encoding('style.css')) as fstyle,open('index.html','wb') as wfile:
  wfile.write(f.read().replace("{{content}}",read()).replace("{{generateTime}}",formattimeDetail(datetime.now())).replace("{{extra}}",getExtra()).replace("{{stylesheet}}",fstyle.read()).encode('utf-8'))
