from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from app.core.cache.invalidation import NAMESPACE_ACCOUNT_SELECTION, NAMESPACE_HTTP_BRIDGE_SESSIONS
from app.modules.accounts.service import AccountsService


pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_reactivate_account_invalidates_and_bumps_account_selection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = SimpleNamespace(update_status=AsyncMock(return_value=True))
    service = AccountsService(repo)
    cache = SimpleNamespace(invalidate=Mock())
    poller = SimpleNamespace(bump=AsyncMock())

    monkeypatch.setattr("app.modules.accounts.service.get_account_selection_cache", lambda: cache)
    monkeypatch.setattr("app.modules.accounts.service.get_cache_invalidation_poller", lambda: poller)

    result = await service.reactivate_account("acc-1")

    assert result is True
    cache.invalidate.assert_called_once_with()
    poller.bump.assert_awaited_once_with(NAMESPACE_ACCOUNT_SELECTION)


@pytest.mark.asyncio
async def test_pause_account_bumps_bridge_namespace_and_invalidates_target_sessions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = SimpleNamespace(update_status=AsyncMock(return_value=True))
    service = AccountsService(repo)
    cache = SimpleNamespace(invalidate=Mock())
    poller = SimpleNamespace(bump=AsyncMock())
    invalidate_bridge_sessions_for_account = AsyncMock()

    monkeypatch.setattr("app.modules.accounts.service.get_account_selection_cache", lambda: cache)
    monkeypatch.setattr("app.modules.accounts.service.get_cache_invalidation_poller", lambda: poller)
    monkeypatch.setattr(
        "app.modules.proxy.account_cache.invalidate_bridge_sessions_for_account",
        invalidate_bridge_sessions_for_account,
    )

    result = await service.pause_account("acc-1")

    assert result is True
    cache.invalidate.assert_called_once_with()
    assert poller.bump.await_args_list[0].args == (NAMESPACE_ACCOUNT_SELECTION,)
    assert poller.bump.await_args_list[1].args == (NAMESPACE_HTTP_BRIDGE_SESSIONS,)
    invalidate_bridge_sessions_for_account.assert_awaited_once_with("acc-1")
