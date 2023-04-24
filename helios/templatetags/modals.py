from django import template
from django.template import TemplateSyntaxError

register = template.Library()
 
'''
https://andrearobertson.com/2019/06/01/django-example-creating-a-custom-block-tag/
'''
@register.tag
def modal(parser, token):
    try:
        tag_name, modal_id, title = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r takes two arguments: the modal id and title" % token.contents.split()[0])
    print(title)
    nodelist = parser.parse(('endmodal',))
    parser.delete_first_token()
    return ModalNode(modal_id, title, nodelist)

class ModalNode(template.Node):
    def __init__(self, modal_id, title, nodelist):
        self.modal_id = modal_id
        self.title = title
        self.nodelist = nodelist
 
    def render(self, context):
        output = \
            f'<div class="modal fade" id="{self.modal_id}" role="dialog" aria-labelledby="{self.modal_id}Title" aria-hidden="true">' \
            '    <div class="modal-dialog modal-dialog-centered" role="document">' \
            '        <div class="modal-content">' \
            '            <div class="modal-header">' \
            f'                <h5 class="modal-title" id="{self.modal_id}Title">{self.title}</h5>' \
            '                <button type="button" class="close" data-dismiss="modal" aria-label="Close">' \
            '                    <span aria-hidden="true">×</span>' \
            '                </button>' \
            '             </div>' \
            '             <div class="modal-body">' \
            f'                {self.nodelist.render(context)}' \
            '            </div>' \
            '        </div>' \
            '    </div>' \
            '</div>'
        return output