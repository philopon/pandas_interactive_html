import os
import html
import json
import base64
from io import BytesIO, StringIO

__all__ = ("InteractiveHtmlFormatter",)


def _convert_dtype(dtype):
    dtype = str(dtype)
    if dtype[:5] == "float" or dtype[:3] == "int":
        return "number"

    return "string"


def _bytes_to_data(b):
    return "data:image/png;base64," + base64.b64encode(b).decode()


def _pil_to_data(pil):
    tmp = BytesIO()
    pil.save(tmp, "PNG")
    return _bytes_to_data(tmp.getvalue())


def _iintercalate(it, c):
    it = iter(it)
    before = next(it)
    for chunk in it:
        yield before + c
        before = chunk

    yield before


class InteractiveHtmlFormatter(object):
    def __init__(self, obj, path_or_buf=None, index=True,
                 image_columns=None, converter=None, mode="w",
                 chunk_size=4096,
                 title="pandas_interactive_html"):
        r"""Interactive html formatter of pandas DataFrame.

        Parameters:
            obj(DataFrame): input data frame
            path_or_buf: output
            index(bool): include index or not
            image_columns(set): columns render as image
            converter(dict[str,function]): convert cell value function on specific column
            mode: file mode when opening file
            chunk_size(int): chunk size when reading asset file
            title(str): page title

        """
        self.path_or_buf = path_or_buf

        if path_or_buf is None:
            self.output = StringIO()
        elif isinstance(path_or_buf, str):
            self.output = open(path_or_buf, mode)
        else:
            self.output = path_or_buf

        self.obj = obj
        self.image_columns = image_columns or set()
        self.converter = converter or {}
        self.index = index
        self.title = title
        self.chunk_size = chunk_size

    def _header(self, name, dtype):
        return {
            "name": str(name),
            "type": "image" if name in self.image_columns else _convert_dtype(dtype),
        }

    def _columns(self):
        return [
            self._header(name, dtype)
            for name, dtype in self.obj.dtypes.iteritems()  # noqa: B301
        ]

    def _index(self):
        return self._header(self.obj.index.name or "", self.obj.index.dtype)

    def _cell(self, value, sdtype, column_name):
        converter = self.converter.get(column_name)
        if converter is not None:
            value = converter(value)

        if sdtype == "number":
            return float(value)
        elif sdtype == "string":
            return str(value)
        elif sdtype == "image":
            if hasattr(value, "_repr_png_"):
                return _bytes_to_data(value._repr_png_())
            else:
                raise ValueError("cannot render {!r} as png".format(value))

    def _iterdata(self, index, columns):
        for idx, series in self.obj.iterrows():
            row = []

            if index:
                row.append(self._cell(idx, index["type"], index["name"]))

            for value, column in zip(series, columns):
                row.append(self._cell(value, column["type"], column["name"]))

            yield row

    def save(self):
        """Save html."""
        self.output.write(
            "<!doctype html>\n"
            "<html>"
            "<head>"
            "<meta charset=\"utf-8\" />"
            "<title>",
        )
        self.output.write(html.escape(self.title))
        self.output.write(
            "</title>"
            "</head>"
            "<body>"
            "<div class=\"mount-point\"/>"
            "<script type=\"application/json\" class=\"table-columns\">",
        )

        out_columns = columns = self._columns()
        if self.index:
            index = self._index()
            out_columns = [index] + out_columns
        else:
            index = None
        self.output.write(json.dumps(out_columns).replace("/", r"\/"))

        self.output.write(
            "</script>"
            "<script type=\"application/json\" class=\"table-data\">[",
        )

        for row in _iintercalate((json.dumps(row) for row in self._iterdata(index, columns)), ","):
            self.output.write(row.replace("/", r"\/"))

        self.output.write(
            "]</script>"
            "<script type=\"text/javascript\">",
        )

        with open(os.path.join(os.path.dirname(__file__), "bundle.js")) as js:
            while True:
                chunk = js.read(self.chunk_size)
                if len(chunk) == 0:
                    break
                self.output.write(chunk)

        self.output.write(
            "</script>"
            "</body>"
            "</html>",
        )

        if self.path_or_buf is None:
            value = self.output.getvalue()
            self.output.close()
            return value
