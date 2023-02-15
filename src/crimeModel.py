class crimeModel:
  
  def __init__(self):
      self.model = self.trainModel()
    

  def trainModel(self):
        
      # Basics
      import pandas as pd
      
      
      
      # Models
      from sklearn.model_selection import train_test_split
      from sklearn.ensemble import RandomForestRegressor
      
      # Load dataset
      df = pd.read_json('https://www.datos.gov.co/resource/75fz-q98y.json?$limit=135000')
      
      
      
      # Convert colums to numeric categories
      
      df['armas_medios'], uniques_armas_medios = pd.factorize(df['armas_medios'])
      df['barrios_hecho'], uniques_barrios_hecho = pd.factorize(df['barrios_hecho'])
      df['zona'], uniques_zona = pd.factorize(df['zona'])
      df['nom_comuna'], uniques_nom_comuna = pd.factorize(df['nom_comuna'])
      df['conducta'], uniques_conducta = pd.factorize(df['conducta'])
      df['mes'], uniques_mes = pd.factorize(df['mes'])
      df['dia_semana'], uniques_mes = pd.factorize(df['dia_semana'])
      df['clasificaciones_delito'], uniques_clasificaciones = pd.factorize(df['clasificaciones_delito'])
      df['curso_de_vida'], uniques_vida = pd.factorize(df['curso_de_vida'])
      df['estado_civil_persona'], uniques_estado = pd.factorize(df['estado_civil_persona'])
      df['genero'], uniques_gender = pd.factorize(df['genero'])
      df['movil_agresor'], uniques_agresor = pd.factorize(df['movil_agresor'])
      df['movil_victima'], uniques_agresor = pd.factorize(df['movil_victima'])
      df["latitud"] = pd.to_numeric(df["latitud"], errors='coerce')
      df["longitud"] =pd.to_numeric(df["longitud"], errors='coerce')
      df['dia']= pd.to_numeric(df["dia"])


      self.conductas = uniques_conducta

      # Delete records out of AMB
      df = df.loc[(df['latitud']>= 6) & (df['latitud'] <= 8)]
      df = df.loc[(df['longitud'] >= -74) & (df['longitud'] <=-72)]
      
      df['mes'] = df['mes'].apply(lambda x: x+1)
      df['dia_semana'] = df['dia_semana'].apply(lambda x: x+1)
      
      """As rows containing any NAN value represent 7.32% del datasee,  we proced to remove such rows to allow better processing."""
      
      df.dropna(inplace=True)
      df.drop(['descripcion_conducta', 'orden', 'edad', 'ano'], axis=1, inplace=True)
      
      ### Training
      
      X = df[[ 'dia_semana', 'curso_de_vida', 'barrios_hecho', 'estado_civil_persona']]
      y = df[[ 'latitud', 'longitud','conducta']]
      
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
      
      accuracySet = []
      
      # Random Forest
      
      # After analysis of MSE, the best pearameters are :
      # Max_depth = 5 , Trees = 7
      
      model = RandomForestRegressor(max_depth=5, n_estimators=7)
      model.fit(X_train.values,y_train.values)
    

      return model


  def crimePrediction(self, lista):

    import numpy as np
    '''
    Parameteres are in a list in this order: 
    [dia_semana, curso_de_vida, barrios_hecho, estado_civil_persona]

    Should Respect that order, in other case model misunderstand data
    '''
    p = self.model.predict(np.reshape(lista, (1, 4)))[0]
    pFormal = { 'lat': p[0], 'lng':p[1], 'conduct':self.conductas[int(p[2])]}
    return pFormal
    
          
          

    