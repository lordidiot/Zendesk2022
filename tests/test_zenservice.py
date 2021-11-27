import requests
import unittest
from unittest.mock import patch
from zviewer.api import ZendeskService, ZendeskServiceError

# credit: https://stackoverflow.com/a/28507806
def mocked_requests_get(url, params=None, auth=None):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if auth != ('username', 'password'):
        return MockResponse({"error":"Couldn't authenticate you"}, 401)
    
    if url == BASE_URL+"/api/v2/users.json":
        return MockResponse({}, 200)
    if url == BASE_URL+"/api/v2/tickets":
        return MockResponse({'tickets': [{'url': 'https://testing.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:43:50Z', 'updated_at': '2021-11-27T03:43:51Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 903453622326, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': None, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'velit eiusmod reprehenderit officia cupidatat', 'raw_subject': 'velit eiusmod reprehenderit officia cupidatat', 'description': 'Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['est', 'incididunt', 'nisi'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem', 'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/4.json', 'id': 4, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:37Z', 'updated_at': '2021-11-27T03:57:37Z', 'type': None, 'subject': 'ad sunt qui aute ullamco', 'raw_subject': 'ad sunt qui aute ullamco', 'description': 'Sunt incididunt officia proident elit anim ullamco reprehenderit ut. Aliqua sint amet aliquip cillum minim magna consequat excepteur fugiat exercitation est exercitation. Adipisicing occaecat nisi aliqua exercitation.\n\nAute Lorem aute tempor sunt mollit dolor in consequat non cillum irure reprehenderit. Nulla deserunt qui aliquip officia duis incididunt et est velit nulla irure in fugiat in. Deserunt proident est in dolore culpa mollit exercitation ea anim consequat incididunt. Mollit et occaecat ullamco ut id incididunt laboris occaecat qui.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['laborum', 'mollit', 'proident'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/5.json', 'id': 5, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:38Z', 'updated_at': '2021-11-27T03:57:38Z', 'type': None, 'subject': 'aliquip mollit quis laborum incididunt', 'raw_subject': 'aliquip mollit quis laborum incididunt', 'description': 'Pariatur voluptate laborum voluptate sunt ad magna exercitation nulla. In in Lorem minim dolor laboris reprehenderit ad Lorem. Cupidatat laborum qui mollit nostrud magna ullamco. Tempor nisi ex ipsum fugiat dolor proident qui consectetur anim sunt. Dolore consectetur in ex esse et aliqua fugiat enim Lorem ea Lorem incididunt. Non amet elit pariatur commodo labore officia esse anim. In do mollit commodo nulla ullamco culpa cillum incididunt.\n\nEt nostrud aute fugiat voluptate tempor ad labore in elit et sunt. Enim quis nulla eu ut sit. Pariatur irure officia occaecat non dolor est excepteur anim incididunt commodo ea cupidatat minim excepteur. Cillum proident tempor laborum amet est ipsum ipsum aliqua sit sunt reprehenderit fugiat aliqua ea.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['consectetur', 'mollit', 'sit'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}], 'next_page': None, 'previous_page': None, 'count': 5}, 200)
    if url == BASE_URL+"/api/v2/tickets/2.json":
        return MockResponse({'ticket': {'url': 'https://testing.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'velit eiusmod reprehenderit officia cupidatat', 'raw_subject': 'velit eiusmod reprehenderit officia cupidatat', 'description': 'Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['est', 'incididunt', 'nisi'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}}, 200)
    if url == BASE_URL+"/api/v2/tickets/show_many.json?ids=3,7,9":
        return MockResponse({'tickets': [{'url': 'https://testing.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem', 'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/7.json', 'id': 7, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:39Z', 'updated_at': '2021-11-27T03:57:39Z', 'type': None, 'subject': 'cillum quis nostrud labore amet', 'raw_subject': 'cillum quis nostrud labore amet', 'description': 'Deserunt officia ea fugiat dolor eu laboris esse reprehenderit deserunt dolore voluptate amet culpa. Proident ut mollit adipisicing occaecat Lorem do ut ex aute laboris fugiat minim dolor. In anim non nostrud adipisicing aliquip nisi laborum cupidatat officia. Sunt cillum sint anim elit culpa commodo amet excepteur consectetur veniam nulla ut. Officia ut ut sit incididunt cupidatat velit proident cupidatat voluptate eu ex.\n\nVelit nisi voluptate nulla reprehenderit officia consectetur dolor nostrud cillum duis. Dolore cupidatat eu veniam ut fugiat mollit ea. Reprehenderit nulla nisi cillum voluptate ex. Occaecat incididunt id mollit deserunt occaecat adipisicing ullamco ipsum. Minim ullamco adipisicing quis aliquip est ex sunt ea quis. Sint aute occaecat velit ipsum enim qui fugiat esse in officia excepteur irure. Enim eu dolore reprehenderit exercitation ullamco est nulla voluptate consectetur aliqua sit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['ad', 'et', 'lorem'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/9.json', 'id': 9, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:40Z', 'updated_at': '2021-11-27T03:57:40Z', 'type': None, 'subject': 'veniam ea eu minim aute', 'raw_subject': 'veniam ea eu minim aute', 'description': 'Ex non officia in ullamco veniam fugiat cupidatat id aute. Quis minim et quis laborum excepteur. Non officia quis tempor quis nisi et. Aliqua tempor voluptate nulla esse sint. Id nulla consequat sint eiusmod nisi.\n\nCupidatat anim magna qui aliquip. Anim deserunt sint incididunt labore aliquip. Reprehenderit magna deserunt reprehenderit irure Lorem nulla est officia cupidatat in. Dolore ullamco veniam proident consectetur amet ad nulla amet commodo enim occaecat. Sint fugiat dolor aliqua proident. Ex enim eu pariatur qui officia cupidatat adipisicing esse qui fugiat. Do mollit quis cillum quis qui occaecat labore.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['ad', 'aute', 'et'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}], 'next_page': None, 'previous_page': None, 'count': 3}, 200)

BASE_URL = "https://testing.zendesk.com"

class ZendeskServiceTest(unittest.TestCase):
    @patch('requests.get', side_effect=mocked_requests_get)
    def test_connect(self, mock_get):
        api_service = ZendeskService(BASE_URL, "username", "password")

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_list(self, mock_get):
        api_service = ZendeskService(BASE_URL, "username", "password")
        tickets = api_service.list_tickets()
        tickets_expected = [{'url': 'https://testing.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:43:50Z', 'updated_at': '2021-11-27T03:43:51Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 903453622326, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': None, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'velit eiusmod reprehenderit officia cupidatat', 'raw_subject': 'velit eiusmod reprehenderit officia cupidatat', 'description': 'Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['est', 'incididunt', 'nisi'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem', 'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/4.json', 'id': 4, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:37Z', 'updated_at': '2021-11-27T03:57:37Z', 'type': None, 'subject': 'ad sunt qui aute ullamco', 'raw_subject': 'ad sunt qui aute ullamco', 'description': 'Sunt incididunt officia proident elit anim ullamco reprehenderit ut. Aliqua sint amet aliquip cillum minim magna consequat excepteur fugiat exercitation est exercitation. Adipisicing occaecat nisi aliqua exercitation.\n\nAute Lorem aute tempor sunt mollit dolor in consequat non cillum irure reprehenderit. Nulla deserunt qui aliquip officia duis incididunt et est velit nulla irure in fugiat in. Deserunt proident est in dolore culpa mollit exercitation ea anim consequat incididunt. Mollit et occaecat ullamco ut id incididunt laboris occaecat qui.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['laborum', 'mollit', 'proident'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/5.json', 'id': 5, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:38Z', 'updated_at': '2021-11-27T03:57:38Z', 'type': None, 'subject': 'aliquip mollit quis laborum incididunt', 'raw_subject': 'aliquip mollit quis laborum incididunt', 'description': 'Pariatur voluptate laborum voluptate sunt ad magna exercitation nulla. In in Lorem minim dolor laboris reprehenderit ad Lorem. Cupidatat laborum qui mollit nostrud magna ullamco. Tempor nisi ex ipsum fugiat dolor proident qui consectetur anim sunt. Dolore consectetur in ex esse et aliqua fugiat enim Lorem ea Lorem incididunt. Non amet elit pariatur commodo labore officia esse anim. In do mollit commodo nulla ullamco culpa cillum incididunt.\n\nEt nostrud aute fugiat voluptate tempor ad labore in elit et sunt. Enim quis nulla eu ut sit. Pariatur irure officia occaecat non dolor est excepteur anim incididunt commodo ea cupidatat minim excepteur. Cillum proident tempor laborum amet est ipsum ipsum aliqua sit sunt reprehenderit fugiat aliqua ea.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['consectetur', 'mollit', 'sit'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}]
        self.assertEqual(tickets, tickets_expected)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_ticket_single(self, mock_get):
        api_service = ZendeskService(BASE_URL, "username", "password")
        ticket = api_service.get_ticket(2)
        ticket_expected = {'url': 'https://testing.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'velit eiusmod reprehenderit officia cupidatat', 'raw_subject': 'velit eiusmod reprehenderit officia cupidatat', 'description': 'Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['est', 'incididunt', 'nisi'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}
        self.assertEqual(ticket, ticket_expected)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_tickets_multiple(self, mock_get):
        api_service = ZendeskService(BASE_URL, "username", "password")
        tickets = api_service.get_tickets([3,7,9])
        tickets_expected = [{'url': 'https://testing.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:36Z', 'updated_at': '2021-11-27T03:57:36Z', 'type': None, 'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem', 'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/7.json', 'id': 7, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:39Z', 'updated_at': '2021-11-27T03:57:39Z', 'type': None, 'subject': 'cillum quis nostrud labore amet', 'raw_subject': 'cillum quis nostrud labore amet', 'description': 'Deserunt officia ea fugiat dolor eu laboris esse reprehenderit deserunt dolore voluptate amet culpa. Proident ut mollit adipisicing occaecat Lorem do ut ex aute laboris fugiat minim dolor. In anim non nostrud adipisicing aliquip nisi laborum cupidatat officia. Sunt cillum sint anim elit culpa commodo amet excepteur consectetur veniam nulla ut. Officia ut ut sit incididunt cupidatat velit proident cupidatat voluptate eu ex.\n\nVelit nisi voluptate nulla reprehenderit officia consectetur dolor nostrud cillum duis. Dolore cupidatat eu veniam ut fugiat mollit ea. Reprehenderit nulla nisi cillum voluptate ex. Occaecat incididunt id mollit deserunt occaecat adipisicing ullamco ipsum. Minim ullamco adipisicing quis aliquip est ex sunt ea quis. Sint aute occaecat velit ipsum enim qui fugiat esse in officia excepteur irure. Enim eu dolore reprehenderit exercitation ullamco est nulla voluptate consectetur aliqua sit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['ad', 'et', 'lorem'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}, {'url': 'https://testing.zendesk.com/api/v2/tickets/9.json', 'id': 9, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-27T03:57:40Z', 'updated_at': '2021-11-27T03:57:40Z', 'type': None, 'subject': 'veniam ea eu minim aute', 'raw_subject': 'veniam ea eu minim aute', 'description': 'Ex non officia in ullamco veniam fugiat cupidatat id aute. Quis minim et quis laborum excepteur. Non officia quis tempor quis nisi et. Aliqua tempor voluptate nulla esse sint. Id nulla consequat sint eiusmod nisi.\n\nCupidatat anim magna qui aliquip. Anim deserunt sint incididunt labore aliquip. Reprehenderit magna deserunt reprehenderit irure Lorem nulla est officia cupidatat in. Dolore ullamco veniam proident consectetur amet ad nulla amet commodo enim occaecat. Sint fugiat dolor aliqua proident. Ex enim eu pariatur qui officia cupidatat adipisicing esse qui fugiat. Do mollit quis cillum quis qui occaecat labore.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 903453620166, 'submitter_id': 903453620166, 'assignee_id': 903453620166, 'organization_id': 900063374026, 'group_id': 4410508687641, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['ad', 'aute', 'et'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 900001876306, 'brand_id': 900002795566, 'allow_channelback': False, 'allow_attachments': True}]
        self.assertEqual(tickets, tickets_expected)
    
    @patch('requests.get', side_effect=mocked_requests_get)
    def test_fail_auth(self, mock_get):
        with self.assertRaises(ZendeskServiceError) as cm:
            api_service = ZendeskService(BASE_URL, "badusername", "badpassword")

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_bad_subdomain(self, mock_get):
        with self.assertRaises(ZendeskServiceError) as cm:
            api_service = ZendeskService('f;1;1d;12;d2;dsdfasf;1', "username", "password")

if __name__ == '__main__':
    unittest.main()