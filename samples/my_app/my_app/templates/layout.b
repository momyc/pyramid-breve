html [
    head [
        title ['My beautiful site'],
        link (rel='stylesheet', type_='text/css', media='screen', href=request.static_path('my_app:static/my_app.css')),
    ],
    body [
        div (id_='container') [
            div (id_='navigation') [
                slot ('navigation'),
            ],
            div (id_='content') [
                slot ('content'),
            ],
            div (id_='side-menu') [
                slot ('side-menu'),
            ],
        ],
    ],
]
