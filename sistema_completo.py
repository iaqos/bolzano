# -*- coding: utf-8 -*-
"""sistema completo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fQFzi_lsus-RTAEbBCcM8fRHP0dJDxFe
"""

from google.colab import drive
drive.mount('/content/drive')

data_path = "drive/MyDrive/Colab Notebooks/Definitivi/Outputs/"

# © Iaqos Bolzano
# Classifier training


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from joblib import dump, load

block = True


# Import, divide and encode data
# in caso si volesse il vecchio file per i test
# data_x = pd.read_csv(data_path + 'data_clean.csv', index_col=0)
data_x = pd.read_csv(data_path + 'data_clean_mapped_2.csv')
data_y = pd.read_csv(data_path + 'data_clustered.csv')

data_x.head(10)

# Commented out IPython magic to ensure Python compatibility.
temp_x = data_x.drop(['Index'], axis=1)
temp_y = data_y.drop(['Label'], axis=1)

colonne_considerate = ['Come ti comporti sui social? ','Pregando di finire in zona gialla','Quando ti trovi in una situazione nuova, circondat* da persone che vedi per la prima volta','Rabbia_inquinamento', 'Rabbia_sessismo', 'Rabbia_sensocivico','Rabbia_capitalismo', 'Rabbia_evasione', 'Rabbia_chiasso','Rabbia_razzismo','Preoccupazione_personale', 'Preoccupazione_altri','Preoccupazione_inquinamento', 'Preoccupazione_tecnologia','Preoccupazione_relazioni','Sei tesserat* o fai vita associativa?',"Misuriamo l'umore, come ti senti ora?","Pensi che questo stato d'animo si prolungherà nel tempo?",'Bisogno_evoluzione', 'Bisogno_verde', 'Bisogno_viabilita','Bisogno_sicurezza', 'Bisogno_equita','Cosa pensi se dico "Intelligenza Artificiale"?']

temp_x = temp_x.loc[:,colonne_considerate]

dataset = pd.concat([temp_x, temp_y], axis=1)
dataset = dataset.sample(frac=1).reset_index(drop=True)

x_set = dataset.drop(['Cluster'], axis=1).values
y_set = dataset['Cluster'].values

enc = OneHotEncoder()
enc.fit(x_set)
x_enc = enc.transform(x_set)


# Set split and check if all classes are contained in test set
while block:

	x_train, x_test, y_train, y_test = train_test_split(x_enc,y_set,test_size=0.1)

	blocker = 0
	for check in range(6):
		if check in y_test:
			pass
		else:
			blocker += 1

	if blocker == 0:
		block = False
	else:
		block = True


# Train classifier
print('Training SVM')
print()
C_range = np.logspace(-1, 4, 6)
C_range = np.concatenate((C_range,C_range*5))
gamma_range = np.logspace(-4, 1, 6)
gamma_range = np.concatenate((gamma_range,gamma_range*5))

parameters_svm = {'gamma':gamma_range, 'C':C_range}
svc = svm.SVC(kernel='rbf', decision_function_shape='ovr', break_ties=False)
grid_svm = GridSearchCV(svc, parameters_svm, cv=4, n_jobs=-1)

grid_svm.fit(x_train,y_train)

print("The best parameters are %s with a score of %0.2f"
#       % (grid_svm.best_params_, grid_svm.best_score_))

svc = grid_svm.best_estimator_

y_pred = svc.predict(x_test)

print()
print('Test Accuracy SVC = ', accuracy_score(y_test,y_pred))
print()
print(confusion_matrix(y_test,y_pred))   
print()

dump(svc, data_path + 'iaqos_svc_nuovo_social_numero_prova.joblib')

### GIOCO

svc = load(data_path + 'iaqos_svc_nuovo_2.joblib')

S = [[1.0,'spettacolo','inquadro_persone','rabbia_inquinamento_si','rabbia_sessismo_si','rabbia_sensocivico_si','rabbia_capitalismo_si','rabbia_evasione_si','rabbia_chiasso_si','rabbia_razzismo_no','preoccupazione_personale_no','preoccupazione_altri_si','preoccupazione_inquinamento_no','preoccupazione_tecnologia_no','preoccupazione_relazioni_no','non_rappresentato','Così, così','umore_prolungato_no','bisogno_evoluzione_no','bisogno_verde_no','bisogno_viabilita_no','bisogno_sicurezza_no','bisogno_equita_no','ia_alleata']]

S_enc = enc.transform(S)

T = svc.predict(S_enc)

print(T)

data_x

data_x = pd.read_csv(data_path + 'data_clean_mapped_2.csv')

svc = load(data_path + 'iaqos_svc_nuovo_social_numero.joblib')
colonne_considerate = ['Come ti comporti sui social? ','Pregando di finire in zona gialla','Quando ti trovi in una situazione nuova, circondat* da persone che vedi per la prima volta','Rabbia_inquinamento', 'Rabbia_sessismo', 'Rabbia_sensocivico','Rabbia_capitalismo', 'Rabbia_evasione', 'Rabbia_chiasso','Rabbia_razzismo','Preoccupazione_personale', 'Preoccupazione_altri','Preoccupazione_inquinamento', 'Preoccupazione_tecnologia','Preoccupazione_relazioni','Sei tesserat* o fai vita associativa?',"Misuriamo l'umore, come ti senti ora?","Pensi che questo stato d'animo si prolungherà nel tempo?",'Bisogno_evoluzione', 'Bisogno_verde', 'Bisogno_viabilita','Bisogno_sicurezza', 'Bisogno_equita','Cosa pensi se dico "Intelligenza Artificiale"?']
data_x = data_x.loc[:,colonne_considerate]

data_x

ind = 0
pred = []
for i in data_x.values:
  S = [list(i)]
  S_enc = enc.transform(S)
  T = svc.predict(S_enc)
  print('indice:', ind, 'T:', T)
  pred.append(T[0])
  ind += 1

data_y.groupby('Cluster').count()

df_pred = pd.DataFrame(columns={'prediction'})
df_pred['prediction'] = pred
df_pred['sksk'] = pred
df_pred.head()
df_pred.groupby('prediction').count()

data_x.values[10]

data_x = pd.read_csv(data_path + 'data_clean_mapped_2.csv')
colonne_considerate = ['Come ti comporti sui social? ','Pregando di finire in zona gialla','Quando ti trovi in una situazione nuova, circondat* da persone che vedi per la prima volta','Rabbia_inquinamento', 'Rabbia_sessismo', 'Rabbia_sensocivico','Rabbia_capitalismo', 'Rabbia_evasione', 'Rabbia_chiasso','Rabbia_razzismo','Preoccupazione_personale', 'Preoccupazione_altri','Preoccupazione_inquinamento', 'Preoccupazione_tecnologia','Preoccupazione_relazioni','Sei tesserat* o fai vita associativa?',"Misuriamo l'umore, come ti senti ora?","Pensi che questo stato d'animo si prolungherà nel tempo?",'Bisogno_evoluzione', 'Bisogno_verde', 'Bisogno_viabilita','Bisogno_sicurezza', 'Bisogno_equita','Cosa pensi se dico "Intelligenza Artificiale"?']
temp_x = data_x.loc[:,colonne_considerate]
temp_x

enc = OneHotEncoder()
enc.fit(temp_x)

answer = temp_x.values[143]
a = [list(answer)]
answer = str(a)
print(type(answer))

import sklearn
print('sklearn:',sklearn.__version__)
import joblib
print('joblib:',joblib.__version__)
import numpy as np
print('numpy:',np.__version__)
import pandas as pd
print('pandas:',pd.__version__)

import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
from joblib import dump, load

data_x = pd.read_csv(data_path + 'data_clean_mapped_2.csv')
colonne_considerate = ['Come ti comporti sui social? ','Pregando di finire in zona gialla','Quando ti trovi in una situazione nuova, circondat* da persone che vedi per la prima volta','Rabbia_inquinamento', 'Rabbia_sessismo', 'Rabbia_sensocivico','Rabbia_capitalismo', 'Rabbia_evasione', 'Rabbia_chiasso','Rabbia_razzismo','Preoccupazione_personale', 'Preoccupazione_altri','Preoccupazione_inquinamento', 'Preoccupazione_tecnologia','Preoccupazione_relazioni','Sei tesserat* o fai vita associativa?',"Misuriamo l'umore, come ti senti ora?","Pensi che questo stato d'animo si prolungherà nel tempo?",'Bisogno_evoluzione', 'Bisogno_verde', 'Bisogno_viabilita','Bisogno_sicurezza', 'Bisogno_equita','Cosa pensi se dico "Intelligenza Artificiale"?']
temp_x = data_x.loc[:,colonne_considerate]


svc = load(data_path + 'iaqos_svc_nuovo_social_numero.joblib')
enc = OneHotEncoder()
enc.fit(temp_x)

def main(answer):
  print('answer', answer)
  S = eval(answer)
  S_enc = enc.transform(S)
  T = svc.predict(S_enc)
  print('Secondo IAQOS appartieni al cluster {}'.format(T[0]))
  return T

if __name__ == "__main__":
  main()



for col in temp_x.columns:
  print(col)
  print(set(temp_x[col]))
  print()

df_new.head(1)

# dizionari per la traduzione

trad_social = {
    1.0: 1.0,
    2.0: 2.0,
    3.0: 3.0,
    4.0: 4.0,
    5.0: 5.0,
    6.0: 6.0,
    7.0: 7.0
 }

trad_zona_gialla = {
    "Rimango fedele all'appartamento, il mio habitat del cuore": "appartamento",
    'Mi gusto uno spettacolo dal vivo': "spettacolo",
    "Improvviso un'escursione in qualsiasi zona purché sia fuori Comune": "escursione",
    'Imploro un aperitivo con gli amici': "aperitivo"}

trad_persone_nuove = {
    "Aspetto che qualcun* parli per interagire, ma non vedevo l'ora che qualcun* avviasse la conversazione": 'aspetto_qualcuno_volgia_1',
    'Rompo il ghiaccio, vado a ruota libera': 'rompo_giaccio',
    'Aspetto che mi coinvolgano le altre persone': 'aspetto_basta',
    'Cerco di inquadrare le persone prima di espormi': 'inquadro_persone',
    'Se potessi mi smaterializzerei': 'scapperei',
    "Aspetto che qualcun* parli per interagire, ma non vedo l'ora che qualcun* avvii la conversazione": 'aspetto_qualcuno_volgia_2'
}

trad_rabbia = {
    'No': 'rabbia_inquinamento_no',
    'Si': 'rabbia_inquinamento_si'
}

trad_rabbia_sessismo = {
    'No': 'rabbia_sessismo_no',
    'Si': 'rabbia_sessismo_si'
}

trad_rabbia_sensocivico = {
    'No': 'rabbia_sensocivico_no',
    'Si': 'rabbia_sensocivico_si'
}

trad_rabbia_capitalismo = {
    'No': 'rabbia_capitalismo_no',
    'Si': 'rabbia_capitalismo_si'
}

trad_rabbia_evasione = {
    'No': 'rabbia_evasione_no',
    'Si': 'rabbia_evasione_si'
}

trad_rabbia_chiasso = {
    'No': 'rabbia_chiasso_no',
    'Si': 'rabbia_chiasso_si'
}

trad_rabbia_razzismo = {
    'No': 'rabbia_razzismo_no',
    'Si': 'rabbia_razzismo_si'
}

trad_preoccupazione_personale = {
    'No': 'preoccupazione_personale_no',
    'Si': 'preoccupazione_personale_si'
}

trad_preoccupazione_altri = {
    'No': 'preoccupazione_altri_no',
    'Si': 'preoccupazione_altri_si'
}

trad_preoccupazione_inquinamento = {
    'No': 'preoccupazione_inquinamento_no',
    'Si': 'preoccupazione_inquinamento_si'
}

trad_preoccupazione_tecnologia = {
    'No': 'preoccupazione_tecnologia_no',
    'Si': 'preoccupazione_tecnologia_si'
}

trad_preoccupazione_relazioni = {
    'No': 'preoccupazione_relazioni_no',
    'Si': 'preoccupazione_relazioni_si'
}

trad_vita_associativa = {
    'Non sono iscritt* a nulla perché in fondo non mi interessa': 'non_interessato',
    'Mi iscriverei, ma la verità è che non mi sento rappresentat*': 'non_rappresentato',
    'Certo! Sostengo associazioni, organizzazioni, partiti o simili': 'iscritto'
    }
trad_umore = {
    'Bene': "umore_bene",
    'Alla grande': "umore_alla_grande",
    'Male': "umore_male",
    'Così,così': "umore_circa",
    "Di peggio non c'è": "umore_malissimo"
}

trad_umore_prolungato = {
    'No': 'umore_prolungato_no',
    'Chissà': 'umore_prolungato_forse',
    'Si': 'umore_prolungato_si'
}

trad_bisogno_evoluzione = {
    'No': 'bisogno_evoluzione_no',
    'Si': 'bisogno_evoluzione_si'
}

trad_bisogno_verde = {
    'No': 'bisogno_verde_no',
    'Si': 'bisogno_verde_si'
}

trad_bisogno_viabilita = {
    'No': 'bisogno_viabilita_no',
    'Si': 'bisogno_viabilita_si'
}

trad_bisogno_sicurezza = {
    'No': 'bisogno_sicurezza_no',
    'Si': 'bisogno_sicurezza_si'
}

trad_bisogno_equita = {
    'No': 'bisogno_equita_no',
    'Si': 'bisogno_equita_si'
}

trad_ia = {
    'Può essere una valida alleata degli umani': 'ia_alleata',
    "Non credo che possa esistere un'Intelligenza Artificiale": 'ia_scettico',
    'Una cosa entusiasmante': 'ia_entusiasta',
    'Scenari tipo Terminator': 'ia_terminator',
    'È una questione delicata che dobbiamo gestire': 'ia_delicata',
    'Non mi interessa': 'ia_disinteresse',
    'Non ho idea di cosa sia, ma sono curios*': 'ia_curioso'
}

# lista dei dizionari per la traduzione
list_trad = [trad_social,trad_zona_gialla,trad_persone_nuove,trad_rabbia,trad_rabbia_sessismo,trad_rabbia_sensocivico,trad_rabbia_capitalismo,trad_rabbia_evasione,trad_rabbia_chiasso,trad_rabbia_razzismo,trad_preoccupazione_personale,trad_preoccupazione_altri,trad_preoccupazione_inquinamento,trad_preoccupazione_tecnologia,trad_preoccupazione_relazioni,trad_vita_associativa,trad_umore,trad_umore_prolungato,trad_bisogno_evoluzione,trad_bisogno_verde,trad_bisogno_viabilita,trad_bisogno_sicurezza,trad_bisogno_equita,trad_ia]
len(list_trad)

# copia del df iniziale, per non perdere dati
#df_new = temp_x.copy()
df_new = pd.read_csv(data_path + 'data_clean.csv')
colonne_considerate = ['Come ti comporti sui social? ','Pregando di finire in zona gialla','Quando ti trovi in una situazione nuova, circondat* da persone che vedi per la prima volta','Rabbia_inquinamento', 'Rabbia_sessismo', 'Rabbia_sensocivico','Rabbia_capitalismo', 'Rabbia_evasione', 'Rabbia_chiasso','Rabbia_razzismo','Preoccupazione_personale', 'Preoccupazione_altri','Preoccupazione_inquinamento', 'Preoccupazione_tecnologia','Preoccupazione_relazioni','Sei tesserat* o fai vita associativa?',"Misuriamo l'umore, come ti senti ora?","Pensi che questo stato d'animo si prolungherà nel tempo?",'Bisogno_evoluzione', 'Bisogno_verde', 'Bisogno_viabilita','Bisogno_sicurezza', 'Bisogno_equita','Cosa pensi se dico "Intelligenza Artificiale"?']
df_new = df_new.loc[:,colonne_considerate]

df_new.head()

# ciclo per la sostituzione
for (i,c) in enumerate(df_new.columns):
  df_new[c] = df_new[c].map(list_trad[i]).fillna(df_new[c])

# Alcune sono buggate non so come mai

# colonna nr. 2 | Quando ti trovi in una situazione nuova, circondat* da persone che vedi per la prima volta
df_new.iloc[:,2] = df_new.iloc[:,2].map(trad_persone_nuove).fillna(df_new.iloc[:,2])

# colonna nr. 15 | Sei tesserat* o fai vita associativa?
df_new.iloc[:,15] = df_new.iloc[:,15].map(trad_vita_associativa).fillna(df_new.iloc[:,15])

# test per vedere le traduzioni fatte
for i,col in enumerate(df_new.columns):
  print(i,col)
  print(set(df_new[col]))
  print()

# Aggiunta dell'indice, non necessario ma l'ho fatto
df_new['Index'] = data_x['Index']

# spostamento dell'ultima colonna (colonna Index) al primo posto, anche questo non è necessario ma pensavo lo fosse
cols = list(df_new.columns)
cols = [cols[-1]] + cols[:-1]
df_new = df_new[cols]

# salvataggio del nuovo df come csv
df_new.to_csv(data_path + "data_clean_mapped_3.csv", index = False)