# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

import pytest

from superset.async_events.async_query_manager import (
    build_job_metadata,
    get_cache_backend,
    increment_id,
    parse_event,
    UnsupportedCacheBackendError,
)


def test_build_job_metadata_minimal() -> None:
    result = build_job_metadata(
        channel_id="ch-1",
        job_id="job-1",
        user_id=42,
    )
    assert result == {
        "channel_id": "ch-1",
        "job_id": "job-1",
        "user_id": 42,
        "status": None,
        "errors": [],
        "result_url": None,
    }


def test_build_job_metadata_with_kwargs() -> None:
    result = build_job_metadata(
        channel_id="ch-2",
        job_id="job-2",
        user_id=None,
        status="running",
        errors=[{"msg": "oops"}],
        result_url="/api/v1/chart/data/123",
    )
    assert result["status"] == "running"
    assert result["errors"] == [{"msg": "oops"}]
    assert result["result_url"] == "/api/v1/chart/data/123"
    assert result["user_id"] is None


def test_parse_event() -> None:
    event_data = (
        "1607477697866-0",
        {"data": '{"channel_id": "ch-1", "status": "done"}'},
    )
    result = parse_event(event_data)
    assert result["id"] == "1607477697866-0"
    assert result["channel_id"] == "ch-1"
    assert result["status"] == "done"


def test_increment_id_normal() -> None:
    assert increment_id("1607477697866-0") == "1607477697866-1"


def test_increment_id_rollover() -> None:
    assert increment_id("1607477697866-9") == "1607477697866-10"


def test_increment_id_invalid_returns_original() -> None:
    assert increment_id("invalid") == "invalid"


def test_get_cache_backend_unsupported_raises() -> None:
    with pytest.raises(UnsupportedCacheBackendError):
        get_cache_backend(
            {"GLOBAL_ASYNC_QUERIES_CACHE_BACKEND": {"CACHE_TYPE": "MemcachedCache"}}
        )


def test_get_cache_backend_missing_config_raises() -> None:
    with pytest.raises(UnsupportedCacheBackendError):
        get_cache_backend({})
