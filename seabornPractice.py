import seaborn as sns;
import matplotlib.pyplot as plt;
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
      "mysql+mysqlconnector://root:abc123@localhost/seabornplots?host=localhost?port=3306")

conn = engine.connect();

results = conn.execute("SELECT id,Nama from dataset").fetchall();
dfDatasets = pd.DataFrame(results);
dfDatasets.columns = results[0].keys();
dfDatasets = dfDatasets.set_index('id');

results1 = conn.execute("SELECT id,Nama from category").fetchall();
dfCategory = pd.DataFrame(results1);
dfCategory.columns = results1[0].keys();
dfCategory = dfCategory.set_index('id');

results2 = conn.execute("SELECT * from plot").fetchall();
dfPlot = pd.DataFrame(results2);
dfPlot.columns = results2[0].keys();
dfPlot = dfPlot.set_index('id');

def MainMenu() :
    inputUser = input('Seaborn Plots \n\n 1. Pilih DataSet \n 2. Keluar \n\nMasukkan Pilihan : ');
    return inputUser;

def PilihDataSet() : 
    print('\nList Datasets : \n');
    for index, row in dfDatasets.iterrows() :
        print(str(index) + '. ' + str(row['Nama']));
    inputUser = input('\nDataset Pilihan : ');
    return dfDatasets.loc[int(inputUser)]['Nama'].lower();

def PilihCategory() :
    print('\nList Categories : \n');
    for index, row in dfCategory.iterrows() :
        print(str(index) + '. ' + str(row['Nama']));
    inputUser = input('\nCategory Pilihan : ');
    return inputUser;

def PilihPlot(idCat) :
    print('\nList Plots : \n');
    for index, row in dfPlot[dfPlot['CategoryId'] == idCat].iterrows() :
        print(str(index) + '. ' + str(row['Nama']));
    inputUser = input('\nPlot Pilihan : ');
    return dfPlot.loc[int(inputUser)];

def PrintPlot(namaPlot, params, df) :
    if(namaPlot == 'Count') :
        sns.countplot(x=params["x"], data=df, hue=params["hue"], 
                    palette=params["palette"]).set_title(params["title"]);
    elif(namaPlot == 'Bar' or namaPlot == 'Box' or namaPlot == 'Violin') :
        sns.factorplot(x=params["x"], y=params["y"], data=df, 
                    hue=params["hue"], kind=namaPlot.lower(),
                    palette=params["palette"]).axes.flat[0].set_title(params["title"]);
    elif(namaPlot == 'Strip') :
        sns.factorplot(x=params["x"], y=params["y"], data=df, 
                    hue=params["hue"], kind=namaPlot.lower(),
                    jitter=True, dodge=True,
                    palette=params["palette"]).axes.flat[0].set_title(params["title"]);
    elif(namaPlot == 'Swarm') :
        sns.factorplot(x=params["x"], y=params["y"], data=df, 
                    hue=params["hue"], kind=namaPlot.lower(),
                    dodge=True,
                    palette=params["palette"]).axes.flat[0].set_title(params["title"]);
    plt.show();

while(True) :
    params = { "x": '', "y": '', "hue": '', "title": '', "palette": ''}
    inputMain = MainMenu();
    if(inputMain == '1') :
        namaDataSet = PilihDataSet();
        df = sns.load_dataset(namaDataSet);
        print(namaDataSet.upper() + ' DataSet : \n');
        print(df.head());
        
        idCategory = PilihCategory();
        PlotPilihan = PilihPlot(idCategory);
        print(list(df.columns));
        for item in PlotPilihan.index[2:] :
            if(PlotPilihan[item] == 1) :
                params[item.lower()] = input(item + ' : ');
        PrintPlot(PlotPilihan['Nama'], params, df);

    elif(inputMain == '2') :
        break;

