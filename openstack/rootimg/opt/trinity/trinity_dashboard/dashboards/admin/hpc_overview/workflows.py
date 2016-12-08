from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import workflows

from openstack_dashboard.api import trinity


class AllocateAction(workflows.Action):
#  name        = forms.CharField   (label=_("Name of the cluster"),
#                         required=True)
#  enabled     = forms.BooleanField(label=_("Allocate HPC resources to this project"),
#                         required=True, initial=False)
#  description = forms.CharField   (label=_("Description"),
#                         widget=forms.widgets.Textarea(), required=False)
#  default     = forms.BooleanField(label=_("Boot with default configuration?"),
#                         required=True, initial=False)
#  login       = forms.IntegerField(label=_("Number of login nodes"),
#                         min_value=1)
  

#  def  __init__(self,request, context, *args, **kwargs):
#    super(AllocateAction,self).__init__(request, context, *args, **kwargs) 
  def  __init__(self,request, context,*args, **kwargs):
    super(AllocateAction,self).__init__(request, context,*args, **kwargs) 
    cluster=self.initial['cluster']
    field        = forms.CharField   (label=_("Name of the cluster"),
                         required=True, initial=cluster)
    self.fields.update({'name':field})

    initial_nodes=trinity.cluster_hardware(request, cluster, summary=True)
    field = forms.CharField(label=_("List of nodes"),
                            required=False, initial=initial_nodes)
    self.fields.update({'nodes':field})



#  compute     = forms.IntegerField(label=_("Generic compute nodes"),
#                         min_value=0,required=True)
#  gpu         = forms.IntegerField(label=_("GPU enabled nodes"),
#                         min_value=0,required=False)
#  highmem     = forms.IntegerField(label=_("High memory nodes"),
#                         min_value=0,required=False)
  
  class Meta:
    name = _("HPC Resources")
    help_text = _("From here you can allocate HPC resources to your project.\n"
                  "This field accepts hostlist formatting as well as comma "
                  "separated lists of nodes.\n"
                  "e.g. c[001-020] or c001,c002")


class AllocateStep(workflows.Step):
  action_class = AllocateAction
  depends_on=('cluster',)
  def __init__(self,workflow):
    super(AllocateStep,self).__init__(workflow)
#    contributes=['name','description','login']
    contributes=['name', 'nodes']
    self.contributes=tuple(contributes)

#    
#  contributes = ("name",
#                 "description",
#                 "login",
#                 "hm",
#                 "gpu",)
#


class CreateCluster(workflows.Workflow):
  slug = "create_cluster"
  name = _("Create Cluster")
  finalize_button_name = _("Create Cluster")
  success_message = _('Created new cluster')
  failure_message = _('Unable to create cluster')
  success_url = "horizon:admin:hpc_overview:index"
  default_steps = (AllocateStep,)
  def handle(self,request,data):
    c = trinity.cluster_modify(request=request,data=data)
    return c    


class UpdateCluster(workflows.Workflow):
  slug = "update_cluster"
  name = _("Update Cluster")
  finalize_button_name = _("Save Changes")
  success_message = _('Cluster updated')
  failure_message = _('Unable to make requested changes')
  success_url = "horizon:admin:hpc_overview:index"
  default_steps = (AllocateStep,)
  def handle(self,request,data):
    c = trinity.cluster_modify(request=request,data=data)
    return c

