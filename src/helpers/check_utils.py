import socket
import re
import psutil
from typing import TypedDict
import requests

class ProcessFound(TypedDict):
  pid: str
  name: str
  status: str

def check_multiple_ports(ports:list, host:str="localhost") -> dict[str, bool]:
  result = {}
  for port in ports: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result[port] = sock.connect_ex((host, int(port))) == 0
    sock.close()
  return result

def check_proccess(process:list[str]) -> list[ProcessFound]:
  result = []
  for proc in psutil.process_iter(['pid', 'name', 'status']):
    for item in process:
      if not re.search(item.lower(), proc.info['name'].lower()): continue
      result.append({
        'pid': proc.info['pid'],
        'name': proc.info['name'],
        'status': proc.info['status'],
      })
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