import pytest
from dbt.artifacts.schemas.catalog import CatalogArtifact
from dbt.tests.adapter.catalog import files
from dbt.tests.adapter.catalog.relation_types import CatalogRelationTypes
from dbt.tests.util import run_dbt


class TestRelationTypes(CatalogRelationTypes):
    """
    This is subclassed to remove the references to the materialized views,
    as SQLServer does not support them.

    Likely does not need to be subclassed since we implement everything,
    but prefer keeping it here for clarity.
    """

    @pytest.fixture(scope="class", autouse=True)
    def seeds(self):
        return {"my_seed.csv": files.MY_SEED}

    @pytest.fixture(scope="class", autouse=True)
    def models(self):
        yield {
            "my_table.sql": files.MY_TABLE,
            "my_view.sql": files.MY_VIEW,
            # "my_materialized_view.sql": files.MY_MATERIALIZED_VIEW,
        }

    @pytest.fixture(scope="class", autouse=True)
    def docs(self, project):
        run_dbt(["seed"])
        run_dbt(["run"])
        yield run_dbt(["docs", "generate"])

    @pytest.mark.parametrize(
        "node_name,relation_type",
        [
            ("seed.test.my_seed", "BASE TABLE"),
            ("model.test.my_table", "BASE TABLE"),
            ("model.test.my_view", "VIEW"),
            # ("model.test.my_materialized_view", "MATERIALIZED VIEW"),
        ],
    )
    def test_relation_types_populate_correctly(
        self, docs: CatalogArtifact, node_name: str, relation_type: str
    ):
        """
        This test addresses: https://github.com/dbt-labs/dbt-core/issues/8864
        """
        assert node_name in docs.nodes
        node = docs.nodes[node_name]
        assert node.metadata.type == relation_type
