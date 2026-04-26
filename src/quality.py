import pandas as pd

def run_quality_checks(df, logger):
    logger.info("Running data quality checks")

    # =========================
    # 1. Dataset não vazio
    # =========================
    if df.shape[0] == 0:
        raise ValueError("Dataset is empty")

    logger.info(f"Dataset rows: {df.shape[0]}")

    # =========================
    # 2. Colunas obrigatórias
    # =========================
    required_columns = ["PassengerId", "Survived", "Pclass", "Sex", "Age", "Fare"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # =========================
    # 3. Tipagem segura
    # =========================
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")

    # =========================
    # 4. % de nulos
    # =========================
    null_pct_age = df["Age"].isna().mean()
    logger.info(f"Age null %: {null_pct_age:.2f}")

    if null_pct_age > 0.5:
        raise ValueError("Too many nulls in Age")

    # =========================
    # 5. Faixas plausíveis
    # =========================
    if df["Age"].dropna().lt(0).any() or df["Age"].dropna().gt(120).any():
        raise ValueError("Invalid values in Age (outside 0-120)")

    if df["Fare"].dropna().lt(0).any():
        raise ValueError("Invalid values in Fare (negative values)")

    # =========================
    # 6. Unicidade da chave
    # =========================
    if df["PassengerId"].duplicated().any():
        raise ValueError("Duplicate PassengerId detected")

    # =========================
    # 7. Valores válidos
    # =========================
    if not df["Survived"].isin([0, 1]).all():
        raise ValueError("Invalid values in Survived (must be 0 or 1)")

    # =========================
    # 8. Pós-validação básica
    # =========================
    if df["Fare"].isna().all():
        raise ValueError("Fare column became fully null after coercion")

    logger.info("Data quality checks passed successfully")