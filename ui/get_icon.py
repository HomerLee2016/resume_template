from dash import html

def get_icon(
    icons_class_name,
    url = None
):
    style = {
        'color': 'black',
        'margin': '4px',
        'font-size': '20px'
    }

    if url:
        return html.A(
            html.I(
                className = icons_class_name,
                style = style
            ),
            href = url
        )
    
    else:
        return html.A(
            html.I(
                className = icons_class_name,
                style = style
            )
        )