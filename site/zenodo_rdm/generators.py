# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Zenodo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Zenodo legacy permissions generators."""

from invenio_access import action_factory
from invenio_access.permissions import Permission
from invenio_rdm_records.services.generators import IfRestricted
from invenio_records.dictutils import dict_lookup
from invenio_records_permissions.generators import Generator

# these are defined here as there is a circular dependency otherwise with the
# permissions.py file
media_files_management_action = action_factory("manage-media-files")
media_files_permission = Permission(media_files_management_action)


class IfFilesRestrictedForCommunity(IfRestricted):
    """Conditional generator for files restriction for community."""

    def __init__(self, then_, else_):
        """Constructor."""
        super().__init__("files", then_, else_)

    def _condition(self, record, **kwargs):
        """Check if community can access restricted files of the migrated record."""
        try:
            can_community_read_files = dict_lookup(
                record.parent, "permission_flags.can_community_read_files"
            )
        except KeyError:
            can_community_read_files = True

        is_restricted = super()._condition(record, **kwargs)
        if is_restricted:
            return not can_community_read_files
        else:
            return False


class MediaFilesManager(Generator):
    """Allows media files management."""

    def __init__(self):
        """Constructor."""
        super(MediaFilesManager, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [media_files_management_action]
