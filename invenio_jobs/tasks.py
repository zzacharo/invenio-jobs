# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tasks."""
from datetime import datetime, timezone

from celery import current_app, shared_task
from invenio_db import db

from invenio_jobs.models import Run, RunStatusEnum


# TODO 1. Move to service? 2. Don't use kwargs?
def update_run(run, **kwargs):
    if not run:
        return
    for kw, value in kwargs.items():
        setattr(run, kw, value)
    db.session.commit()


@shared_task(bind=True, ignore_result=True)
def execute_run(self, run_id, kwargs=None):
    """Run a job."""

    # TODO Catch jobsystem error
    run = Run.query.filter_by(id=run_id).one_or_none()
    task = self.app.tasks.get(run.job.task)
    update_run(run, status=RunStatusEnum.RUNNING, started_at=datetime.now(timezone.utc))
    try:
        message = task.apply(kwargs=kwargs)
    except Exception as e:
        # TODO should we log the error in message?
        update_run(
            run,
            status=RunStatusEnum.FAILURE,
            finished_at=datetime.now(timezone.utc),
        )
        return
    except SystemExit:
        update_run(
            run,
            status=RunStatusEnum.TERMINATED,
            finished_at=datetime.now(timezone.utc),
        )
        return
    # TODO Don't update message like this, use celery app task state
    update_run(
        run,
        status=RunStatusEnum.SUCCESS,
        finished_at=datetime.now(timezone.utc),
    )
