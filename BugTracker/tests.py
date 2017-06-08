from django.test import TestCase
from django.contrib.auth.models import User
from BugTracker.models import Issue, State, Comment

class StateTestCase(TestCase):
    def setUp(self):
        State.objects.create(name='testState')
    
    def testState(self):
        state = State.objects.get(name='testState')
        self.assertEqual(str(state), "testState")

class IssueTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1')
        state = State.objects.create(name='testState')   
        Issue.objects.create(owner=user,state=state,name="testName",description="testDescription")

    def testIssue(self):
        issue = Issue.objects.get(name="testName")
        self.assertEqual(str(issue), "testName")
        
class CommentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1')
        state = State.objects.create(name='testState')   
        issue = Issue.objects.create(owner=user,state=state,name="testName",description="testDescription")
        Comment.objects.create(owner=user,comment="test",issue=issue)
    
    def testComment(self):
        comment = Comment.objects.get(id="1")
        self.assertEqual(str(comment), "user1 about testName")