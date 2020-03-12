def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_forms(cldf_dataset):
    assert len(list(cldf_dataset["FormTable"])) == 711
    assert any(f["Form"] == "katare:i-ri" for f in cldf_dataset["FormTable"])


def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 102


def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 8


def test_cognates(cldf_dataset):
    assert len(list(cldf_dataset["CognateTable"])) == 711
    assert any(f["Form"] == "phálhai" for f in cldf_dataset["FormTable"])
