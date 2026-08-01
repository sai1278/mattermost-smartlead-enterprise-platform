from scripts.e2e_verification import verify_e2e_flow


def test_e2e_workflow_demonstration():
    assert verify_e2e_flow() is True
