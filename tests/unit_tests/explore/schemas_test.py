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

from superset.explore.form_data.schemas import FormDataPostSchema, FormDataPutSchema
from superset.explore.permalink.schemas import (
    ExplorePermalinkSchema,
    ExplorePermalinkStateSchema,
)


def test_form_data_post_schema_valid() -> None:
    schema = FormDataPostSchema()
    result = schema.load(
        {
            "datasource_id": 1,
            "datasource_type": "table",
            "form_data": '{"viz_type": "table"}',
        }
    )
    assert result["datasource_id"] == 1
    assert result["datasource_type"] == "table"
    assert result["form_data"] == '{"viz_type": "table"}'


def test_form_data_post_schema_with_chart_id() -> None:
    schema = FormDataPostSchema()
    result = schema.load(
        {
            "datasource_id": 1,
            "datasource_type": "table",
            "form_data": "{}",
            "chart_id": 42,
        }
    )
    assert result["chart_id"] == 42


def test_form_data_post_schema_rejects_missing_required() -> None:
    schema = FormDataPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({})
    errors = exc_info.value.messages
    assert "datasource_id" in errors
    assert "datasource_type" in errors
    assert "form_data" in errors


def test_form_data_post_schema_rejects_invalid_datasource_type() -> None:
    schema = FormDataPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "datasource_id": 1,
                "datasource_type": "invalid",
                "form_data": "{}",
            }
        )
    assert "datasource_type" in exc_info.value.messages


def test_form_data_put_schema_valid() -> None:
    schema = FormDataPutSchema()
    result = schema.load(
        {
            "datasource_id": 2,
            "datasource_type": "query",
            "form_data": '{"viz_type": "bar"}',
        }
    )
    assert result["datasource_type"] == "query"


def test_permalink_state_schema_valid() -> None:
    schema = ExplorePermalinkStateSchema()
    result = schema.load({"formData": {"viz_type": "table", "datasource": "1__table"}})
    assert result["formData"]["viz_type"] == "table"


def test_permalink_state_schema_rejects_missing_form_data() -> None:
    schema = ExplorePermalinkStateSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({})
    assert "formData" in exc_info.value.messages


def test_permalink_state_schema_with_url_params() -> None:
    schema = ExplorePermalinkStateSchema()
    result = schema.load(
        {
            "formData": {"viz_type": "table"},
            "urlParams": [("key1", "val1"), ("key2", "val2")],
        }
    )
    assert len(result["urlParams"]) == 2


def test_permalink_schema_valid() -> None:
    schema = ExplorePermalinkSchema()
    result = schema.load(
        {
            "datasourceType": "table",
            "datasourceId": 1,
            "chartId": 5,
            "state": {"formData": {"viz_type": "bar"}},
        }
    )
    assert result["datasourceType"] == "table"
    assert result["chartId"] == 5


def test_permalink_schema_rejects_missing_datasource_type() -> None:
    schema = ExplorePermalinkSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"datasourceId": 1})
    assert "datasourceType" in exc_info.value.messages


def test_permalink_schema_allows_null_chart_id() -> None:
    schema = ExplorePermalinkSchema()
    result = schema.load(
        {
            "datasourceType": "table",
            "chartId": None,
        }
    )
    assert result["chartId"] is None
