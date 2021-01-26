import base64, io, os, json, pandas as pd
from apyori import apriori, dump_as_json
from io import StringIO
import matplotlib.pyplot as plt, mpld3
import seaborn as sb 
import scipy.cluster.hierarchy as shc
import functools
import numpy as np
from scipy.spatial import distance
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator
import joblib

Matriz = None
headers = None
Clasificacion = joblib.load('modelo.pkl')

def read_file(file, filename, **kwargs):
  read_map = {
    'xls': pd.read_excel, 
    'xlsx': pd.read_excel, 
    'csv': pd.read_csv,
    'gz': pd.read_csv,
    'txt' : pd.read_table
  }
  ext = os.path.splitext(filename)[1].lower()[1:]
  assert ext in read_map, "Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl; current format '{0}'".format(ext)
  return read_map[ext](file, error_bad_lines = False, **kwargs)

def df_to_json(data_frame):
  df1 = data_frame.where(pd.notnull(data_frame), None)
  registros = json.loads(data_frame.to_json(orient='records'))
  headers = [{'text': str(data), 'value': str(data), 'sortable': False} for data in df1]
  return registros, headers

def alg_apriori(df, **kwargs):
  data_frame = df.copy()
  data_frame.fillna(0, inplace=True)
  registros = []
  for i in range(0, len(data_frame)):
    registros.append([str(data_frame.values[i,j]) for j in range(0, data_frame.shape[1])])
  Reglas = apriori(registros, **kwargs)
  Resultados = list(Reglas)
  output = []
  for item in Resultados:
    o = {}
    o['items_base'] = [(x) for x in item[2][0][0] if x != 'nan']
    o['items_add'] = [(x) for x in item[2][0][1] if x != 'nan']
    o['support'] = item[1]
    o['confidence'] = item[2][0][2]
    o['lift'] = item[2][0][3]
    if '0' not in o['items_add']:
      output.append(o)
  return output

def alg_correlaciones(data_frame, **kwargs):
  global Matriz, headers
  Matriz = data_frame.corr(method='pearson')
  headers = [data for data in Matriz]
  matriz_correlaciones = []
  for index, row in Matriz.iterrows():
    data = {}
    for col in headers:
      data[col] = round(row[col], 4)
    matriz_correlaciones.append(data)
  matriz_correlaciones.reverse()
  return matriz_correlaciones

def headers_correlaciones():
  return [{'text': str(data), 'value': str(data), 'sortable': False} for data in headers]

def map_correlaciones():
  data = []
  for index, row in Matriz.iterrows():
    for col in headers:
      data.append({"value": round(row[col], 4)})
  return data

def heat_map():
  plt.figure(figsize = (20,10))
  sb.heatmap(Matriz, annot = True)  
  fig = plt.gcf()
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  return base64.b64encode(buf.getvalue())


def distancias(df):
  data_frame = pd.DataFrame()
  Matriz = (df.copy()).corr(method='pearson')
  for data in Matriz:
    data_frame[data] = df[data]
  E = []
  for row in data_frame.iloc:
    E.append(row.tolist())
  response = {}
  response['headers'] = [{'text': str("id"), 'value': str("id"), 'sortable': True}]
  response['headers'] += [{'text': str(i), 'value': str(i), 'sortable': True} for i in range (0, len(E))]
  response['euclidean'] = []
  response['chebyshev'] = []
  response['cityblock'] = []
  response['minkowski'] = []
  for i, e1 in enumerate(E):
    euclidean = {'id' : i}
    chebyshev = {'id' : i}
    cityblock = {'id' : i}
    minkowski = {'id' : i}
    for j, e2 in enumerate(E):
      euclidean[j] = float(round(distance.euclidean(e1, e2), 4))
      chebyshev[j] = float(round(distance.chebyshev(e1, e2), 4))
      cityblock[j] = float(round(distance.cityblock(e1, e2), 4))
      minkowski[j] = float(round(distance.minkowski(e1, e2), 4))
    response['euclidean'].append(euclidean)
    response['chebyshev'].append(chebyshev)
    response['cityblock'].append(cityblock)
    response['minkowski'].append(minkowski)
  return response

def clustering_jerarquico(df, headers):
  data_frame = df.copy()
  def add_node(node, parent):
    newNode = dict( node_id=node.id, d=node.dist , c=[])
    parent["c"].append( newNode )
    if node.left: add_node( node.left, newNode )
    if node.right: add_node( node.right, newNode )

  def label_tree(n):
    if len(n["c"]) == 0:
      leafNames = [id2name[n["node_id"]]]
    else:
      leafNames = functools.reduce(lambda ls, c: ls + label_tree(c), n["c"], [])
    del n["node_id"]
    if len(leafNames) == 1:
      n["n"] = name = "(" + ",".join(sorted(map(str, leafNames))) + ")"
    return leafNames

  variables = pd.DataFrame()
  if(len(headers) == 0):
    Matriz = data_frame.corr(method='pearson')
    for data in Matriz:
      variables[data] = data_frame[data]
  else:
    for data in headers:
      if data['select']:
        variables[data['text']] = data_frame[data['text']]
  
  Arbol = shc.to_tree(shc.linkage(variables, method='complete'))
  labels = [i for i in range(len(variables))]
  id2name = dict(zip(range(len(labels)), labels))
  d3Dendro = dict(c=[], name="Root1")
  add_node(Arbol, d3Dendro)
  label_tree(d3Dendro["c"][0])

  VariablesModelo = np.array(data_frame[[data for data in variables]])
  MJerarquico = AgglomerativeClustering(
    n_clusters=5, 
    affinity='euclidean', 
    linkage='complete'
  )
  MJerarquico.fit_predict(VariablesModelo)
  data_frame['cluster'] = MJerarquico.labels_
  cluster_count = data_frame.groupby(['cluster'])['cluster'].count()

  response = {}
  response['dendrograma'] = d3Dendro
  response['count'] = [data for data in cluster_count]
  return response


def clusters_jerarquico(df, headers, n_clusters = 4):
  data_frame = df.copy()
  variables = pd.DataFrame()
  if(len(headers) == 0):
    Matriz = data_frame.corr(method='pearson')
    for data in Matriz:
      variables[data] = data_frame[data]
  else:
    for data in headers:
      if data['select']:
        variables[data['text']] = data_frame[data['text']]
  VariablesModelo = np.array(data_frame[[data for data in variables]])
  MJerarquico = AgglomerativeClustering(
    n_clusters=n_clusters, 
    affinity='euclidean', 
    linkage='complete'
  )
  MJerarquico.fit_predict(VariablesModelo)
  data_frame['Cluster'] = MJerarquico.labels_
  cluster_count = data_frame.groupby(['Cluster'])['Cluster'].count()
  Centroides = data_frame.groupby(['Cluster'])[['Cluster'] + [data for data in variables]].mean()

  series = []
  for c in range(len(cluster_count)):
    series.append({"name": "cluster-" + str(c), "data" : []})
    for i in range(len(VariablesModelo[:,0])):
      if MJerarquico.labels_[i] == c:
        series[c]['data'].append([VariablesModelo[i,0], VariablesModelo[i,1]])
  response = {}
  response['count'] = [{"name": "Clúster", "data": [data for data in cluster_count]}]
  response['table'], response['headers'] = df_to_json(Centroides)
  response['series'] = series
  return response

def elbow_method(df, headers):
  data_frame = df.copy()
  variables = pd.DataFrame()
  if(len(headers) == 0):
    Matriz = data_frame.corr(method='pearson')
    for data in Matriz:
      variables[data] = data_frame[data]
  else:
    for data in headers:
      if data['select']:
        variables[data['text']] = data_frame[data['text']]
  VariablesModelo = np.array(data_frame[[data for data in variables]])
  
  SSE = []
  for i in range(2, 16):
    km = KMeans(n_clusters=i, random_state=0)
    km.fit(VariablesModelo)
    SSE.append(km.inertia_)
  kl = KneeLocator(range(2, 16), SSE, curve="convex", direction="decreasing")
  response = {}
  response['data'] = [[i + 2, round(SSE[i])] for i in range(len(SSE))]
  response['name'] = "SSE"
  return [[response], int(kl.elbow)]

def clusters_particional(df, headers, n_clusters = 0):
  data_frame = df.copy()
  variables = pd.DataFrame()
  if(len(headers) == 0):
    Matriz = data_frame.corr(method='pearson')
    for data in Matriz:
      variables[data] = data_frame[data]
  else:
    for data in headers:
      if data['select']:
        variables[data['text']] = data_frame[data['text']]
  VariablesModelo = np.array(data_frame[[data for data in variables]])
  MParticional = KMeans(n_clusters=n_clusters, random_state=0).fit(VariablesModelo)
  MParticional.predict(VariablesModelo)
  MParticional.labels_
  MParticional.fit_predict(VariablesModelo)
  data_frame['Cluster'] = MParticional.labels_
  cluster_count = data_frame.groupby(['Cluster'])['Cluster'].count()
  Centroides = data_frame.groupby(['Cluster'])[['Cluster'] + [data for data in variables]].mean()

  series = []
  for c in range(len(cluster_count)):
    series.append({"name": "cluster-" + str(c), "data" : []})
    for i in range(len(VariablesModelo[:,0])):
      if MParticional.labels_[i] == c:
        series[c]['data'].append([VariablesModelo[i,0], VariablesModelo[i,1]])
  response = {}
  response['count'] = [{"name": "Clúster", "data": [data for data in cluster_count]}]
  response['table'], response['headers'] = df_to_json(Centroides)
  response['series'] = series
  return response

def logistic(texture, area, compactness, concavity, symmetry, fractalDimension):
  NuevoPaciente2 = pd.DataFrame({
    'Texture': [texture], 
    'Area': [area], 
    'Compactness': [compactness], 
    'Concavity': [concavity], 
    'Symmetry': [symmetry], 
    'FractalDimension': [fractalDimension]})
  return int(Clasificacion.predict(NuevoPaciente2)[0])