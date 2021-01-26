import subprocess
import eel
import pandas as pd
import json
from io import StringIO

from functions import *

debug = False
df = None
registros = None

def start_web():
  if debug:
    subprocess.check_output('cd vue && npm run serve', shell=True)
  else:
    subprocess.check_output('cd vue && npm run build', shell=True)

def start_ell():
  if debug:
    eel.init('vue/public')
    eel.start({'port':8080}, mode='chrome-app')
    eel.show()
  else:
    eel.init('web')
    eel.start('index.html')

@eel.expose
def load_file(file, file_name,  header):
  global df
  kwargs = {}
  if not header: kwargs['header'] = None
  df = read_file(StringIO(file), file_name, **kwargs)

@eel.expose
def get_headers():
  try:
    return [{'text': str(data), 'value': str(data), 'sortable': False} for data in df]
  except:
    pass

@eel.expose
def get_headers_numeric():
  try:
    Matriz = df.corr(method='pearson')
    return [{'text': str(data), 'value': str(data), 'sortable': False} for data in Matriz]
  except:
    pass

@eel.expose
def get_table():
  global registros
  try:
    df1 = df.where(pd.notnull(df), None)
    registros = json.loads(df1.to_json(orient='records'))
    return registros
  except:
    pass

@eel.expose
def get_apriori(min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2):
  kwargs = {}
  kwargs['min_support'] = min_support
  kwargs['min_confidence'] = min_confidence
  kwargs['min_lift'] = min_lift
  kwargs['min_length'] = min_length
  try:
    return alg_apriori(df, **kwargs)
  except:
    pass

@eel.expose
def get_correlaciones(method='pearson'):
  kwargs = {}
  kwargs['method'] = 'pearson'
  try:
    return {
      "matriz" : alg_correlaciones(df, **kwargs),
      "headers": headers_correlaciones(),
      "map" : map_correlaciones()
    }
  except:
    pass

@eel.expose
def get_heat_map():
  try:
    return map_correlaciones()
  except:
    pass

@eel.expose
def get_headers_correlaciones():
  try:
    return headers_correlaciones()
  except:
    pass

@eel.expose
def get_html():
  img = heat_map().decode('UTF-8')
  return str(img)

@eel.expose
def get_distancias():
  return distancias(df)

@eel.expose
def get_jerarquico(headers):
  try:
    return clustering_jerarquico(df, headers)
  except:
    pass

@eel.expose
def get_clusters_jerarquico(headers, n_clusters = 4):
  try:
    return clusters_jerarquico(df, headers, int(n_clusters))
  except:
    pass

@eel.expose
def get_elbow(headers):
  try:
    return elbow_method(df, headers)
  except:
    pass

@eel.expose
def get_clusters_particional(headers, n_clusters = 0):
  return clusters_particional(df, headers, int(n_clusters))

@eel.expose
def get_regresion_logistica(texture, area, compactness, concavity, symmetry, fractalDimension):
  return logistic(texture, area, compactness, concavity, symmetry, fractalDimension)


if __name__ == '__main__':
  start_ell()