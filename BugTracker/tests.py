from django.test import TestCase
from django.contrib.auth.models import User
from BugTracker.models import Issue, State, Comment

class IssueTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1')
        state = State.objects.create(name='testState')   
        Issue.objects.create(owner=user,state=state,name="testName",description="testDescription")

    def testA(self):
        issue = Issue.objects.get(name="testName")
        self.assertEqual(str(issue), "testName by user1")