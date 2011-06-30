#
#from tests.base import Base
#import iconfig
#
#from project.forms import ProjectPrioritiesFormset
#from project.models import Project
#
#from utils.form_tools import export_formset_to_json
#
#class TestExportFormsetToJSON(Base):
#    fixtures = Base.fixtures + ['tests/test_project_data.xml',
#                                'tests/test_feature_data.xml']
#    def setUp(self):
#        super(self.__class__, self).setUp()
#        #iconfig.loaddata('tests/test_project_data.xml')
#        #iconfig.loaddata('tests/test_feature_data.xml')
#        project = Project.objects.get(abbreviation='TST')
#        self.project = project
#
#    def tearDown(self):
#        del self.project
#        #Project.objects.all().delete()
#
#    def test_export_formset_to_json(self):
#        formset = ProjectPrioritiesFormset(instance=self.project)
#        json_object = export_formset_to_json(formset)
#        assert json_object['forms']
#        assert json_object['management_form']
#        assert len(json_object['forms']) == len(formset.forms)
#
#    def test_export_formset_to_json_with_errors(self):
#        data = {u'priorities-7-id': u'18', u'priorities-11-priority': u'0', u'priorities-TOTAL_FORMS': u'12', u'priorities-7-story': u'http://testserver/story/TST-16/',
#            u'priorities-11-id': u'', u'priorities-4-story': u'http://testserver/story/TST-7/', u'priorities-2-story': u'http://testserver/story/TST-8/',
#            u'priorities-6-project': u'TST', u'priorities-8-id': u'20', u'priorities-3-story': u'http://testserver/story/TST-5/', u'priorities-2-priority': u'3',
#            u'priorities-1-story': u'http://testserver/story/TST-3/', u'priorities-5-id': u'4', u'priorities-10-id': u'2', u'priorities-0-priority': u'1',
#            u'priorities-9-project': u'TST', u'priorities-4-priority': u'6', u'priorities-5-project': u'TST', u'priorities-INITIAL_FORMS': u'11',
#            u'priorities-7-project': u'TST', u'priorities-1-project': u'TST', u'priorities-5-story': u'http://testserver/story/TST-12/',
#            u'priorities-10-story': u'http://testserver/story/TST-9/', u'priorities-10-priority': u'11', u'priorities-8-project': u'TST', u'priorities-3-project': u'TST',
#            u'priorities-8-story': u'http://testserver/story/TST-6/', u'priorities-11-story': u'', u'priorities-9-id': u'23', u'priorities-7-priority': u'8',
#            u'priorities-2-project': u'TST', u'priorities-0-project': u'TST', u'priorities-3-priority': u'4', u'priorities-0-story': u'http://testserver/story/TST-18/',
#            u'priorities-2-id': u'5', u'priorities-6-id': u'12', u'priorities-9-story': u'http://testserver/story/TST-10/', u'priorities-6-priority': u'5',
#            u'priorities-1-priority': u'2', u'priorities-1-id': u'24', u'priorities-8-priority': u'9', u'priorities-9-priority': u'10', u'priorities-10-project': u'TST',
#            u'priorities-3-id': u'17', u'priorities-6-story': u'http://testserver/story/TST-4/', u'priorities-0-id': u'7', u'priorities-4-id': u'9',
#            u'priorities-4-project': u'TST', u'priorities-11-project': u'TST', u'priorities-5-priority': u'7'}
#        item = {u'priorities-INITIAL_FORMS': u'9',u'priorities-TOTAL_FORMS': u'10'}
#        data.update(item)
#        formset = ProjectPrioritiesFormset(data,instance=self.project)
#        json_object = export_formset_to_json(formset)
#        assert json_object['forms']
#        assert json_object['management_form']
#        assert len(json_object['forms']) == len(formset.forms)
#        assert json_object['errors']
#        assert json_object['errors'] == formset.errors