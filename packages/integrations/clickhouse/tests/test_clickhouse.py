from tmmp_integrations_clickhouse import ClickHouseConfig, ClickHouseQueryResult


def test_clickhouse_config():
    cfg = ClickHouseConfig()
    assert isinstance(cfg.url, str)
    assert isinstance(cfg.user, str)
    assert isinstance(cfg.password.get_secret_value(), str)


def test_clickhouse_query_result():
    res = ClickHouseQueryResult(columns=["id", "sent"], rows=[[1, 100], [2, 200]])
    assert len(res.columns) == 2
    assert len(res.rows) == 2
