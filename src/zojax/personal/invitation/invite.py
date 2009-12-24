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
from zope.component import getAdapter, getUtility, getMultiAdapter
from zope.app.component.hooks import getSite
from z3c.schema.email import RFC822MailAddress
from z3c.breadcrumb.interfaces import IBreadcrumb
from zojax.layoutform.interfaces import ICancelButton
from zojax.layoutform import button, Fields, PageletForm
from zojax.mailtemplate.interfaces import IMailTemplate
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.principal.registration.interfaces import IPortalRegistration

from interfaces import _


class IInviteForm(interface.Interface):

    name = schema.TextLine(
        title = _(u'Name'),
        required = False)

    email = RFC822MailAddress(
        title = _(u'Email'),
        required = True)

    subject = schema.TextLine(
        title = _(u'Subject'),
        required = True)

    message = schema.Text(
        title = _(u'Message'),
        required = True)


class InviteForm(PageletForm):

    fields = Fields(IInviteForm)

    label = _(u'Invite People to Join site')
    description = _(u'Tell other people about this site.')

    def update(self):
        super(InviteForm, self).update()

        self.widgets['subject'].style = u'width: 80%'

    def getContent(self):
        crumb = getMultiAdapter((getSite(), self.request), IBreadcrumb)

        title = IPersonalProfile(self.request.principal).title
        return {'subject': u'%s invites you to join %s site'%(title.strip(), crumb.name),
                'message': u'Hello,\n\nJoin the site %s!'%crumb.name}

    @button.buttonAndHandler(_('Invite'))
    def inviteHandler(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(
                _('Please fix indicated errors.'), 'warning')
        else:
            invitation = getUtility(IPortalRegistration).invitePerson(
                self.request.principal.id,
                data['name'], data['email'], data['subject'], data['message'])

            template = getMultiAdapter((invitation, self.request), IMailTemplate)
            template.send((data['email'],))

            IStatusMessage(self.request).add(_('Invitation has been sent.'))
            self.redirect('.')

    @button.buttonAndHandler(_('Cancel'), provides=ICancelButton)
    def cancelHandler(self, action):
        self.redirect('.')
