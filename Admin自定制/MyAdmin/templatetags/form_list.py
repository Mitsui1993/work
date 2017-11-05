from django.template import Library
from django.forms.models import ModelChoiceField
from django.urls import reverse
from MyAdmin.service import v1
register = Library()

@register.inclusion_tag("md/form.html")
def show_add_edit_form(form):
    """
    根据传的modelform多个对象，生成展示页面，在处理FK与M2M字段时，在reg.py注册了model后，
    生成一个a标签，跳转到对于FK或M2M对应表的新增页面中。
    :param form:查询到的由ModelForm生成的对象
    :return:封装的ModelForm对象 {'is_popup':False,'item':ModelForm对象,'popup_url':FK或M2M对象的表的新增数据url}
    """
    form_list = []
    for item in form:
        row = {'is_popup':False,'item':None,'popup_url':None}
        if isinstance(item.field,ModelChoiceField) and item.field.queryset.model in v1.site._registry:
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            url_name = "{0}:{1}_{2}_add".format(v1.site.namespace,target_app_label,target_model_name)
            #对于Form对象生成标签时会有默认的ID，即用auto_id可取到
            target_url = "{0}?popup={1}".format(reverse(url_name),item.auto_id)

            row['is_popup'] = True
            row['item'] = item
            row['popup_url'] = target_url
        else:
            row['item'] = item
        form_list.append(row)
    return {'form':form_list}








