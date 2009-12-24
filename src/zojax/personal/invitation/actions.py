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
from zope import interface, component
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zojax.content.actions.action import Action
from zojax.content.actions.interfaces import IAction
from zojax.personal.profile.interfaces import IProfileWorkspace
from zojax.principal.invite.interfaces import IInvitations
from zojax.principal.registration.interfaces import IPortalRegistration

from interfaces import _, IJoinAction, IInvitationsAction, IMyInvitationsAction


class JoinAction(Action):
    interface.implements(IJoinAction)
    component.adapts(IProfileWorkspace, interface.Interface)

    weight = 10000
    title = _(u'Invite person to join this site')
    permissions = 'zojax.ModifyPreference'

    @property
    def url(self):
        return '%s/invite.html'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        principal = self.context.__principal__

        if self.request.principal.id == principal.id:
            return getUtility(IPortalRegistration).invitation

        return False


class InvitationsAction(Action):
    interface.implements(IInvitationsAction)
    component.adapts(IProfileWorkspace, interface.Interface)

    weight = 100001
    title = _(u'Invitations I have sent')
    permissions = 'zojax.ModifyPreference'

    @property
    def url(self):
        return '%s/invitations.html'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        principal = self.context.__principal__
        if self.request.principal.id != principal.id:
            return False

        if not super(InvitationsAction, self).isAvailable():
            return False

        configlet = getUtility(IInvitations)
        if configlet.getInvitationsByOwner(
            principal.id, ('invitation.membership',)):
            return True

        return False


class MyInvitationsAction(Action):
    interface.implements(IMyInvitationsAction)
    component.adapts(IProfileWorkspace, interface.Interface)

    weight = 100002
    title = _(u'Invitations I have received')
    permissions = 'zojax.ModifyPreference'

    @property
    def url(self):
        return '%s/myinvitations.html'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        principal = self.context.__principal__.id
        if principal != self.request.principal.id:
            return False

        if getUtility(IInvitations).getInvitationsByPrincipal(principal):
            return True

        return False
