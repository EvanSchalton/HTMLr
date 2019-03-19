import warnings


class HTMLObject(object):
    cssKeys = {"style":[], "id":"", "klass":[], "mixins":{}, "class":[]}
    def __init__(self, tag = "div", css = {"style": [], "id": None, "class": [], "mixins":{}}, innerText = "", children= [], span=None, parent=None, **kwargs):
        self.kwargs = kwargs
        self.tag = tag
        self.css = css
        self +=  {"style": [], "id": None, "class": [], "mixins":{}}
        self += {k.replace("klass", "class"):v for (k, v) in kwargs.items() if k in self.cssKeys}
        self += {"mixins":{k:v for (k,v) in kwargs.items() if k not in self.cssKeys}}
        self += {k:v for (k,v) in self.cssKeys.items() if k != "klass"}
        self.innerText = innerText
        self.children = children
        if self.children:
            for child in self.children:
                child.parent = self

        self.parent = parent
        # self.parent_enricher = []
        # self.enricher = []
        self.span = span

    def __getattr__(self, attr):
        # print("getattr:", attr)
        if attr in self.cssKeys:
            if attr == "klass":
                attr="class"
            return self.css.get(attr, self.cssKeys[attr])
        else:
            raise AttributeError

    def __setattr__(self, attr, value):
        # print("setattr:", attr, "=", value)
        if attr in self.cssKeys:
            if attr == "klass":
                attr="class"
                # print(attr, value, type(value))
            if attr in [attr_name for attr_name, val in self.cssKeys.items() if isinstance(val, list)]:
                if isinstance(value, str):
                    value = [value]
                    # print(attr, value, type(value))
                if len([j for j in [len(i)==1 for i in value] if j]) > 1:
                    warnings.warn("likely error in '{}' attribute, looks like a string was provided when a list is required.".format(attr))

            self += {attr:value}
            #elif attr not in ["args", "kwargs"]:
        else:
            super().__setattr__(attr, value)

    def __add__(self, css):
        css = {k:[v] if (isinstance(self.cssKeys[k], list) and isinstance(v, str)) else v for (k,v) in css.items()}
        new_css = {}
        reduced_css = {k:v for (k,v) in self.css.items() if v}
        for k,v in css.items():
            if k not in reduced_css:
                if k in self.cssKeys:
                    reduced_css[k] = v
                elif isinstance(v, str):
                    reduced_css['mixins'] = {**reduced_css['mixins'], **{k, v}}
            else:
                if isinstance(v, list):
                    try:
                        if isinstance(reduced_css[k], str):
                            reduced_css[k] = [reduced_css[k]]
                        reduced_css[k]+=v
                        reduced_css[k] = list(dict.fromkeys(reduced_css[k]))
                    except Exception as e:
                        print("Key: '{}'".format(k), "Current Value: '{}'".format(reduced_css[k]), "New Value: '{}'".format(v))
                        raise e
                elif k == "id":
                    if v:
                        reduced_css[k] = v
                elif k == "mixins":
                    reduced_css[k] = {**reduced_css[k], **v}

        return reduced_css

    def __iadd__(self, css):
        self.css = self.__add__(css)
        return self

    def append(self, child):
        self.children = self.children + [child]
        for child in self.children:
            child.parent = self

    def innerTxt(self, enricher=None):
        if self.children:
            return self.innerText + "\n".join([child.get_html(enricher) for child in self.children])
        return self.innerText

    def get_html(self, enricher=None):
        return HTMLRender.get_html(self, enricher)

    # Idea to allow user to set enricher to be passed on to parent
    # def get_parent(self):
    #     return self._parent
    #
    # def set_parent(self, obj):
    #     self._parent = obj
    #     if self.parent_enricher:
    #         self._parent.enricher += self.parent_enricher
    #
    # parent = property(get_parent, set_parent)



    # @property
    # def parent_class(self):
    #     return self._parent_class
    #
    # @parent_class.setter
    # def parent_class(self, x):
    #     if isinstance(x, str):
    #         self._parent_class = x
    #     else:
    #         raise Exception("Parent_class attribute must be string")

    # def copy(self, cls_elem, children=True):
    #     self.tag = cls_elem.tag
    #     self.css = cls_elem.css
    #     self.innerText = cls_elem.innerText
    #     if children: self.children = cls_elem.children
    #
    # def enrich(self, enricher):
    #     if isinstance(enricher, list):
    #         for c_enricher in enricher:
    #             self.children = [child.enrich(enricher) for child in self.children]
    #     else:
    #         self.children = [child.enrich(enricher) for child in self.children]
    #     return enricher(self)
class spanify:
    @classmethod
    def span(cls, elem_cls):
        if elem_cls.span:
            if "col" in str(elem_cls.span):
                col = HTMLObject(klass=elem_cls.span)
            else:
                col = HTMLObject(klass="col-{}".format(elem_cls.span))

            if elem_cls.parent:
                if not any(["col" in kls for kls in elem_cls.parent.klass]):
                    col.append(elem_cls)
                    return col
            else:
                col.append(elem_cls)
                return col
        return elem_cls

class HTMLRender:
    @classmethod
    def get_html(cls, elem_cls, enricher=None):
        return HTMLRender._html(spanify.span(elem_cls), enricher)

    @classmethod
    def _html(cls, elem_cls, enricher=None):
        # Idea to be able to pass enrichers to the class object
        # if elem_cls.enricher:
        #     if enricher:
        #         if isinstance(enricher, list):
        #             enricher += elem_cls.enricher
        #         else:
        #             enricher = [enricher] + elem_cls.enricher
        #     else:
        #         enricher = elem_cls.enricher

        attrs = ""
        elem_cls +=  {"style": [], "id": None, "class": [], "mixins":{}}


        if enricher:
            if isinstance(enricher, list):
                for c_enricher in enricher:
                    elem_cls = c_enricher(elem_cls)
            else:
                elem_cls = enricher(elem_cls)

        css = {k:v for k, v in elem_cls.css.items() if v}
        if css:
            for key, val in css.items():
                attr = val
                if isinstance(val, dict):
                    for mix, ins in val.items():
                        attrs+=" {}='{}'".format(mix, ins)
                    continue
                if isinstance(val, list):
                    attr = " ".join(val)
                attr = "'{}'".format(attr)
                attrs+=" {}={}".format(key, attr)

        prefix_tags = ["input", "br"]
        if elem_cls.tag.lower() in prefix_tags:
            return "{2}<{0}{1}>".format(elem_cls.tag, attrs, elem_cls.innerTxt(enricher))
        else:
            return "<{0}{1}>{2}</{0}>".format(elem_cls.tag, attrs, elem_cls.innerTxt(enricher))


# def spanify(layout_dict):
#     parent_div = HTMLObject()
#     for c_row in range(len(layout_dict)):
#         row_obj = HTMLObject(css={'class':['row']})
#         for elem in layout_dict[c_row]:
#             if elem.span:
#                 if isinstance(elem.span, list):
#                     col_width = elem.span
#                 elif "col" in str(elem.span):
#                     col_width = [elem.span]
#                 else:
#                     col_width = ["col-{}".format(elem.span)]
#             else:
#                 col_width = ["col"]
#             #col_width = "col-" + str(elem.span) if elem.span else "col"
#             col_obj = HTMLObject(css={'class':col_width})
#             col_obj.append(elem)
#             row_obj.append(col_obj)
#         parent_div.append(row_obj)
#
#     return parent_div
