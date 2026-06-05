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

# Flask 3.x removed _app_ctx_stack (replaced by contextvars internally).
# Flask-SQLAlchemy 2.5.x still imports it for session scoping.  Re-add
# a lightweight adapter that bridges to Flask 3.x's ContextVar so the
# existing session machinery keeps working without upgrading to
# Flask-SQLAlchemy 3.0 (which has breaking session-management changes).
import flask as _flask  # isort: skip  # noqa: E402

if not hasattr(_flask, "_app_ctx_stack"):  # Flask >= 3.0
    import threading as _threading
    from typing import Any as _Any, Callable as _Callable, Optional as _Optional

    from flask.globals import _cv_app as _cv_app

    class _AppCtxStackCompat:
        """Minimal shim for the removed ``flask._app_ctx_stack``."""

        @property
        def __ident_func__(self) -> _Callable[[], int]:
            return _threading.get_ident

        @property
        def top(self) -> _Optional[_Any]:
            return _cv_app.get(None)

    _flask._app_ctx_stack = _AppCtxStackCompat()  # noqa: E501
    _flask.globals._app_ctx_stack = _flask._app_ctx_stack  # noqa: E501

from werkzeug.local import LocalProxy

from superset.app import create_app  # noqa: F401
from superset.extensions import (
    appbuilder,  # noqa: F401
    cache_manager,
    db,  # noqa: F401
    event_logger,  # noqa: F401
    feature_flag_manager,
    manifest_processor,
    results_backend_manager,
    security_manager,  # noqa: F401
    talisman,  # noqa: F401
)
from superset.security import SupersetSecurityManager  # noqa: F401

# All of the fields located here should be considered legacy. The correct way to
# declare "global" dependencies is to define it in extensions.py,
# then initialize it in app.create_app(). These fields will be removed
# in subsequent PRs as things are migrated towards the factory pattern
cache = cache_manager.cache
get_feature_flags = feature_flag_manager.get_feature_flags
get_manifest_files = manifest_processor.get_manifest_files
is_feature_enabled = feature_flag_manager.is_feature_enabled
results_backend = LocalProxy(lambda: results_backend_manager.results_backend)
results_backend_use_msgpack = LocalProxy(
    lambda: results_backend_manager.should_use_msgpack
)
data_cache = LocalProxy(lambda: cache_manager.data_cache)
thumbnail_cache = LocalProxy(lambda: cache_manager.thumbnail_cache)
