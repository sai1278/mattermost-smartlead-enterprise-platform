"""Flowable REST Async Client."""

from __future__ import annotations

from typing import Any

import httpx
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_shared.logging import get_logger

from tmmp_integrations_flowable.config import FlowableConfig
from tmmp_integrations_flowable.dto import ProcessInstanceDTO, TaskDTO

LOGGER = get_logger(__name__)


class FlowableClient:
    """Async client interacting with Flowable REST API."""

    def __init__(self, config: FlowableConfig | None = None) -> None:
        self._config = config or FlowableConfig()
        self._http = httpx.AsyncClient(
            base_url=self._config.url,
            auth=(self._config.user, self._config.password.get_secret_value()),
            timeout=self._config.timeout_seconds,
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def start_process_instance(
        self, process_definition_key: str, variables: dict[str, Any] | None = None
    ) -> Result[ProcessInstanceDTO, IntegrationError]:
        payload = {
            "processDefinitionKey": process_definition_key,
            "variables": [{"name": k, "value": v} for k, v in (variables or {}).items()],
        }
        try:
            res = await self._http.post("/service/runtime/process-instances", json=payload)
            if res.status_code not in (200, 201):
                msg = f"Flowable start instance failed ({res.status_code}): {res.text}"
                return Result.fail(IntegrationError(message=msg))
            data = res.json()
            inst = ProcessInstanceDTO(
                id=str(data.get("id", "")),
                process_definition_id=str(data.get("processDefinitionId", "")),
                ended=bool(data.get("ended", False)),
                suspended=bool(data.get("suspended", False)),
            )
            return Result.ok(inst)
        except Exception as exc:
            LOGGER.error("Flowable start process instance exception: %s", exc)
            return Result.fail(IntegrationError(message=str(exc)))

    async def complete_task(
        self,
        task_id: str,
        action: str = "complete",
        variables: dict[str, Any] | None = None,
    ) -> Result[bool, IntegrationError]:
        payload = {
            "action": action,
            "variables": [{"name": k, "value": v} for k, v in (variables or {}).items()],
        }
        try:
            res = await self._http.post(f"/service/runtime/tasks/{task_id}", json=payload)
            if res.status_code not in (200, 204):
                msg = f"Flowable complete task failed ({res.status_code}): {res.text}"
                return Result.fail(IntegrationError(message=msg))
            return Result.ok(True)
        except Exception as exc:
            LOGGER.error("Flowable complete task exception: %s", exc)
            return Result.fail(IntegrationError(message=str(exc)))

    async def list_active_tasks(
        self, process_instance_id: str
    ) -> Result[list[TaskDTO], IntegrationError]:
        try:
            res = await self._http.get(
                "/service/runtime/tasks",
                params={"processInstanceId": process_instance_id},
            )
            if res.status_code != 200:
                msg = f"Flowable list tasks failed ({res.status_code}): {res.text}"
                return Result.fail(IntegrationError(message=msg))
            data = res.json()
            tasks = [
                TaskDTO(
                    id=str(item.get("id", "")),
                    name=str(item.get("name", "")),
                    assignee=item.get("assignee"),
                    process_instance_id=str(item.get("processInstanceId", "")),
                    create_time=str(item.get("createTime", "")),
                )
                for item in data.get("data", [])
            ]
            return Result.ok(tasks)
        except Exception as exc:
            LOGGER.error("Flowable list active tasks exception: %s", exc)
            return Result.fail(IntegrationError(message=str(exc)))
