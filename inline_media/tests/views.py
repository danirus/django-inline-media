import re

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_contactme import signals, signed
from django_contactme.models import ContactMsg
from django_contactme.views import CONTACTME_SALT


MESSAGE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean pulvinar, diam quis iaculis placerat, quam tellus ullamcorper risus, a accumsan lectus dui id nisi. Nulla nisi nulla, feugiat at malesuada ut, commodo sollicitudin urna. Sed adipiscing aliquam metus a scelerisque. Proin in erat ut lectus gravida rutrum. Sed vel eros id turpis convallis scelerisque ut nec nisl. Morbi et odio id ante ullamcorper ultrices. Nulla odio dui, ultricies a egestas nec, aliquet at ligula. Vestibulum scelerisque turpis mollis arcu suscipit laoreet. Suspendisse faucibus erat fermentum tortor facilisis aliquam. Donec vitae arcu elit. In hac habitasse platea dictumst. Morbi congue scelerisque lobortis."


class GetContactFormViewTestCase(TestCase):

    def test_get_contact_form(self):
        response = self.client.get(reverse("contactme-get-contact-form"))
        # Check whether the form has all expected fields
        self.assertContains(response, 'name="timestamp"')
        self.assertContains(response, 'name="security_hash"')
        self.assertContains(response, 'name="honeypot"')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')


class PostContactFormViewTestCase(TestCase):
  
    def setUp(self):
        self.response = self.client.get(reverse("contactme-get-contact-form"))
        for context in self.response.context:
            if context.has_key("form"):
                form = context.get("form")
                self.timestamp = form.initial["timestamp"]
                self.security_hash = form.initial["security_hash"]

    def post_valid_data(self):
        data = {'timestamp':     self.timestamp,
                'security_hash': self.security_hash,
                'name':          'Alice Bloggs',
                'email':         'alice.bloggs@example.com',
                'message':       MESSAGE }
        self.response = self.client.post(
            reverse("contactme-post-contact-form"), data=data)        
  
    def test_post_without_security_data(self):
        data = {'name':    'Alice Bloggs',
                'email':   'alice.bloggs@example.com',
                'message': MESSAGE }
        response = self.client.post(
            reverse("contactme-post-contact-form"), data=data)
        self.assertNotContains(
            response, "Please correct the errors below", status_code=400)
        
    def test_post_with_security_data_and_empty_required_fields(self):
        data = {'timestamp':     self.timestamp,
                'security_hash': self.security_hash,
                'name':          '',
                'email':         '',
                'message':       '' }
        response = self.client.post(
            reverse("contactme-post-contact-form"), data=data)        
        self.assertContains(response, "Please correct the errors below")
        self.assertTemplateUsed(response, "django_contactme/preview.html")

    def test_signal_receiver_may_kill_the_process(self):
        # Test that receivers of signal confirmation_will_be_requested may
        # produce a ContactMsgPostBadRequest (Http code 400) 
        def on_signal(sender, data, request, **kwargs):
            return False

        signals.confirmation_will_be_requested.connect(on_signal)
        self.post_valid_data() # self.response gets updated
        self.assertTemplateUsed(self.response, 
                                "django_contactme/discarded.html")
        
    def test_confirmation_email_is_sent(self):
        self.assertEqual(len(mail.outbox), 0)
        self.post_valid_data() # self.response gets updated
        self.assertEqual(len(mail.outbox), 1)

    def test_signal_confirmation_requested_is_sent(self):
        self.calls = 0
        def on_signal(sender, data, request, **kwargs):
            self.calls += 1

        signals.confirmation_requested.connect(on_signal)
        self.post_valid_data() # self.response gets updated
        self.assert_(self.calls == 1)

    def test_user_is_told_about_confirmation_email_sent(self):
        self.post_valid_data() # self.response gets updated
        self.assertTemplateUsed(self.response, 
                                "django_contactme/confirmation_sent.html")


class ConfirmContactViewTestCase(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("contactme-get-contact-form"))
        for context in self.response.context:
            if context.has_key("form"):
                form = context.get("form")
                timestamp = form.initial["timestamp"]
                security_hash = form.initial["security_hash"]
        data = {'timestamp':     timestamp,
                'security_hash': security_hash,
                'name':          'Alice Bloggs',
                'email':         'alice.bloggs@example.com',
                'message':       MESSAGE }
        self.response = self.client.post(
            reverse("contactme-post-contact-form"), data=data)        
        self.url = re.search(r'http://[\S]+', mail.outbox[0].body).group()

    def get_confirm_contact_url(self, key):
        self.response = self.client.get(reverse("contactme-confirm-contact",
                                                kwargs={'key': key}))

    def test_404_on_bad_signature(self):
        key = self.url.split("/")[-1]
        key = key[:-1]
        self.get_confirm_contact_url(key)
        self.assertContains(self.response, "404", status_code=404)

    def test_consecutive_confirmation_url_visits_fail(self):
        # test that consecutives visits to the same confirmation URL produce
        # an Http 404 code, as the contact_msg has already been verified in
        # first visit
        key = self.url.split("/")[-1]        
        self.get_confirm_contact_url(key)
        self.get_confirm_contact_url(key)
        self.assertContains(self.response, "404", status_code=404)

    def test_signal_receiver_avoids_mailing_admins(self):
        # test that receivers of signal confirmation_received may return False
        # and thus rendering a template_discarded uotput
        def on_signal(sender, data, request, **kwargs):
            return False

        self.assertEqual(len(mail.outbox), 1) # sent during setUp
        signals.confirmation_received.connect(on_signal)
        key = self.url.split("/")[-1]
        self.get_confirm_contact_url(key)
        self.assertEqual(len(mail.outbox), 1) # mailing avoided by on_signal
        self.assertTemplateUsed(self.response, 
                                "django_contactme/discarded.html")

    def test_contact_msg_is_created_and_email_sent(self):
        key = self.url.split("/")[-1]
        self.get_confirm_contact_url(key)
        data = signed.loads(key, extra_key=CONTACTME_SALT)
        try:
            cmsg = ContactMsg.objects.get(email=data["email"], 
                                          name=data["name"],
                                          submit_date=data["submit_date"])
        except:
            cmsg = None
        self.assert_(cmsg != None)
        # be sure that settings module contains either ADMINS or 
        # CONTACTME_NOTIFY_TO, otherwise there won't be 2 mails
        self.assertEqual(len(mail.outbox), 2)

    def test_user_is_told_about_contact_msg_received(self):
        key = self.url.split("/")[-1]
        self.get_confirm_contact_url(key)
        self.assertTemplateUsed(self.response, 
                                "django_contactme/accepted.html")
