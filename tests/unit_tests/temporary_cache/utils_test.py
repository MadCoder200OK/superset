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

from superset.temporary_cache.utils import cache_key, SEPARATOR


def test_cache_key_single_arg() -> None:
    assert cache_key("foo") == "foo"


def test_cache_key_multiple_args() -> None:
    assert cache_key("a", "b", "c") == f"a{SEPARATOR}b{SEPARATOR}c"


def test_cache_key_numeric_args() -> None:
    assert cache_key(1, 2, 3) == f"1{SEPARATOR}2{SEPARATOR}3"


def test_cache_key_mixed_types() -> None:
    result = cache_key("prefix", 42, None)
    assert result == f"prefix{SEPARATOR}42{SEPARATOR}None"


def test_cache_key_empty_strings() -> None:
    result = cache_key("", "")
    assert result == f"{SEPARATOR}"


def test_separator_is_semicolon() -> None:
    assert SEPARATOR == ";"
