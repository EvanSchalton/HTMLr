from HTMLr.Core import HTMLObject

def ComboButton(button_string, combo_list, breaks=None, enricher=None):
    container = HTMLObject(css={"class":["container"]})

    dropdown = HTMLObject(css={"class":["dropdown"]})

    button = HTMLObject(
        tag="button",
        css={"class":["btn", "btn-default", "dropdown-toggle"],
             "mixins":{"type":"button", "data-toggle":"dropdown"},
             "id":"menu1"},
        inner_string=button_string,
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
        children=[HTMLObject(tag="a", css={"mixins":{"role":"menuitem", "tabindex":"-1", "href":url}}, inner_string=inner_str)]
    ) for (url, inner_str) in combo_list]

    if breaks:
        for c_break in breaks:
            lst.children.insert(c_break, HTMLObject(tag="li", css={"mixins":{"role":"presentation"}, "class":["divider"]}))

    dropdown.append(lst)

    container.append(dropdown)

    return container.get_html(enricher=enricher)

#creates box that allows user input and dropdown options

def ComboInput(list_name, option_list=[], label=None):
    if label:
        ComboInput = HTMLObject(tag='label',css={'class':['inputLabel']}, inner_string=label)
    else:
        ComboInput = HTMLObject()

    input = HTMLObject(tag='input', css={'mixins':{'type':'text', 'list':list_name}})
    ComboInput.append(input)

    list_items = [HTMLObject(tag='option',css={'mixins':{'value':option}}, inner_string=option) for option in option_list]
    datalist = HTMLObject(tag='datalist', css={'id':list_name}, children=list_items)

    ComboInput.append(datalist)

    return ComboInput
