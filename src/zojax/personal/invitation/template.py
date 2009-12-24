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
from email.Utils import formataddr

from zope import interface, component
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zojax.principal.profile.interfaces import IPersonalProfile

message = u"""

Your invitation code: %s

Or use link %s
"""


class InvitationMail(object):

    def update(self):
        super(InvitationMail, self).update()

        context = self.context

        self.url = u'%s/join.html?invitationCode=%s'%(
            absoluteURL(getSite(), self.request), context.id)

        profile = IPersonalProfile(self.request.principal, None)
        if profile is not None and profile.email:
            self.addHeader(u'From', formataddr((profile.title, profile.email),))

        self.addHeader(u'To', formataddr((context.name, context.principal),))

    @property
    def subject(self):
        return self.context.subject

    def render(self):
        return self.context.message + message%(self.context.id, self.url)
