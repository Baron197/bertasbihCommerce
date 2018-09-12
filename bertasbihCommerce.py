import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
      "mysql+mysqlconnector://root:abc123@localhost/toko?host=localhost?port=3306")

conn = engine.connect();

def MainMenu() : 
    inputUser = input('Bertasbih Commerce \n\n 1. Lihat Categories \n 2. Input Product Baru \n 3. Edit Product Tertentu \n 4. Hapus Product Tertentu \n 5. Keluar \n\n Pilih Menu : ');
    return inputUser;

programJalan = True;

while(programJalan) :
    inputUser = MainMenu();
    if(inputUser == '1') :
        results = conn.execute("SELECT id,Nama from category where ParentId is Null").fetchall();
        df1 = pd.DataFrame(results);
        df1.columns = results[0].keys();
        df1 = df1.set_index('id');
        print('List Categories : ');
        print(df1);
        inputCat = '0'
        while(True) :
            inputCat = input('Masukkan id Cat Pilihan : ');
            result1 = conn.execute("SELECT id,Nama from category where ParentId = " + inputCat).fetchall();
            df2 = pd.DataFrame(result1);
            if(len(df2) == 0) :
                break;
            df2.columns = result1[0].keys();
            df2 = df2.set_index('id');
            print(df2);

        result2 = conn.execute("SELECT p.id as ProductId,p.Nama as NamaProduct, c.Nama as NamaCategory from product p join category c on p.CategoryId = c.id where CategoryId = " + inputCat).fetchall();
        df3 = pd.DataFrame(result2);
        df3.columns = result2[0].keys();
        df3 = df3.set_index('ProductId');
        print('List Products : ');
        print(df3);
    elif(inputUser == '2') :
        inputNama = input('Nama Product : ');
        inputCatId = input('Category Id : ');
        conn.execute("Insert into product values(Null, '" + inputNama + "', " + inputCatId + ")");
    elif(inputUser == '3') :
        result3 = conn.execute("SELECT p.id as ProductId,p.Nama as NamaProduct, c.Nama as NamaCategory from product p join category c on p.CategoryId = c.id").fetchall();
        df4 = pd.DataFrame(result3);
        df4.columns = result3[0].keys();
        df4 = df4.set_index('ProductId');
        print('List Products : ');
        print(df4);
        inputIdProd = input("\nMasukkan Id Product Yang ingin di edit : ");
        inputNamaBaruProd = input("Nama Baru : ");
        inputCatIdBaruProd = input("Category Id Baru : ");
        conn.execute("Update product set Nama = '" + inputNamaBaruProd + "', CategoryId = " + inputCatIdBaruProd + " where id = " + inputIdProd);
    elif(inputUser == '4') :
        result4 = conn.execute("SELECT p.id as ProductId,p.Nama as NamaProduct, c.Nama as NamaCategory from product p join category c on p.CategoryId = c.id").fetchall();
        df5 = pd.DataFrame(result4);
        df5.columns = result4[0].keys();
        df5 = df5.set_index('ProductId');
        print('List Products : ');
        print(df5);
        inputIdProd = input("\nMasukkan Id Product Yang ingin di delete : ");
        conn.execute("Delete from product where id = " + inputIdProd);
    elif(inputUser == '5') :
        programJalan = False;
