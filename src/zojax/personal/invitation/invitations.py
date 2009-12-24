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
from zope import interface
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zojax.layout.interfaces import IPagelet
from zojax.mailtemplate.interfaces import IMailTemplate
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.principal.invite.interfaces import IInvitations

from interfaces import _


class InvitationsForm(object):

    def update(self):
        request = self.request
        principal = self.context.__principal__
        configlet = getUtility(IInvitations)

        invitations = dict(
            [(invitation.id, invitation)
             for invitation in configlet.getInvitationsByOwner(
                    principal.id, ('invitation.membership',))])

        if 'button.resend' in request:
            ids = request.get('ids', ())
            if not ids:
                IStatusMessage(request).add(
                    _(u'Please select invitations.'), 'warning')
            else:
                for id in ids:
                    invitation = invitations.get(id)

                    if invitation is not None:
                        template = getMultiAdapter(
                            (invitation, request), IMailTemplate)
                        template.send((invitation.email,))

                IStatusMessage(request).add(_(u'Invitations have been sent.'))

        if 'button.remove' in request:
            ids = request.get('ids', ())
            if not ids:
                IStatusMessage(request).add(
                    _(u'Please select invitations.'), 'warning')
            else:
                for id in ids:
                    if id in invitations:
                        del configlet[id]

                IStatusMessage(request).add(_(u'Invitations have been removed.'))

        self.invitations = [invitation for invitation in
                            configlet.getInvitationsByOwner(
                principal.id, ('invitation.membership',))]


class MyInvitations(object):

    def update(self):
        context = self.context
        request = self.request

        invitations = []
        for inv in getUtility(IInvitations).getInvitationsByPrincipal(
            self.context.__principal__.id):
            view = queryMultiAdapter((inv, request), IPagelet)
            if view is not None:
                view.update()
                invitations.append(view)

        self.invitations = invitations
