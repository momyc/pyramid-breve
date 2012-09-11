inherits ('my_app:templates/layout.b') [
    override ('content') [
        div (class_='alert alert-success') [
            'Welcome to', E.nbsp, project, E.nbsp, 'project!',
        ],
    ],
]
