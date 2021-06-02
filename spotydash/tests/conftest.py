import pytest
from airflow.models import DagBag

from spotydash.constants import DAGS_DIR


@pytest.fixture(scope="session")
def dagbag():
    return DagBag(dag_folder=DAGS_DIR)
