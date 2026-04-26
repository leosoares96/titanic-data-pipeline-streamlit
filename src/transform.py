def transform(df):
    # remover colunas inúteis
    df = df.drop(columns=["Name", "Ticket", "Cabin"])
    
    # tratar nulos
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna("Unknown")
    
    # feature engineering
    df["is_child"] = df["Age"] < 12
    
    # padronização
    df.columns = [c.lower() for c in df.columns]
    
    return df