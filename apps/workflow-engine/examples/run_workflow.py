"""Example launcher for Flowable Workflow Engine Service."""

from tmmp_workflow_engine.config import WorkflowEngineConfig
from tmmp_workflow_engine.main import create_app


def main() -> None:
    config = WorkflowEngineConfig(port=8004)
    app = create_app(config)
    print("Successfully initialized Workflow Engine Service:", app.title)


if __name__ == "__main__":
    main()
