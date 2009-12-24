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
from zope import component, interface
from zope.component import queryMultiAdapter
from zope.security.management import queryInteraction
from zojax.layout.interfaces import IPagelet
from zojax.ownership.interfaces import IOwnership
from zojax.messaging.interfaces import IMessageStorage
from zojax.personal.messages.interfaces import SERVICE_ID
from zojax.principal.invite.interfaces import IInvitationAcceptedEvent
from zojax.principal.registration.interfaces import IMembershipInvitation


@component.adapter(IMembershipInvitation, IInvitationAcceptedEvent)
def invitationAcceptedHandler(invitation, event):
    owner = IOwnership(invitation).owner
    if owner is None:
        return

    messaging = IMessageStorage(owner, None)
    if messaging is None:
        return

    interaction = queryInteraction()

    if interaction is not None:
        for request in interaction.participations:
            principal = invitation.principal

            view = queryMultiAdapter(
                (principal, request), IPagelet, 'personal.message')
            if view is None:
                return

            view.update()

            data = {'title': u'Your invitation has been accepted',
                    'text': view.render(),
                    'sender': unicode(principal.id)}
            messaging.create(SERVICE_ID, **data)
