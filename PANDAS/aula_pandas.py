#%%

import pandas as pd
import numpy as np


df_vendas_tech = pd.read_csv("vendas_tech.csv")
df_gerentes_xl = pd.read_excel("gerentes_lojas.xlsx")
#inicializando uma copia do df 
df_vendas_copy = df_vendas_tech.copy()
print(df_vendas_copy.info())
print(df_vendas_copy.columns)

#apagando coluna e tratando NaN
df_vendas_copy = df_vendas_copy.drop(columns=["Data_Base"])

#arrumando tipos
df_vendas_copy["Data"] = pd.to_datetime(df_vendas_copy["Data"],format="%Y-%m-%d")

#tratando NaM

df_vendas_copy = df_vendas_copy.fillna("Online")

#padronizando texto
df_vendas_copy["Loja"] = df_vendas_copy["Loja"].str.title().str.strip()

#removendo duplicatas
df_vendas_copy = df_vendas_copy.drop_duplicates(subset=["ID_Pedido"])

#criando colunas

df_vendas_copy["Faturamento"] = df_vendas_copy["Qtd"] * df_vendas_copy["Preco_Unitario"]
df_vendas_copy["Forma_Venda"] = np.where(df_vendas_copy["Loja"] == "Online","Venda Online","Venda Presencial")
mapa_regioes = {
    "São Paulo": "SUDESTE",
    "Belo Horizonte": "SUDESTE",
    "Online": "ONLINE",
    "Rio De Janeiro": "SUDESTE",
    "Salvador": "NORDESTE",
    "Recife": "NORDESTE",
    "Curitiba": "SUL",
    "Porto Alegre": "SUL",
}
df_vendas_copy["Regiao"] = df_vendas_copy["Loja"].map(mapa_regioes)
print(df_vendas_copy.isna().sum())

df_vendas_copy = df_vendas_copy.sort_values(by=["Data","Faturamento"])
#reorganizando indice
df_vendas_copy = df_vendas_copy.reset_index(drop=True)

#Filtrando dados

df_vendas_sp = df_vendas_copy.loc[df_vendas_copy["Loja"] == "São Paulo"]
# ou df_vendas_sp = df_vendas_copy[df_vendas_copy["Loja"] == "São Paulo"]

#filtrando clientes que compraram cabohdmi:
#filtrando com 2 +  condicoes

c1 = df_vendas_copy["Regiao"] == "SUL"
c2 = df_vendas_copy["Produto"] == "Cabo HDMI"

df_vendas_hdmi_sul = df_vendas_copy[c1 & c2 ]

#filtrando com 2+ condicoes mesma linha:

df_vendas_hdmi_sul = df_vendas_copy[(df_vendas_copy["Regiao"]=="SUL") & (df_vendas_copy["Produto"] == "Cabo HDMI")]

#CLIENTES QUE COMPROU CABO HDMI EM SP
df_vendas_sp_cabohdmi_clientes = len(df_vendas_sp.loc[df_vendas_sp["Produto"] == "Cabo HDMI","Cliente"].values) # .values retorna um objeto numpy semelhante a  lista ou seja pode ser percorrida com for e pode ser util, para realmente receber lista python use .tolist()

print(f"Quantidade de clientes que compraram cabo hdmi em São Paulo: {df_vendas_sp_cabohdmi_clientes}")

print(f"Quantidade de clientes que comprou algo em sp: {df_vendas_sp["Cliente"].nunique()}") #nunique > retorna qtd de valores unicos q aparece ou seja conta os ids unicos,unique retorna uma lista numpy com os valores unicos encontrados

#exportando vendas do ano 2024

df_vendas_2024 = df_vendas_copy[df_vendas_copy["Data"].dt.year == 2024 ]

#usando groupby para rankear faturamento de cada loja

df_venda_loja = df_vendas_copy.groupby("Loja",as_index=False)["Faturamento"].sum()
df_venda_loja = df_venda_loja.sort_values("Faturamento",ascending=False)
df_venda_loja = df_venda_loja.reset_index(drop=True)
df_venda_loja["Faturamento"] = df_venda_loja["Faturamento"].map(lambda x: f"R${x:,.2f}")

#ranking de  produto que mais vendeu online

df_produto_online = df_vendas_copy[df_vendas_copy["Regiao"] == "ONLINE"]
df__produto_online_maisvendido = df_produto_online.groupby("Produto",as_index=False)[["Qtd","Faturamento"]].sum()
df__produto_online_maisvendido = df__produto_online_maisvendido.sort_values(by = "Qtd",ascending=False).reset_index(drop = True)

df__produto_online_maisvendido = df__produto_online_maisvendido.rename(columns={"Qtd":"Quantidade Produtos ONLINE"}) #ALTERAR nome colunas

#ranking produto mais vendido em cada loja/cidade

df_loja_produto_qtd = df_vendas_copy.groupby(["Loja","Produto"],as_index=False)["Qtd"].sum()
df_loja_produto_qtd = df_loja_produto_qtd.sort_values(by=["Loja","Qtd"],ascending=[True,False]).reset_index(drop =True)

#gerentes que batera a meta em certo mes

df_meta_jun_2024 = df_vendas_copy[(df_vendas_copy['Data'].dt.year  == 2024) & (df_vendas_copy["Data"].dt.month == 6)]

df_metajun2024_loja_agrupada = df_meta_jun_2024.groupby("Loja",as_index=False)["Faturamento"].sum()

df_gerentes_xl["Loja"] = df_gerentes_xl["Loja"].str.title().str.strip()

df_metajun2024_loja_agrupada = df_metajun2024_loja_agrupada.merge(df_gerentes_xl,on = "Loja",how = "left")

df_metajun2024_loja_agrupada["BATEU META"] = np.where(df_metajun2024_loja_agrupada["Faturamento"] >= df_metajun2024_loja_agrupada["Meta_Mensal"],"SIM","NAO")

df_vendas_copy["MES-ANO"] = df_vendas_copy["Data"].to_period("M")
df_mes = df_vendas_copy.groupby("MES-ANO")["Faturamento"].sum()

# %%
