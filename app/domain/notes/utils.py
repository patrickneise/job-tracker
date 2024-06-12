import markdown


def note_to_html(note):
    html = markdown.markdown(note)
    return html
