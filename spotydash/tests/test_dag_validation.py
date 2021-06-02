from airflow.models import DagBag

from spotydash.constants import DAGS_DIR


class TestDagValidation:

    LOAD_SECOND_THRESHOLD = 2
    EXPECTED_NUMBER_OF_DAGS = 4
    DAG_BAG_TEST = DagBag(dag_folder=DAGS_DIR)

    def test_import_dags(self):
        """
        Verify that Airflow is able to import all DAGs
        in the repo
        - check for typos
        - check for cycles
        """
        assert (
            len(self.DAG_BAG_TEST.import_errors) == 0
        ), "DAG failures detected! Got: {}".format(self.DAG_BAG_TEST.import_errors)

    def test_time_import_dags(self):
        """
        Verify that DAGs load fast enough
        - check for loading time
        """
        stats = self.DAG_BAG_TEST.dagbag_stats
        slow_dags = list(
            filter(lambda f: f.duration.seconds > self.LOAD_SECOND_THRESHOLD, stats)
        )
        res = ", ".join(map(lambda f: f.file[1:], slow_dags))

        assert (
            len(slow_dags) == 0
        ), "The following DAGs take more than {0}s to load: {1}".format(
            self.LOAD_SECOND_THRESHOLD, res
        )

    def test_default_args_retries(self):
        """
        Verify that DAGs have the required number of retries
        - Check retries
        """
        for dag_id, dag in self.DAG_BAG_TEST.dags.items():
            retries = dag.default_args.get("retries", None)
            assert (
                retries is not None
            ), "You must specify a number of retries in the DAG: {0}".format(dag_id)

    def test_default_args_retry_delay(self):
        """
        Verify that DAGs have the required retry_delay expressed in seconds
        - Check retry_delay
        """
        for dag_id, dag in self.DAG_BAG_TEST.dags.items():
            retry_delay = dag.default_args.get("retry_delay", None)
            assert (
                retry_delay is not None
            ), "You must specify a retry delay (seconds) in the DAG: {0}".format(dag_id)

    def test_number_of_dags(self):
        """
        Verify if there is the right number of DAGs in the dag folder
        - Check number of dags
        """
        stats = self.DAG_BAG_TEST.dagbag_stats
        dag_num = sum([o.dag_num for o in stats])
        assert (
            dag_num == self.EXPECTED_NUMBER_OF_DAGS
        ), "Wrong number of dags, {0} expected got {1} (Can be due to cycles!)".format(
            self.EXPECTED_NUMBER_OF_DAGS, dag_num
        )
