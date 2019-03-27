from .core import HTMLObject

def ComboButton(HTMLObject):

    def __init__(self, button_string, combo_list, breaks=None):
        super(ComboButton, self).__init__(klass="container")

        dropdown = HTMLObject(css={"class":["dropdown"]})

        button = HTMLObject(
            tag="button",
            css={"class":["btn", "btn-default", "dropdown-toggle"],
                 "mixins":{"type":"button", "data-toggle":"dropdown"},
                 "id":"menu1"},
            innerText=button_string,
        )

        button.append(HTMLObject(tag="span", css={"class":["caret"]}))

        dropdown.append(button)

        lst = HTMLObject(
            tag="ul",
            css={
                "class":["dropdown-menu"],
                "mixins":{"role":"menu", "aria-labelledby":"menu1"}
            })

        lst.children = [HTMLObject(
            tag="li",
            css={"mixins":{"role":"presentation"}},
        ) for txt in combo_list]
#             children=[HTMLObject(tag="a", css={"mixins":{"role":"menuitem", "tabindex":"-1", "href":url}}, innerText=innerText)]
#         ) for (url, innerText) in combo_list]

        if breaks:
            for c_break in breaks:
                lst.children.insert(c_break, HTMLObject(tag="li", css={"mixins":{"role":"presentation"}, "class":["divider"]}))

        dropdown.append(lst)

        self.append(dropdown)

#creates box that allows user input and dropdown options

class Combo(HTMLObject):
    def __init__(self, list_name, option_list=[], label=None):
        if label:
            super().__init__(tag='label',css={'class':['inputLabel']}, innerText=label)
        else:
            super().__init__()

        input = HTMLObject(tag='input', css={'mixins':{'type':'text', 'list':list_name}})
        self.append(input)

        list_items = [HTMLObject(tag='option',css={'mixins':{'value':option}}, innerText=option) for option in option_list]
        datalist = HTMLObject(tag='datalist', css={'id':list_name}, children=list_items)

        self.append(datalist)
