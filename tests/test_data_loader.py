from src.data_loader import load_data


def test_load_data():
    df = load_data("data/xy_data.csv")

    assert list(df.columns) == ["x", "y"]
    assert len(df) == 1500
    assert df.isnull().sum().sum() == 0
    assert df.duplicated().sum() == 0