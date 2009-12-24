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
from zope.traversing.browser import absoluteURL
from zojax.principal.profile.interfaces import IPersonalProfile


class MessageView(object):

    def update(self):
        profile = IPersonalProfile(self.context)

        self.name = profile.title

        space = profile.space
        if space is not None:
            self.space = u'%s/'%absoluteURL(space, self.request)
        else:
            self.space = None
