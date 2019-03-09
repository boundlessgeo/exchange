import os
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from django.utils.six import StringIO
from exchange.themes.models import Theme
from shutil import rmtree

from . import ExchangeTest

theme_dir = os.path.join(
    settings.MEDIA_ROOT,
    'theme'
)


class MockRequest:
    pass


request = MockRequest()


class ThemeTestCase(ExchangeTest):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()
        self.ma = admin.ModelAdmin(Theme, self.site)
        self.t1 = Theme.objects.create(
            name="Test1",
            description="Test Description",
            default_theme=True,
            active_theme=True,
            title="Test Title",
            tagline="Test Tagline",
            running_hex="ffffff",
            running_text_hex="ffffff",
            running_link_hex="ffffff",
            pb_text="Test Powered By Text",
            pb_link="http://boundlessgeo.com/",
            docs_text="Documentation",
            docs_link="/static/docs/html/index.html",
            background_logo="theme/img/default-background.png",
            primary_logo="theme/img/default-primary-logo.png",
            banner_logo="theme/img/default-banner-logo.png"
        )
        self.t1.save()
        self.t2 = Theme.objects.create(
            name="Test2",
            description="Test Description",
            default_theme=False,
            active_theme=True,
            title="Test Title",
            tagline="Test Tagline",
            running_hex="ffffff",
            running_text_hex="ffffff",
            running_link_hex="ffffff",
            pb_text="Test Powered By Text",
            pb_link="http://boundlessgeo.com/",
            docs_text="Documentation",
            docs_link="https://boundlessgeo.github.io/"
                      "exchange-documentation/",
            background_logo=None,
            primary_logo=None,
            banner_logo=None
        )
        self.t2.save()

    def test(self):
        test_img = self.get_file_path('test.png')

        self.assertEqual(
            self.ma.get_fieldsets(request),
            [(None,
              {'fields': [
                  'name',
                  'description',
                  'active_theme',
                  'title',
                  'tagline',
                  'running_hex',
                  'running_text_hex',
                  'running_link_hex',
                  'pb_text',
                  'pb_link',
                  'docs_text',
                  'docs_link',
                  'background_logo',
                  'primary_logo',
                  'banner_logo',
                  'custom_analytics']})])
        self.assertEqual(
            self.t1.background_logo_url,
            '/static/theme/img/default-background.png'
        )
        self.assertEqual(
            self.t1.primary_logo_url,
            '/static/theme/img/default-primary-logo.png'
        )
        self.assertEqual(
            self.t1.banner_logo_url,
            '/static/theme/img/default-banner-logo.png'
        )
        self.assertEqual(self.t1.__unicode__(), self.t1.name)
        self.assertEqual(self.t2.background_logo_url, None)
        self.assertEqual(self.t2.primary_logo_url, None)
        self.assertEqual(self.t2.banner_logo_url, None)
        self.t2.background_logo = SimpleUploadedFile(
            name='test2a_delete_me.png',
            content=open(test_img, 'rb').read(),
            content_type='image/png',
        )
        self.t2.primary_logo = SimpleUploadedFile(
            name='test2b_delete_me.png',
            content=open(test_img, 'rb').read(),
            content_type='image/png',
        )
        self.t2.banner_logo = SimpleUploadedFile(
            name='test2c_delete_me.png',
            content=open(test_img, 'rb').read(),
            content_type='image/png',
        )
        self.t2.save()
        self.assertEqual(
            self.t2.background_logo_url,
            '/media/theme/img/test2a_delete_me.png'
        )
        self.assertEqual(
            self.t2.primary_logo_url,
            '/media/theme/img/test2b_delete_me.png'
        )
        self.assertEqual(
            self.t2.banner_logo_url,
            '/media/theme/img/test2c_delete_me.png'
        )

    def tearDown(self):
        rmtree(theme_dir)


class ThemeViewTest(ExchangeTest):

    def setUp(self):
        super(ThemeViewTest, self).setUp()

        self.login()

    def test_model_admin(self):
        r = self.client.get('/admin/themes/theme/')

        self.assertEqual(r.status_code, 200,
                         'Did not get admin theme list (status: %d)' % (
                             r.status_code))

        r = self.client.get('/admin/themes/theme/add/')

        self.assertEqual(r.status_code, 200, 'Did not get admin theme add')

        r = self.client.get('/admin/themes/theme/1/')
        r = self.client.get('/admin/themes/theme/2/')


class ListThemeTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('list_themes', stdout=out)
        self.assertTrue('Available Themes:' in out.getvalue())


class SetActiveThemeByIdTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('set_active_theme_by_id', theme_id=1, stdout=out)
        self.assertTrue('Successfully' in out.getvalue())


class SetActiveThemeByNameTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command(
            'set_active_theme_by_name',
            theme_name='GEOINT',
            stdout=out
        )
        self.assertTrue('Successfully' in out.getvalue())
