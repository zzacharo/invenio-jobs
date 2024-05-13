# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Services."""

from .config import JobsServiceConfig
from .schema import JobSchema
from .services import JobsService

__all__ = (
    "JobSchema",
    "JobsService",
    "JobsServiceConfig",
)