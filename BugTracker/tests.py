from django.test import TestCase
from django.contrib.auth.models import User
from BugTracker.models import Issue, State, Comment
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1')
        user.set_password('test')
        user.save()
    
    def testLogin(self):
        #Use credentials to call 'issue' see if authentication has worked
        token = Token.objects.get(user__username='user1')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/bugTracker/issue/')
        self.assertEqual(response.status_code, 200,"Test Return Code Login")

class StateTestCase(TestCase):
    def setUp(self):
        State.objects.create(name='testState')
    
    def testStateDB(self):
        #DB test
        state = State.objects.get(name='testState')
        self.assertEqual(str(state), "testState")

class IssueTestCase(TestCase):    
    def setUp(self):
        user = User.objects.create(username='user1')
        user.set_password('test')
        user.save()
        state = State.objects.create(name='testState')
        Issue.objects.create(owner=user,state=state,name="testName",description="testDescription")

    def testIssueDB(self):
        #DB test
        issue = Issue.objects.get(name="testName")
        self.assertEqual(str(issue), "testName")
        
    def testAPIIssue(self):
        token = Token.objects.get(user__username='user1')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        idState = State.objects.get(name='testState').id
        response = client.post('/bugTracker/issue/',{'name':'testIssue','description':'testDescription','state':idState})
        idIssue = response.data['id']
        
        #Add Issue
        self.assertEqual(response.status_code, 201, "Test Return Code Add Issue")

        #Get Issue        
        response = client.get('/bugTracker/issue/'+str(idIssue))
        self.assertEqual(response.data['name'], "testIssue", "Test Name Added Issue")
        self.assertEqual(response.status_code, 200, "Test Return Code Get Issue")
        
        #Update Issue
        client.patch('/bugTracker/issue/'+str(idIssue), {'name':'testIssue2'})
        response = client.get('/bugTracker/issue/'+str(idIssue))
        self.assertEqual(response.data['name'], "testIssue2", "Test Name Edit Issue")
        self.assertEqual(response.status_code, 200, "Test Return Code Patch Issue")

        
        
        client.logout()

class CommentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1')
        state = State.objects.create(name='testState')   
        issue = Issue.objects.create(owner=user,state=state,name="testName",description="testDescription")
        Comment.objects.create(owner=user,comment="test",issue=issue)
    
    def testCommentDB(self):
        #DB test
        comment = Comment.objects.get(comment="test")
        self.assertEqual(str(comment), "user1 about testName")
        
    def testAPIComment(self):
        token = Token.objects.get(user__username='user1')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        idIssue = Issue.objects.get(name='testName').id

        response = client.post('/bugTracker/comment/',{'comment':'HelloWorld','issue':idIssue})
        idComment = response.data['id']
        
        #Add Issue
        self.assertEqual(response.status_code, 201, "Test Return Code Add Comment")

        #Get Issue        
        response = client.get('/bugTracker/comment/'+str(idComment))
        self.assertEqual(response.data['comment'], "HelloWorld", "Test Name Get Comment") 
        self.assertEqual(response.status_code, 200, "Test Return Code Get Comment")