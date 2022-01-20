from th2_data_services.data_source import DataSource
from th2_data_services.filter import Filter


def test_get_url():
    assert (
        DataSource._get_url(
            {
                "filters": [
                    Filter("type", "recon"),
                    Filter("status", "Failed", negative=True),
                ]
            }
        )
        == "filters=type&type-values=recon&type-negative=False&filters=status&status-values=Failed&status-negative=True"
    )
    assert (
        DataSource._get_url({"filters": Filter("type", "recon")})
        == "filters=type&type-values=recon&type-negative=False"
    )
