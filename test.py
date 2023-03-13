import pandas as pd

pd.set_option('display.max_columns', 1000)  # or 1000
pd.set_option('display.max_rows', 1000)  # or 1000
pd.set_option('display.max_colwidth', 199)  # or 199
pd.set_option('display.width', 5000)

# pytest 
# run all: pytest
# run one file: pytest file.py
# run one method: pytest file.py::method
import pytest




# pytest.main(["-s"])
# pytest.main(["tests"])
# pytest.main(["-s", "tests/test_models.py"])
# pytest.main(["-s", "tests/test_models.py::test_get_csindex_industry_data"])
pytest.main(["-s", "tests/test_models.py::test_get_stock_data"])
# pytest.main(["-s", "tests/test_hello.py::test_helloworld"])