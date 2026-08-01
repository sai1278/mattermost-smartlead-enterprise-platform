from tmmp_integrations_flowable import FlowableConfig, ProcessInstanceDTO, TaskDTO


def test_flowable_config():
    cfg = FlowableConfig()
    assert isinstance(cfg.url, str)
    assert isinstance(cfg.user, str)
    assert isinstance(cfg.password.get_secret_value(), str)


def test_flowable_dtos():
    inst = ProcessInstanceDTO(
        id="inst-1", process_definition_id="def-1", ended=False, suspended=False
    )
    assert inst.id == "inst-1"
    assert inst.ended is False

    task = TaskDTO(
        id="t-1",
        name="Approve Warmup",
        assignee="mgr",
        process_instance_id="inst-1",
        create_time="2026-08-01",
    )
    assert task.name == "Approve Warmup"
