from django import forms
from blog.models import Blog
from ckeditor.widgets import CKEditorWidget

from comment.models import Comment


class CommentForm(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(config_name="comment_ckeditor"),
                           error_messages={'required': '评论内容不能为空'})

    object_id = forms.IntegerField(widget=forms.HiddenInput)

    content_type = forms.CharField(widget=forms.HiddenInput)#设置HiddenInput隐藏不显示

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))


    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError("用户尚未登录")
        # 验证评论数据
        object_id = self.cleaned_data['object_id']
        content_type = self.cleaned_data['content_type']
        try:
            content_object = Blog.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = content_object
        except Exception as e:
            raise forms.ValidationError("评论对象不存在")
        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id



"""1.
form类的运行顺序是init，clean，validte，save

其中clean和validate会在form.is_valid()
方法中被先后调用。(这里留有一个疑问，结构完全相同的两个form，但是一个为先验证后clean，另一个先clean后验证。原因不明。)

这里
https: // docs.djangoproject.com / en / dev / ref / forms / validation / 给的是先验证后clean

2.
cleaned_data中的值类型与字段定义的Field类型一致。

如果字段定义charfield，那么clean方法返回的cleaned_data中对应的字段值就是字符型，

定义为ModelChoiceField，则cleaned_data中字段值是某个model实例。

定义为ModelMultipleChoiceField，则cleaned_data中字段值是个model实例list。



3.
clean等步骤遇到的异常：Exception
Value: argument
of
type
'NoneType' is not iterable.

可能是cleaned_data中某个字段值应该是个列表，实际上却是空值。



4.
ModelForm的Meta类中定义的fields

默认的Field是Model中定义的Field，如需更改，可在Form类内以同名字段覆盖，比如自定义widget和required属性等。

不管字段在form中怎么自定义，cleaned_data中对应的值都必须按照model中定义的字段类型取值，否则校验不通过或保存时报错。



暂时记这几条，form还可以重写init、save方法，并且可以自定义方法。如果对这几个东西不懂，想办法找例子读一遍就懂了。



※※※ clean方法重写时一定不要忘了return
cleaned_data ※※※



补充：

5.
form的四种初始化方式

①实例化oneform(initial={'onefield': value})

②定义字段时给初始化值oneformfield = forms.CharField(initial=value)

③重写Form类的__init__()
方法：self.fields['onefield'].initial = value

④当给form传参instanse(即oneform(instanse=onemodel_instance))
时，前三种初始化方法会全部失效，即使重写__init__时，先调用父类的__init__再使用方法③，仍然无效(不是很爽)。

这时想重新初始化字段值只能在__init__()
里
self.initial['title'] = value，直接对Form类的initial属性字典赋值。"""