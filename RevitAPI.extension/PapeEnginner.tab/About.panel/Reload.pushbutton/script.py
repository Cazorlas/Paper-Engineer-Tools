"""Reload pyRevit into new session."""
# -*- coding=utf-8 -*-
# pylint: disable=import-error,invalid-name,broad-except
from pyrevit import EXEC_PARAMS
from pyrevit import script
from pyrevit import forms
from pyrevit.loader import sessionmgr
from pyrevit.loader import sessioninfo

res = True
if EXEC_PARAMS.executed_from_ui:
    res = forms.alert('Cái nút này dùng để Reload lại toàn bộ Pyrevit.\nBấm Ok để nó Reload, ko thích thì bấm Hủy',
                      ok=False, yes=True, no=True)

if res:
    logger = script.get_logger()
    results = script.get_results()

    # re-load pyrevit session.
    logger.info('Reloading....')
    sessionmgr.reload_pyrevit()

    results.newsession = sessioninfo.get_session_uuid()
