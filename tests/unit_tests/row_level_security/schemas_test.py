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
from marshmallow import ValidationError

from superset.row_level_security.schemas import (
    get_delete_ids_schema,
    openapi_spec_methods_override,
    RLSPostSchema,
    RLSPutSchema,
    RolesSchema,
    TablesSchema,
)


def test_roles_schema() -> None:
    schema = RolesSchema()
    result = schema.load({"name": "Admin", "id": 1})
    assert result["name"] == "Admin"
    assert result["id"] == 1


def test_tables_schema() -> None:
    schema = TablesSchema()
    result = schema.load({"schema": "public", "table_name": "users", "id": 5})
    assert result["table_name"] == "users"
    assert result["id"] == 5


def test_rls_post_schema_valid() -> None:
    schema = RLSPostSchema()
    result = schema.load(
        {
            "name": "dept_filter",
            "filter_type": "Regular",
            "tables": [1, 2],
            "roles": [1],
            "clause": "department_id = 1",
        }
    )
    assert result["name"] == "dept_filter"
    assert result["filter_type"] == "Regular"
    assert result["clause"] == "department_id = 1"


def test_rls_post_schema_rejects_missing_required_fields() -> None:
    schema = RLSPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({})
    errors = exc_info.value.messages
    assert "name" in errors
    assert "filter_type" in errors
    assert "tables" in errors
    assert "roles" in errors
    assert "clause" in errors


def test_rls_post_schema_rejects_empty_name() -> None:
    schema = RLSPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "name": "",
                "filter_type": "Regular",
                "tables": [1],
                "roles": [1],
                "clause": "1=1",
            }
        )
    assert "name" in exc_info.value.messages


def test_rls_post_schema_rejects_invalid_filter_type() -> None:
    schema = RLSPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "name": "test",
                "filter_type": "InvalidType",
                "tables": [1],
                "roles": [1],
                "clause": "1=1",
            }
        )
    assert "filter_type" in exc_info.value.messages


def test_rls_post_schema_rejects_empty_tables() -> None:
    schema = RLSPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "name": "test",
                "filter_type": "Regular",
                "tables": [],
                "roles": [1],
                "clause": "1=1",
            }
        )
    assert "tables" in exc_info.value.messages


def test_rls_post_schema_accepts_base_filter_type() -> None:
    schema = RLSPostSchema()
    result = schema.load(
        {
            "name": "base_filter",
            "filter_type": "Base",
            "tables": [1],
            "roles": [1],
            "clause": "1 = 0",
        }
    )
    assert result["filter_type"] == "Base"


def test_rls_put_schema_all_fields_optional() -> None:
    schema = RLSPutSchema()
    result = schema.load({})
    assert result == {}


def test_rls_put_schema_partial_update() -> None:
    schema = RLSPutSchema()
    result = schema.load({"clause": "region = 'EU'"})
    assert result["clause"] == "region = 'EU'"


def test_get_delete_ids_schema_structure() -> None:
    assert get_delete_ids_schema["type"] == "array"
    items = get_delete_ids_schema["items"]
    assert isinstance(items, dict)
    assert items["type"] == "integer"


def test_openapi_spec_methods() -> None:
    expected = {"get", "get_list", "delete", "info"}
    assert set(openapi_spec_methods_override.keys()) == expected
