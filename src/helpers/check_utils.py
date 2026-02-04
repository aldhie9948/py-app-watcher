import socket
import re
import psutil
from typing import TypedDict
import requests

class ProcessFound(TypedDict):
  pid: str
  name: str
  status: str

def check_port(port:str, host:str="localhost") -> bool:
  result = False
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(0.5)
  result = sock.connect_ex((host, int(port))) == 0
  sock.close()
  return result

def check_proccess(process:str) -> bool:
  result = False
  for proc in psutil.process_iter(['pid', 'name', 'status']):
    if not re.match(process.lower(), proc.info['name'].lower()): continue
    else:
      result = proc.info['status'] == 'running'
      break
  return result

def check_website(urls: list[str], timeout:int = 10)->dict[str, bool]: 
  result = {}
  for url in urls:
    try:
      response = requests.get(url=url, timeout=timeout)
      result[url] = response.status_code == 200
    except:
      result[url] = False
  return result