class Tag:
    def __init__(self, tag, klass=None, is_single=False, **other_attrs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, val in other_attrs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = val

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs=[]
        for attr, val in self.attributes.items():
            attrs.append('%s="%s"' % (attr, val))
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            opening = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "\n</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>\n{text}\n</{tag}>\n".format(tag=self.tag, attrs=attrs, text=self.text)

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        html_code = "<%s>\n" % self.tag
        for child in self.children:
            html_code += str(child)
        html_code += "</%s>\n" % self.tag
        return html_code

class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w", encoding="utf-8") as f:
                f.write(str(self))
        else:
            print(self)
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        html_code = "<html>\n"
        for child in self.children:
            html_code += str(child)
        html_code += "</html>"
        return html_code

with HTML(output=None) as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png") as img:
                div += img

            body += div

        doc += body