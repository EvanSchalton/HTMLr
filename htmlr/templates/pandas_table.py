import pandas as pd
from .core import HTMLObject, HTMLRender

def enricher(elem_cls):

    if isinstance(elem_cls, Table):
        elem_cls += {"class":["table", "sortable-table", "table-striped", "table-bordered"]}

    elif isinstance(elem_cls, TableRow):
        if elem_cls.kwargs["table_type"] == "thead":
            elem_cls += {"class":["table-header"]}

        if elem_cls.kwargs["table_type"] == "tbody":
            elem_cls += {"class":["table-row"]}
            if elem_cls.kwargs["row_num"] % 2 == 0:
                elem_cls += {"class":["even"]}
            else:
                elem_cls += {"class":["odd"]}

    elif isinstance(elem_cls, TableCell):
        if elem_cls.kwargs["table_type"] == "thead":
            #elem_cls += {"mixins":{"scope":"col"}}
            elem_cls += {"class":["table-col"]}
        else:
            if elem_cls.kwargs["col_num"] == 0:
                elem_cls.tag = "th"
                #elem_cls += {"mixins":{"scope":"row"}}
                #elem_cls += {"class":["row"]}

    return elem_cls

class pdTable(HTMLObject):
    # css = {"style": [], "id": None, "class": [], "mixins":{}}
    # tag = "table"
    # innerText = ""
    # parent=None

    def __init__(self, dataframe, table_id=None, index_name = "No."):
        super(Table, self).__init__(self, tag = "table")
        self.kwargs = {"header":True, "index":True, "table_id":table_id, "index_name":index_name}

        self.children = []
        if table_id: self.css["id"] = table_id
        self.dataframe = dataframe

        self.kwargs["column_to_index"] = {i:index+1 for index, i in enumerate(dataframe.columns)}
        self.kwargs["column_to_index"][index_name] = 0
        self.kwargs["index_to_column"] = {v:k for (k, v) in self.kwargs["column_to_index"].items()}

        # Build Head
        self.children = [TableHB(dataframe.columns, self.kwargs)]

        # Build Body
        self.children.append(TableHB(dataframe.values.tolist(), self.kwargs))

    def innerTxt(self, enricher=None):
        return "\n".join([HTMLRender.get_html(c_comp, enricher) for c_comp in self.children])

    def get_html(self, enricher=None):
        return HTMLRender.get_html(self, enricher)

class TableHB(HTMLObject):
    # css = {"style": [], "id": None, "class": [], "mixins":{}}
    # innerText = ""
    # parent=None

    def __init__(self, lst, kwargs):
        super(TableHB, self).__init__(self, tag = "tbody" if all([isinstance(i, list) for i in lst]) else "thead")
        self.kwargs = kwargs.copy()
        self.kwargs["table_type"] = self.tag
        #if index, element in enumerate(lst):
        if self.tag == "thead": lst = [lst]
        self.children = [TableRow(index, c_lst, self.kwargs) for index, c_lst in enumerate(lst)]

    def innerTxt(self, enricher=None):
        return "\n".join([HTMLRender.get_html(c_row, enricher) for c_row in self.children])

class TableRow(HTMLObject):
    # css = {"style": [], "id": None, "class": [], "mixins":{}}
    # tag = "tr"
    # innerText = ""
    # parent=None

    def __init__(self, row_num, lst, kwargs):
        super(TableRow, self).__init__(self, tag = "tr")
        self.kwargs = kwargs.copy()
        self.kwargs["row_num"] = row_num
        if isinstance(lst, str): lst = [lst]
        self.row_num = row_num
        if kwargs["table_type"]== "thead":
            self.children = [TableCell(col_num=0, innerText=self.kwargs["index_name"], kwargs=self.kwargs)]
        else:
            self.children = [TableCell(col_num=0, innerText=row_num, kwargs=self.kwargs)]
        self.children += [TableCell(col_num+1, cell_value, self.kwargs) for col_num, cell_value in enumerate(lst)]

    def innerTxt(self, enricher=None):
        return "\n".join([HTMLRender.get_html(c_cell, enricher) for c_cell in self.children])

class TableCell(HTMLObject):
    # css = {"style": [], "id": None, "class": [], "mixins":{}}
    # children = []
    # parent=None
    def __init__(self, col_num, innerText, kwargs):
        super(TableCell, self).__init__(self, tag = "td" if kwargs["table_type"] == "tbody" else "th")
        self.kwargs = kwargs.copy()
        self.kwargs["col_num"] = col_num
        self.innerText = innerText
        self.kwargs["innerText"] = innerText
        self += {"class": ["field:{}".format(self.kwargs["index_to_column"][col_num])]}

    def innerTxt(self, enricher=None):
        if self.children:
            return str(self.innerText) + "\n".join([child.get_html(enricher) for child in self.children])
        return self.innerText
