'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os
from tests import test_settings
from django.core import management
from django.test import SimpleTestCase, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, AnonymousUser
from django.test.client import RequestFactory, Client
from arches.app.views.main import auth
from arches.app.views.concept import rdm
from arches.app.views.resources import resource_manager
from django.contrib.sessions.middleware import SessionMiddleware

from arches.app.utils.set_anonymous_user import SetAnonymousUser
from arches.management.commands.packages import Command as PackageCommand
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.utils.data_management.resources.importer import ResourceLoader
import arches.app.utils.data_management.resources.remover as resource_remover
from arches.management.commands.package_utils import resource_graphs
from arches.management.commands.package_utils import authority_files
from arches.app.models import models
from arches.app.models.entity import Entity
from arches.app.models.resource import Resource
from arches.app.models.concept import Concept
from arches.app.models.concept import ConceptValue
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer

# these tests can be run from the command line via
# python manage.py test tests --pattern="*.py" --settings="tests.test_settings"


class AuthTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@archesproject.org', 'password')
        self.user.save()

        cmd = PackageCommand()
        try: 
            Group.objects.get(name='edit')
            Group.objects.get(name='read')
        except:
            cmd.create_groups()
            cmd.create_users()

        self.anonymous_user = User.objects.get(username='anonymous')

    def test_login(self):
        """
        Test that a user can login and is redirected to the home page

        """

        request = self.factory.post(reverse('auth'), {'username': 'test', 'password': 'password'})
        request.user = self.user
        apply_middleware(request)
        response = auth(request)

        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.get('location') == reverse('home'))

    def test_set_anonymous_user_middleware(self):
        """
        Test to check that any anonymous request to the system gets the anonymous user set on the 
        request as opposed to the built-in AnonymousUser supplied by django

        """

        request = self.factory.get(reverse('home'))
        request.user = AnonymousUser()
        set_anonymous_user(request)

        self.assertTrue(request.user.username == 'anonymous')
        self.assertTrue(request.user != AnonymousUser())

    def test_nonauth_user_access_to_RDM(self):
        """
        Test to check that a non-authenticated user can't access the RDM page, or POST data to the url

        """

        request = self.factory.get(reverse('rdm', args=['']))
        request.user = AnonymousUser()
        apply_middleware(request)
        response = rdm(request)

        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.get('location').split('?')[0] == reverse('auth'))


        # test get a concept
        request = self.factory.get(reverse('rdm', kwargs={'conceptid':'00000000-0000-0000-0000-000000000001'}))
        request.user = AnonymousUser()
        apply_middleware(request)
        response = rdm(request)

        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.get('location').split('?')[0] == reverse('auth'))


        # test update a concept
        concept ={
            "id": "00000000-0000-0000-0000-000000000001",
            "legacyoid": "ARCHES",
            "nodetype": "ConceptScheme",
            "values": [],
            "subconcepts": [{
                "values": [{
                    "value": "test label",
                    "language": "en-US",
                    "category": "label",
                    "type": "prefLabel",
                    "id": "",
                    "conceptid": ""
                },{
                    "value": "",
                    "language": "en-US",
                    "category": "note",
                    "type": "scopeNote",
                    "id": "",
                    "conceptid": ""
                }],
                "relationshiptype": "hasTopConcept",
                "nodetype": "Concept",
                "id": "",
                "legacyoid": "",
                "subconcepts": [],
                "parentconcepts": [],
                "relatedconcepts": []
            }]
        }

        request = self.factory.post(reverse('rdm', kwargs={'conceptid':'00000000-0000-0000-0000-000000000001'}), concept)
        request.user = AnonymousUser()
        apply_middleware(request)
        response = rdm(request)

        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.get('location').split('?')[0] == reverse('auth'))

    def test_nonauth_user_access_to_resource_manager(self):
        """
        Test to check that a non-authenticated user can't perform CRUD on resources

        """

        response = self.client.get(reverse('resource_manager', kwargs={'resourcetypeid':'HERITAGE_RESOURCE.E18', 'form_id': 'summary', 'resourceid': ''}))

        self.assertTrue(response.status_code == 302)
        self.assertTrue(strip_response_location(response) == reverse('auth'))


        postbody = {
            "RESOURCE_TYPE_CLASSIFICATION.E55":[],
            "NAME.E41":[{
                "nodes":[{
                    "property":"",
                    "entitytypeid":"NAME.E41",
                    "entityid":"",
                    "value":"ANP TEST",
                    "label":"",
                    "businesstablename":"",
                    "child_entities":[]
                },{
                    "property":"",
                    "entitytypeid":"NAME_TYPE.E55",
                    "entityid":"",
                    "value":"527d4bcf-d95a-487a-9849-c523a838ae92",
                    "label":"Primary",
                    "businesstablename":"",
                    "child_entities":[]
                }]
            }],
            "important_dates":[],
            "KEYWORD.E55":[]
        }

        response = self.client.post(reverse('resource_manager', kwargs={'resourcetypeid':'HERITAGE_RESOURCE.E18', 'form_id': 'summary', 'resourceid': ''}), data={'formdata':postbody})

        self.assertTrue(response.status_code == 302)
        self.assertTrue(strip_response_location(response) == reverse('auth'))


        response = self.client.delete(reverse('resource_manager', kwargs={'resourcetypeid':'HERITAGE_RESOURCE.E18', 'form_id': 'summary', 'resourceid': ''}), data={'formdata':postbody})

        self.assertTrue(response.status_code == 302)
        self.assertTrue(strip_response_location(response) == reverse('auth'))



    def tearDown(self):
        self.user.delete()


def apply_middleware(request):
    save_session(request)
    set_anonymous_user(request)

def save_session(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

def set_anonymous_user(request):
    set_anon_middleware = SetAnonymousUser()
    set_anon_middleware.process_request(request)

def strip_response_location(response):
    return response.get('location').replace('http://testserver', '').split('?')[0]