##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, schema
from zope.component import getUtility
from zope.app.authentication.principalfolder import Principal

from zojax.layoutform import button, Fields, PageletForm
from zojax.principal.registration.interfaces import IPortalRegistration
from zojax.principal.registration.interfaces import IMemberRegistrationForm


class IRegForm(interface.Interface):

    id = schema.TextLine(title=u'User Id')

    title = schema.TextLine(title=u'User Title')


class TestingActionForm(PageletForm):
    interface.implements(IMemberRegistrationForm)

    fields = Fields(IRegForm)
    ignoreContext = True

    @button.buttonAndHandler(u"Register")
    def handle_register(self, action):
        request = self.request

        data, errors = self.extractData()
