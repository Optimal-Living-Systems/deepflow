"""Async-compatible SQLite checkpointer helpers for Deep Flo."""

from __future__ import annotations

import asyncio
from contextlib import contextmanager
from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.sqlite import SqliteSaver


class AsyncCompatibleSqliteSaver(BaseCheckpointSaver[Any]):
    """Wrap `SqliteSaver` with async methods backed by thread offload."""

    def __init__(self, saver: SqliteSaver) -> None:
        super().__init__(serde=saver.serde)
        self._saver = saver

    def __getattr__(self, name: str) -> Any:
        return getattr(self._saver, name)

    def get_tuple(self, config: Any) -> Any:
        return self._saver.get_tuple(config)

    def put(self, config: Any, checkpoint: Any, metadata: Any, new_versions: Any) -> Any:
        return self._saver.put(config, checkpoint, metadata, new_versions)

    def put_writes(self, config: Any, writes: Any, task_id: str, task_path: str = "") -> None:
        self._saver.put_writes(config, writes, task_id, task_path)

    def list(self, config: Any, *, filter: dict[str, Any] | None = None, before: Any = None, limit: int | None = None):
        return self._saver.list(config, filter=filter, before=before, limit=limit)

    def delete_thread(self, thread_id: str) -> None:
        self._saver.delete_thread(thread_id)

    def get(self, config: Any) -> Any:
        return self._saver.get(config)

    def copy_thread(self, source_thread_id: str, target_thread_id: str) -> None:
        self._saver.copy_thread(source_thread_id, target_thread_id)

    def delete_for_runs(self, run_ids: list[str]) -> None:
        self._saver.delete_for_runs(run_ids)

    def prune(self, thread_ids: list[str], *, strategy: str = "keep_latest") -> None:
        self._saver.prune(thread_ids, strategy=strategy)

    async def aget_tuple(self, config: Any) -> Any:
        return await asyncio.to_thread(self._saver.get_tuple, config)

    async def aput(self, config: Any, checkpoint: Any, metadata: Any, new_versions: Any) -> Any:
        return await asyncio.to_thread(self._saver.put, config, checkpoint, metadata, new_versions)

    async def aput_writes(self, config: Any, writes: Any, task_id: str, task_path: str = "") -> None:
        await asyncio.to_thread(self._saver.put_writes, config, writes, task_id, task_path)

    async def alist(self, config: Any, *, filter: dict[str, Any] | None = None, before: Any = None, limit: int | None = None):
        items = await asyncio.to_thread(lambda: list(self._saver.list(config, filter=filter, before=before, limit=limit)))
        for item in items:
            yield item

    async def adelete_thread(self, thread_id: str) -> None:
        await asyncio.to_thread(self._saver.delete_thread, thread_id)

    async def aget(self, config: Any) -> Any:
        return await asyncio.to_thread(self._saver.get, config)

    async def acopy_thread(self, source_thread_id: str, target_thread_id: str) -> None:
        await asyncio.to_thread(self._saver.copy_thread, source_thread_id, target_thread_id)

    async def adelete_for_runs(self, run_ids: list[str]) -> None:
        await asyncio.to_thread(self._saver.delete_for_runs, run_ids)

    async def aprune(self, thread_ids: list[str], *, strategy: str = "keep_latest") -> None:
        await asyncio.to_thread(lambda: self._saver.prune(thread_ids, strategy=strategy))


@contextmanager
def open_checkpointer(path: str):
    """Open a Deep Flo SQLite checkpointer with async compatibility."""
    with SqliteSaver.from_conn_string(path) as saver:
        yield AsyncCompatibleSqliteSaver(saver)
