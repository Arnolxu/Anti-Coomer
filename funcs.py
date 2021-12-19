import psutil
import cpuinfo
def kusDili(tr:str):
  sesliler = ['i', 'a', 'e', 'ı', 'u', 'ü', 'o', 'ö']
  bsesliler = ['İ', 'A', 'E', 'I', 'U', 'Ü', 'O', 'Ö']
  ret = ""
  for i in tr:
    ret += i
    if i in sesliler:
      ret += "g" + i
    elif i in bsesliler:
      ret += "G" + i
  return ret

def turkDili(kd:str):
  return kd.replace('aga', 'a').replace('ege', 'e').replace('ıgı', 'ı').replace('igi', 'i').replace('ugu', 'u').replace('ügü', 'ü').replace('ogo', 'o').replace('ögö', 'ö').replace('AGA', 'A').replace('EGE', 'E').replace('IGI', 'I').replace('İGİ', 'İ').replace('UGU', 'U').replace('ÜGÜ', 'Ü').replace('OGO', 'O').replace('ÖGÖ', 'Ö')

def get_processor_name():
  return cpuinfo.cpu.info[0]['model name']
def get_ram():
  svmem = psutil.virtual_memory()
  return get_size(svmem.total)
def get_size(bytes, suffix="B"):
  """
  Scale bytes to its proper format
  e.g:
      1253656 => '1.20MB'
      1253656678 => '1.17GB'
  """
  factor = 1024
  for unit in ["", "K", "M", "G", "T", "P"]:
    if bytes < factor:
      return f"{bytes:.2f}{unit}{suffix}"
    bytes /= factor