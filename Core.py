class HTMLObject:
    def __init__(self, tag = "div", css = {"style": [], "id": None, "class": [], "mixins":{}}, innerText = "", children= [], span=None, **kwargs):
        self.kwargs = kwargs
        self.tag = tag
        self.css = css
        cssKeys = ["style", "id", "klass", "mixins"]
        self +=  {"style": [], "id": None, "class": [], "mixins":{}}
        self += {k.replace("klass", "class"):v for (k, v) in kwargs.items() if k in cssKeys}
        self += {"mixins":{k:v for (k,v) in kwargs.items() if k not in cssKeys}}
        self.innerText = innerText
        self.children = children
        if self.children:
            for child in self.children:
                child.parent = self

        self.parent = None
        # self.parent_enricher = []
        # self.enricher = []
        self.span = span

    def __add__(self, css):
        new_css = {}
        reduced_css = {k:v for (k,v) in self.css.items() if v}
        for k,v in css.items():
            if k not in reduced_css:
                reduced_css[k] = v
            else:
                if isinstance(v, list):
                    try:
                        if isinstance(reduced_css[k], str):
                            reduced_css[k] = [reduced_css[k]]
                        reduced_css[k]+=v
                        reduced_css[k] = list(set(reduced_css[k]))
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


class HTMLRender:
    @classmethod
    def get_html(cls, elem_cls, enricher=None):

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


def spanify(layout_dict):
    parent_div = HTMLObject()
    for c_row in range(len(layout_dict)):
        row_obj = HTMLObject(css={'class':['row']})
        for elem in layout_dict[c_row]:
            if elem.span:
                if isinstance(elem.span, list):
                    col_width = elem.span
                elif "col" in str(elem.span):
                    col_width = [elem.span]
                else:
                    col_width = ["col-{}".format(elem.span)]
            else:
                col_width = ["col"]
            #col_width = "col-" + str(elem.span) if elem.span else "col"
            col_obj = HTMLObject(css={'class':col_width})
            col_obj.append(elem)
            row_obj.append(col_obj)
        parent_div.append(row_obj)

    return parent_div
