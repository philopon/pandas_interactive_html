from .formatter import InteractiveHtmlFormatter

__all__ = ("register",)


def _to_interactive_html(
    self, path_or_buf=None, index=True, image_columns=None, converter=None,
        mode="w", chunk_size=4096, title="pandas_interactive_html"):

    fmt = InteractiveHtmlFormatter(
        self, path_or_buf=path_or_buf, index=index, image_columns=image_columns,
        converter=converter, mode=mode, chunk_size=chunk_size, title=title,
    )
    return fmt.save()


def register():
    import pandas
    pandas.DataFrame.to_interactive_html = _to_interactive_html
