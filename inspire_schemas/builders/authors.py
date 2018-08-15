# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Author builder class and related code."""

from __future__ import absolute_import, division, print_function

from inspire_utils.date import normalize_date
from inspire_utils.helpers import force_list
from inspire_utils.name import normalize_name

from ..utils import EMPTIES


class AuthorBuilder(object):
    """Author record builder."""
    def __init__(self, author=None):
        if author is None:
            author = {}
        self.obj = author

    def _append_to(self, field, element):
        """Append the ``element`` to the ``field`` of the record.

        This method is smart: it does nothing if ``element`` is empty and
        creates ``field`` if it does not exit yet.

        :param field: the name of the field of the record to append to
        :type field: string
        :param element: the element to append
        """
        if element not in EMPTIES:
            self.obj.setdefault(field, [])
            self.obj.get(field).append(element)

    def set_name(self, value):
        """Set the name for the author.

        :param value: should be the family name, the given names, or both, and at least one is required.
        :type value: string
        """
        self._append_to('name', {
            "value": normalize_name(value)
        })

    def set_display_name(self, name):
        """Set the preferred name for the author.

        :param name: preferred name to be displayed for the author.
        :type name: string
        """
        self._append_to('name', {
            "preferred_name": name
        })

    def add_native_name(self, name):
        """Add native name.

        :param name: native name for the current author.
        :type name: string
        """
        if name in self.obj:
            if 'native_names' in self.obj['name']:
                self.obj['name']['native_names'].append(name)
            else:
                self.obj['name']['native_names'] == [name]
        else:
            self._append_to('name', {
                "native_names": [
                    name
                ]
            })

    def add_email_address(self, email):
        """Add email address.

        :param email: public email of the author.
        :type email: string
        """
        self._append_to('email_addresses', email)

    def set_status(self, status):
        """Set the person's status.

        :param status: status from the enumeration of statuses.
        :type status: string
        """
        self._append_to('status', status)

    def add_url(self, value, description=None):
        """Add a personal website.

        :param value: url to the person's website.
        :type value: string

        :param description: short description of the website.
        :type description: string
        """
        self._append_to('urls', {
            'value': value,
            'description': description,
        })

    def add_blog(self, url):
        """Add a personal website as blog.

        :param value: url to the person's blog.
        :type value: string
        """
        self._append_to('urls', {
            'value': url,
            'description': 'blog',
        })

    def add_linkedin(self, url):
        """Add a linkedIn url.

        :param value: url to the person's linkedIn profile.
        :type value: string
        """
        self._append_to('ids', {
            'value': url,
            'schema': 'LINKEDIN',
        })

    def add_twitter(self, url):
        """Add a Twitter url.

        :param value: url to the person's Twitter profile.
        :type value: string
        """
        self._append_to('ids', {
            'value': url,
            'schema': 'TWITTER',
        })

    def add_research_field(self, category):
       	"""Add a field of research.

        :param category: valid arxiv category related to the field of research.
        :type category: string
        """
        self._append_to('arxiv_categories', category)

    def add_institution(self, institution, start_date=None, end_date=None, rank=None, record=None, curated=False, current=False):
        """Add an institution where the person works/worked.

        :param institution: name of the institution.
        :type institution: string

        :param start_date: the date when the person joined the institution, in any format.
        :type start_date: string

        :param end_date: the date when the person left the institution, in any format.
        :type end_date: string

        :param rank: the rank of academic position of the person inside the institution.
        :type rank: string

        :param record: URI for the institution record.
        :type record: string

        :param curated: if the institution has been curated i.e. has been verified.
        :type curated: boolean

        :param current: if the person is currently associated with this institution.
        :type current: boolean
        """
        new_institution = {}
        new_institution['institution'] = institution
        if start_date:
            new_institution['start_date'] = normalize_date(start_date)
        if end_date:
            new_institution['end_date'] = normalize_date(end_date)
        if rank:
            new_institution['rank'] = rank
        if record:
            new_instituion['record'] = record
        new_institution['curated_relation'] = curated
        new_institution['current'] = current
        self._append_to('positions', new_institution)

    def add_project(self, name, record=None, start_date=None, end_date=None, curated=False, current=False):
        """Add an experiment that the person worked on.

        :param name: name of the experiment.
        :type name: string

        :param start_date: the date when the person started working on the experiment.
        :type start_date: string

        :param end_date: the date when the person stopped working on the experiment.
        :type end_date: string

        :param record: URI for the experiment record.
        :type record: string

        :param curated: if the experiment has been curated i.e. has been verified.
        :type curated: boolean

        :param current: if the person is currently working on this experiment.
        :type current: boolean
        """
        new_experiment = {}
        new_experiment['institution'] = institution
        if start_date:
            new_experiment['start_date'] = normalize_date(start_date)
        if end_date:
            new_experiment['end_date'] = normalize_date(end_date)
        if record:
            new_experiment['record'] = record
        new_experiment['curated_relation'] = curated
        new_experiment['current'] = current
        self._append_to('project_membership', new_experiment)

    def add_advisor(self, name, ids=None, degree_type=None, record=None, curated=False):
        """Add an advisor.

        :param name: full name of the advisor.
        :type name: string

        :param ids: list with the IDs of the advisor.
        :type ids: list

        :param degree_type: one of the allowed types of degree the advisor helped with.
        :type degree_type: string

        :param record: URI for the advisor.
        :type record: string

        :param curated: if the advisor relation has been curated i.e. has been verified.
        :type curated: boolean
        """
        new_advisor = {}
        new_advisor['name'] = normalize_name(name)
        if ids:
            new_advisor['ids'] = force_list(ids)
        if degree_type:
            new_advisor['degree_type'] = degree_type
        if record:
            new_advisor['record'] = record
        new_advisor['curated_relation'] = curated
        self._append_to('advisors', new_advisor)

    def add_comment(self, comment, source=None):
        """Add a private comment.

        :param comment: comment about the author.
        :type comment: string
        """
        self._append_to('_private_notes', {
            'value': comment,
            'source': source,
        })
