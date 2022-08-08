from ssl import SSL_ERROR_SSL
import dash
import dash_bootstrap_components as dbc
from dash import html
from datetime import datetime, date
from dateutil import relativedelta
from ui.get_icon import get_icon
from common.string_aggregate import get_list_for_display

################################################################################
# 04.  UI / UX
################################################################################
'''
+---- 4 / 2 ---+  +------------- 8 / 10 --------------+
| +----------+ |  | +-----------------------------+ ^ |
| |          | |  | |             exp 1           | | |
| |  Profile | |  | +-----------------------------+ | |
| |          | |  | +-----------------------------+ | |
| +----------+ |  | |             exp 2           | | | 
| +----------+ |  | +-----------------------------+ | |
| |          | |  | +-----------------------------+ | |
| |   Tech   | |  | |             exp 3           | | |
| |   Stack  | |  | +-----------------------------+ | |
| |          | |  | +-----------------------------+ | |
| |          | |  | |             exp 4           | | |
| +----------+ |  | +-----------------------------+ v |
+---- 4 / 2 ---+  +------------- 8 / 10 --------------+
'''

def get_layout(
    title = 'Resume',
    data = None,
    tech_stack = None
    ):

    if data is None:
        return [dbc.Card([dbc.CardHeader('data.json is blank')])]
    
    # top tech stack 
    top_tech_stack = data["top tech stack"]
    
    # Profile
    ui_profile = html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H4(
                                data["personal detail"]["full name"],
                                className = "card-title",
                                style = {'display': 'inline-block'}
                            ),
                            html.H6(
                                [
                                    '(',
                                    data["personal detail"]["pronouns"],
                                    ')'
                                ],
                                className = "text-muted",
                                style = {'display': 'inline-block', 'padding': '4px'}
                            ),

                            # social media clickable icon
                            get_icon(
                                icons_class_name = "bi bi-linkedin",
                                url = data["personal detail"]["linkedin url"]
                            ),
                            get_icon(
                                icons_class_name = "bi bi-github",
                                url = data["personal detail"]["github url"]
                            )
                        ]
                    ),        

                    dbc.CardBody(
                        [
                            # phone
                            get_icon(
                                icons_class_name = "bi bi-telephone-fill"
                            ),
                            data["personal detail"]["phone"],
                            html.Hr(),

                            # email
                            get_icon(
                                icons_class_name = "bi bi-envelope-fill"
                            ),
                            data["personal detail"]["email"],
                        ],
                        className = "align-items-center"
                    ),
                ],
                style = {'margin-top': '10px'},
                className = "bg-light",
            )
        ]
    )
    
    # tech stack
    ui_tech_stack = html.Div(
        [
            dbc.Alert(
                [
                    get_icon(
                        icons_class_name = "bi bi-info-circle-fill me-2"
                    ),
                    "Try filtering experiences by Tech Stack",
                ],
                color = "light",
                style = {'margin-top': '10px'},
                className = "d-flex align-items-center",
            ),

            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.H4(
                                "Tech Stack",
                                className = "card-title",
                                style = {'display': 'inline-block', 'margin-right': '20px'}
                            ),
                            dbc.Button(
                                "Select All",
                                outline = True,
                                color = "secondary",
                                className = "me-1",
                                style = {'display': 'inline-block', 'margin-left': '4px', 'text-align': 'right'},
                                id = 'dbc-bt-tech-stack-select-all'
                            ),
                            dbc.Button(
                                "Deselect All",
                                outline = True,
                                color = "secondary",
                                className = "me-1",
                                style = {'display': 'inline-block', 'margin-left': '4px', 'text-align': 'right'},
                                id = 'dbc-bt-tech-stack-deselect-all'
                            )
                        ]
                    ),        

                    dbc.CardBody(
                        [
                            dbc.Checklist(
                                options = [
                                    # putting the tech-stacks in the TOP_TECH_STACK at the top
                                    *[
                                        {"label": k, "value": k, "label_id": 'dbc-cl-tech-stack-' + k}
                                        for k, _ in tech_stack.items() if k in top_tech_stack
                                    ],
                                    *[
                                        {"label": k, "value": k, "label_id": 'dbc-cl-tech-stack-' + k}
                                        for k, _ in tech_stack.items() if k not in top_tech_stack
                                    ]
                                ],
                                value = [k for k, _ in tech_stack.items()],
                                id = 'dbc-cl-tech-stack'
                            )
                        ],
                        style = {'column-count': '2'},
                        className = "align-items-center"
                    ),
                ],
                style = {'margin-top': '10px'},
                className = "bg-light",
            ),
            *[
                dbc.Tooltip(
                    get_list_for_display(v),
                    target = 'dbc-cl-tech-stack-' + k
                ) for k, v in tech_stack.items() if v
            ]
        ]
    )

    # main deck - experience
    def get_experience_layout(data_exp, id_suffix = None):
        if id_suffix is None:
            return html.Div()

        # Accordion title - start/end date
        job_start_date_time = datetime.strptime(data_exp["start date"], "%Y-%m-%d")
        job_start_date = job_start_date_time.strftime("%b %Y")

        job_end_date = 'Present'           # default value if end_date is blank
        job_end_date_time = date.today()    # default value if end_date is blank
        if "end date" in data_exp:
            if data_exp["end date"]:
                job_end_date_time = datetime.strptime(data_exp["end date"], "%Y-%m-%d")
                job_end_date = job_end_date_time.strftime("%b %Y")
        

        # Accordion title - job period
        job_period_time_delta = relativedelta.relativedelta(job_end_date_time, job_start_date_time)
        job_y, job_m = "", ""
        if job_period_time_delta.years:
            if job_period_time_delta.years == 1:
                job_y = str(job_period_time_delta.years) + ' yr '
            else:
                job_y = str(job_period_time_delta.years) + ' yrs '
        if job_period_time_delta.months:
            if job_period_time_delta.months == 1:
                job_m = str(job_period_time_delta.months) + ' mo'
            else:
                job_m = str(job_period_time_delta.months) + ' mos'
        job_period = job_start_date + ' \u2014 ' + job_end_date + ' \u2022 ' + job_y + job_m


        # Job title and company
        full_job_title = str(data_exp["position"]) + " \u2014 " + str(data_exp["company"])
        

        # Tech Stack in each experience
        exp_tech_stack = html.Div()

        if "tech stack" in data_exp:
            if data_exp["tech stack"]:
                exp_tech_stack = html.Div(
                    [
                        html.H5(
                            [
                                "Tech Stack: ",
                                *[
                                    dbc.Badge(
                                        str(k),
                                        id = {
                                            "id": f"dbc-bd-exp-tech-stack-{id_suffix}-{k}",
                                            "type": "tech-stack",
                                            "tech_stack": str(k)
                                        },
                                        color = "primary",
                                        className = "ms-1",
                                        style = {'margin-left': '4px'}
                                    ) for k, _ in data_exp["tech stack"].items()
                                ]
                            ]
                        ),
                        *[
                            dbc.Tooltip(
                                get_list_for_display(v),
                                placement = "bottom",
                                target = {
                                    "id": f"dbc-bd-exp-tech-stack-{id_suffix}-{k}",
                                    "type": "tech-stack",
                                    "tech_stack": str(k)
                                }
                            ) for k, v in data_exp["tech stack"].items() if v
                        ],
                        html.Hr()
                    ]
                )
        

        # Highlight
        highlight = html.Div()
        
        if "highlight" in data_exp:
            if data_exp["highlight"]:
                highlight = html.Div(
                    [
                        html.H5("Highlight: " + data_exp["highlight"]),
                        html.Hr()
                    ]
                )
        

        # position history
        def display_history_pos(pos, pos_eff_date):
            d = datetime.strptime(pos_eff_date, "%Y-%m-%d")
            return 'Position: ' + pos + ' (effective from ' + d.strftime("%B %Y") +')'

        pos_hst = html.Div()

        if "position history" in data_exp:
            if data_exp["position history"]:
                pos_hst = html.Div(
                    [
                        html.H6(display_history_pos(data_exp["position"], data_exp["position effective date"])),
                        *[html.H6(display_history_pos(h["position"], h["position effective date"])) for h in data_exp["position history"]],
                        html.Hr()
                    ]
                )


        return dbc.AccordionItem(
            [
                html.H4(full_job_title),
                html.H6(
                    ['Location: ' + data_exp["location"]],
                    className = "text-muted"
                ),
                html.Hr(),
                exp_tech_stack,
                highlight,
                pos_hst,
                *[html.H6('\u2022 ' + d) for d in data_exp["details"]],
            ],
            item_id = "dbc-ad-main-deck-" + id_suffix,
            title = job_period
        )

    ui_experience = html.Div(
        [
            dbc.Accordion(
                [get_experience_layout(data["experience"][e], id_suffix = e) for e, _ in data["experience"].items()],
                id = "dbc-ad-main-deck",
                start_collapsed = False,
                always_open = True
            )
        ],
        style = {'padding-top': '10px'}
    )

    # full layout
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            ui_profile,
                            ui_tech_stack
                        ],
                        xs = 12, sm = 5, md = 5, lg = 4      # wider for the smaller screen
                    ),
                    dbc.Col(
                        ui_experience,
                        xs = 12, sm = 7, md = 7, lg = 8     # wider for the smaller screen
                    ),
                ]
            ),
        ],
        fluid = True,
    )
