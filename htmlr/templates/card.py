from HTMLr.core import HTMLObject

class Card(HTMLObject):
    def __init__(self, header=None, body=None, footer=None):
        super(Card, self).__init__(klass = "card")
        if header:
            self.header = header
        else:
            self.header = HTMLObject(klass="card-header")

        if body:
            self.body = body
        else:
            self.body = HTMLObject(klass="card-body")

        if footer:
            self.footer = footer
        else:
            self.footer = HTMLObject(klass="card-footer")

        self.children = [self.header, self.body, self.footer]
