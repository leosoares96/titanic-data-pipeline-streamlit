def run_quality_checks(df, logger):
    logger.info("Running data quality checks")

    # regra 1: dataset não vazio
    assert df.shape[0] > 0, "Dataset is empty"

    # regra 2: colunas obrigatórias
    required_columns = ["Age", "Sex", "Survived"]
    for col in required_columns:
        assert col in df.columns, f"Missing column: {col}"

    # regra 3: % de nulos em Age
    null_pct = df["Age"].isna().mean()
    assert null_pct < 0.5, "Too many nulls in Age"

    logger.info("Data quality checks passed")