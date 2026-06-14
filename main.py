import os
import flet as ft
import flet.canvas as cv
import subprocess

# ── SHARED CONSTANTS ──────────────────────────────────────────────────────────
ACCENT_COLOR   = "#7A2D5F"
DIVIDER_COLOR  = "#C86B93"
IC_BADGE       = "#1F9FB3"
IC_BOOK        = "#7A2D5F"
IC_GROUPS      = "#2D8C73"
IC_EMAIL       = "#B23A5B"
IC_PHONE       = "#2D8C73"
IC_INSTA       = "#C8568A"
TEXT_COLOR     = "#261626"
SUBTLE_COLOR   = ft.Colors.with_opacity(0.72, TEXT_COLOR)
BG_COLOR       = "#F8C5DD"
DEMO_VIDEO_SRC = "project_demo.mp4"

HEADER_SIZE    = 28
SUBHEADER_SIZE = 20
CONTENT_SIZE   = 14

# ── CONSTELLATION BACKGROUND (built ONCE, reused every page) ──────────────────
def _build_background_shapes():
    branch_paint = ft.Paint(
        color=ft.Colors.with_opacity(0.72, "#3D1828"),
        stroke_width=2.2,
    )
    twig_paint = ft.Paint(
        color=ft.Colors.with_opacity(0.50, "#5C2438"),
        stroke_width=1.15,
    )
    bloom_paint = ft.Paint(
        color=ft.Colors.with_opacity(0.55, "#D87EA6"),
        style=ft.PaintingStyle.FILL,
    )
    shapes = [
        cv.Line(x1=380, y1=0, x2=270, y2=90, paint=branch_paint),
        cv.Line(x1=270, y1=90, x2=330, y2=172, paint=branch_paint),
        cv.Line(x1=270, y1=90, x2=185, y2=150, paint=branch_paint),
        cv.Line(x1=330, y1=172, x2=410, y2=220, paint=twig_paint),
        cv.Line(x1=330, y1=172, x2=280, y2=280, paint=twig_paint),
        cv.Line(x1=185, y1=150, x2=118, y2=230, paint=twig_paint),
        cv.Line(x1=1280, y1=0, x2=920, y2=170, paint=branch_paint),
        cv.Line(x1=920, y1=170, x2=1120, y2=330, paint=branch_paint),
        cv.Line(x1=920, y1=170, x2=700, y2=280, paint=branch_paint),
        cv.Line(x1=1120, y1=330, x2=1410, y2=430, paint=branch_paint),
        cv.Line(x1=1120, y1=330, x2=960, y2=520, paint=branch_paint),
        cv.Line(x1=700, y1=280, x2=520, y2=420, paint=twig_paint),
        cv.Line(x1=700, y1=280, x2=620, y2=115, paint=twig_paint),
        cv.Line(x1=960, y1=520, x2=870, y2=690, paint=twig_paint),
        cv.Line(x1=960, y1=520, x2=1190, y2=640, paint=twig_paint),
        cv.Line(x1=1410, y1=430, x2=1660, y2=560, paint=twig_paint),
        cv.Line(x1=1410, y1=430, x2=1540, y2=245, paint=twig_paint),
    ]

    blooms = [
        (118, 230), (186, 150), (278, 92), (330, 172), (282, 280),
        (624, 116), (540, 410), (702, 276), (860, 688), (1192, 640),
        (1540, 246), (1660, 560), (1136, 336), (1010, 500), (760, 250),
    ]
    for x_pos, y_pos in blooms:
        shapes.append(cv.Circle(x=x_pos, y=y_pos, radius=5, paint=bloom_paint))
        shapes.append(cv.Circle(x=x_pos + 8, y=y_pos + 4, radius=3, paint=bloom_paint))
        shapes.append(cv.Circle(x=x_pos - 7, y=y_pos + 6, radius=3, paint=bloom_paint))

    return shapes

# Pre-compute once at import time — all pages share this
_BG_SHAPES = _build_background_shapes()


def build_background():
    return ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-0.9, -1.0),
                    end=ft.Alignment(0.8, 1.0),
                    colors=["#7ED7DE", "#D9C9EC", "#F9B8D4", "#F47FB5"],
                ),
            ),
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.22, "#FFF7FB"),
            ),
            cv.Canvas(expand=True, shapes=_BG_SHAPES),
        ],
        expand=True,
    )


# ── TOP NAV ───────────────────────────────────────────────────────────────────
def build_top_nav(page: ft.Page, active_key: str):
    def go(route):
        def handler(e):
            page.go(route)
        return handler

    def nav_button(label, icon, route):
        is_active = active_key == route.strip("/")
        return ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(icon, size=15,
                            color=TEXT_COLOR if is_active else ACCENT_COLOR),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_500,
                            color=TEXT_COLOR if is_active else ACCENT_COLOR),
                ],
                spacing=5,
                tight=True,
            ),
            on_click=go(route),
            style=ft.ButtonStyle(
                padding=ft.Padding(10, 6, 10, 6),
                bgcolor=ft.Colors.with_opacity(0.12, ACCENT_COLOR) if is_active
                        else ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.with_opacity(0.08, ACCENT_COLOR),
            ),
        )

    return ft.Container(
        bgcolor=ft.Colors.with_opacity(0.84, "#FFF7FB"),
        # ── taller navbar ──
        padding=ft.Padding(20, 14, 20, 14),
        border=ft.border.Border(
            bottom=ft.border.BorderSide(1, ft.Colors.with_opacity(0.22, ACCENT_COLOR))
        ),
        content=ft.Row(
            controls=[
                # ── UNAM logo replacing text ──
                ft.TextButton(
                    content=ft.Row([
                        ft.Image(
                            src="unam_logo.png",
                            width=70, height=70,
                            fit=ft.BoxFit.CONTAIN,
                            error_content=ft.Text(
                                "UNAM", size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ACCENT_COLOR,
                            ),
                        ),
                        ft.Column([
                            ft.Text("Anna NN Kambala", size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_COLOR),
                            ft.Text("Computer Programming I · 2026",
                                    size=10, color=SUBTLE_COLOR),
                        ], spacing=1, tight=True),
                    ], spacing=10, tight=True),
                    on_click=go("/home"),
                    style=ft.ButtonStyle(overlay_color=ft.Colors.TRANSPARENT),
                ),
                ft.Row(
                    controls=[
                        nav_button("Home",       ft.Icons.HOME,        "/home"),
                        nav_button("Timeline",   ft.Icons.TIMELINE,    "/timeline"),
                        nav_button("GitHub",     ft.Icons.CODE,        "/github"),
                        nav_button("MATLAB Hub", ft.Icons.SCHOOL,      "/matlab"),
                        nav_button("Demos",      ft.Icons.PLAY_CIRCLE, "/demos"),
                        nav_button("Blog",       ft.Icons.ARTICLE,     "/blog"),
                        nav_button("Contact",    ft.Icons.MAIL,        "/contact"),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.END,
                    wrap=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


# ── FULL-PAGE SHELL ───────────────────────────────────────────────────────────
def page_shell(page: ft.Page, active_key: str, body: ft.Control):
    nav = build_top_nav(page, active_key)
    scrollable = ft.Column(
        controls=[
            ft.Container(content=body, padding=ft.Padding(30, 30, 30, 40), expand=True)
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
    page_col = ft.Column(
        controls=[nav, scrollable],
        expand=True,
        spacing=0,
    )
    return ft.Stack(
        controls=[build_background(), page_col],
        expand=True,
    )


# ── HELPER WIDGETS ────────────────────────────────────────────────────────────
def math_module_card(title, description, top_formula,
                     bottom_formula=None, plain_suffix=""):
    formula_controls = []
    if bottom_formula:
        formula_controls += [
            ft.Text(top_formula, size=14, color=ACCENT_COLOR,
                    weight=ft.FontWeight.BOLD),
            ft.Container(width=160, height=1, bgcolor=DIVIDER_COLOR,
                         margin=ft.Margin(top=2, bottom=2)),
            ft.Text(bottom_formula, size=14, color=ACCENT_COLOR,
                    weight=ft.FontWeight.BOLD),
        ]
    else:
        formula_controls.append(
            ft.Text(top_formula, size=14, color=ACCENT_COLOR, italic=True)
        )
    if plain_suffix:
        formula_controls.append(
            ft.Text(plain_suffix, size=12, color=SUBTLE_COLOR)
        )

    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
            ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
            ft.Container(
                content=ft.Column(
                    formula_controls,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=12,
                bgcolor=ft.Colors.with_opacity(0.50, "#FFF7FB"),
                border=ft.Border.all(1, ft.Colors.with_opacity(0.18, ACCENT_COLOR)),
                border_radius=6,
            ),
        ], spacing=10),
        padding=20,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.18, ACCENT_COLOR)),
        border_radius=10,
        col={"sm": 12, "md": 6, "lg": 4},
    )


def blog_post_preview(title, description):
    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=SUBHEADER_SIZE,
                    weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
            ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
            ft.TextButton("Read full post…",
                          style=ft.ButtonStyle(color=ACCENT_COLOR)),
        ], spacing=5),
        margin=ft.Margin(bottom=20),
        padding=15,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.18, ACCENT_COLOR)),
        border_radius=10,
    )


def cert_card(img_path):
    return ft.Container(
        content=ft.Image(src=img_path, border_radius=10, fit=ft.BoxFit.COVER),
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10,
                            color=ft.Colors.with_opacity(0.26, ft.Colors.BLACK)),
        col={"sm": 12, "md": 6},
    )


def skill_chip(label, icon, color):
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, size=16, color=color),
            ft.Text(label, size=13, color=TEXT_COLOR,
                    weight=ft.FontWeight.W_500),
        ], spacing=6, tight=True),
        padding=ft.Padding(12, 8, 12, 8),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.25, color)),
        border_radius=20,
        bgcolor=ft.Colors.with_opacity(0.18, color),
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE BODIES
# ══════════════════════════════════════════════════════════════════════════════

# ── HOME ──────────────────────────────────────────────────────────────────────
def home_body():
    profile_section = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 12, "md": 5},
                content=ft.Container(
                    width=280, height=340,
                    border_radius=20,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.35, ACCENT_COLOR)),
                    padding=10,
                    content=ft.Image(src="anna.jpeg", fit=ft.BoxFit.COVER,
                                     border_radius=14),
                ),
            ),
            ft.Container(
                col={"sm": 12, "md": 7},
                padding=ft.Padding(left=15, right=15, top=10, bottom=10),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Column(spacing=4, controls=[
                            ft.Text("Anna NN Kambala", size=36,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_COLOR),
                            ft.Text("Mining Engineering Student | Documentation Lead",
                                    size=16, color=ACCENT_COLOR,
                                    weight=ft.FontWeight.W_500),
                        ]),
                        ft.Divider(color=DIVIDER_COLOR, height=10, thickness=1),
                        ft.Column(spacing=8, controls=[
                            ft.Text("Project Brief", size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_COLOR),
                            ft.Text(
                                "Serving as the Documentation Lead for Group 1 in the "
                                "Computer Programming I project, I organize and refine "
                                "the SRS documentation for EM-Lab, our metallurgical "
                                "laboratory management app built using Expo, React Native, "
                                "and Firebase.",
                                size=15, color=SUBTLE_COLOR,
                            ),
                        ]),
                        ft.Column(spacing=5, controls=[
                            ft.Row([
                                ft.Icon(ft.Icons.BADGE, color=IC_BADGE, size=16),
                                ft.Text("Student Number: 225054310",
                                        size=14, color=SUBTLE_COLOR),
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.BOOK_ROUNDED, color=IC_BOOK, size=16),
                                ft.Text("Module: Computer Programming I",
                                        size=14, color=SUBTLE_COLOR),
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.GROUPS_3, color=IC_GROUPS, size=16),
                                ft.Text("Assigned Team: Group 1 (EM-Lab)",
                                        size=14, color=SUBTLE_COLOR),
                            ]),
                        ]),
                    ],
                ),
            ),
            
        ],
        spacing=30,
        run_spacing=30,
    )

    # ── SKILLS & TECH SECTION (the area indicated in the image) ──
    skills_section = ft.Container(
        margin=ft.Margin(top=40, bottom=0, left=0, right=0),
        content=ft.Column([
            ft.Row([
                ft.Container(
                    width=4, height=30, bgcolor=ACCENT_COLOR,
                    border_radius=2,
                    margin=ft.Margin(right=12, top=0, left=0, bottom=0),
                ),
                ft.Text("Skills & Technologies",
                        size=SUBHEADER_SIZE + 2,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_COLOR),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=6),
            ft.Text(
                "A snapshot of the tools, frameworks, and languages I apply across "
                "the EM-Lab project and my academic coursework at UNAM.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            ft.Container(height=18),

            # Row 1 — Languages
            ft.Text("Languages", size=13, color=ACCENT_COLOR,
                    weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
                skill_chip("Python",      ft.Icons.CODE,            "#5BC8F5"),
                skill_chip("JavaScript",  ft.Icons.JAVASCRIPT,      "#FACC15"),
                skill_chip("JSX / React", ft.Icons.WIDGETS,         "#A78BFA"),
                skill_chip("MATLAB",      ft.Icons.CALCULATE,       "#4ADE80"),
            ]),
            ft.Container(height=16),

            # Row 2 — Frameworks & Tools
            ft.Text("Frameworks & Tools", size=13, color=ACCENT_COLOR,
                    weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
                skill_chip("Flet",          ft.Icons.DESKTOP_WINDOWS, "#5BC8F5"),
                skill_chip("React Native",  ft.Icons.PHONE_ANDROID,   "#F472B6"),
                skill_chip("Expo",          ft.Icons.ROCKET_LAUNCH,   "#FB923C"),
                skill_chip("Firebase",      ft.Icons.LOCAL_FIRE_DEPARTMENT, "#FACC15"),
                skill_chip("AsyncStorage",  ft.Icons.CLOUD_SYNC,      "#34D399"),
                skill_chip("Git & GitHub",  ft.Icons.MERGE_TYPE,      "#F87171"),
            ]),
            ft.Container(height=16),

            # Row 3 — Engineering domains
            ft.Text("Engineering Domains", size=13, color=ACCENT_COLOR,
                    weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
                skill_chip("Mining Engineering",       ft.Icons.DOMAIN,          "#A78BFA"),
                skill_chip("Lab Sample Tracking",      ft.Icons.SCIENCE,         "#4ADE80"),
                skill_chip("NoSQL / Firestore",        ft.Icons.STORAGE,         "#5BC8F5"),
                skill_chip("System Architecture",      ft.Icons.ACCOUNT_TREE,    "#FB923C"),
                skill_chip("Cross-Platform Dev",       ft.Icons.DEVICES,         "#F472B6"),
            ]),

            ft.Container(height=30),
            ft.Divider(color=DIVIDER_COLOR, thickness=1),

            # Quick-stats bar
            ft.Container(height=10),
            ft.ResponsiveRow(
                controls=[
                    _stat_card("8",   "MATLAB Courses",   ft.Icons.SCHOOL,           "#4ADE80"),
                    _stat_card("15%", "CA Weighting",     ft.Icons.GRADE,            "#FACC15"),
                    _stat_card("16",  "Team Members",     ft.Icons.GROUPS_3,         "#F472B6"),
                    _stat_card("5",   "Sprint Phases",    ft.Icons.TIMELINE,         "#5BC8F5"),
                ],
                spacing=15, run_spacing=15,
            ),
        ]),
        padding=ft.Padding(30, 28, 30, 28),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.20, ACCENT_COLOR)),
        border_radius=14,
        bgcolor=ft.Colors.with_opacity(0.56, "#FFF7FB"),
    )

    return ft.Column(
        expand=True,
        controls=[
            profile_section, 
            skills_section,
            ft.Container(expand=True),
            ft.Divider(color=DIVIDER_COLOR, height=60),
            ft.Column(
                [
                    ft.Text(
                        "(c) 2026 Anna NN Kambala | Computer Programming I ",
                        color=SUBTLE_COLOR,
                        size=12, italic=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=float("inf"),
            ),
            ft.Container(height=20),
        ], 
        spacing=0
    )



def _stat_card(value, label, icon, color):
    return ft.Container(
        col={"xs": 6, "sm": 6, "md": 3},
        content=ft.Column([
            ft.Icon(icon, size=28, color=color),
            ft.Text(value, size=32, weight=ft.FontWeight.BOLD,
                    color=TEXT_COLOR),
            ft.Text(label, size=12, color=SUBTLE_COLOR,
                    text_align=ft.TextAlign.CENTER),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        padding=20,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, color)),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.07, color),
    )


# ── TIMELINE ─────────────────────────────────────────────────────────────────
def timeline_body():
    entries = [
        ("Weeks 1–2: Initiation & Architecture",
         "Conducted initial design meetings to finalize the SRS technical contracts, "
         "role-based access flows, and data boundaries.",
         ft.Icons.ASSIGNMENT_TURNED_IN, "#5BC8F5", "SRS ARCHITECTURE"),
        ("Weeks 3–5: UI/UX & Frontend Scaffolding",
         "Collaborated with design leads to engineer modular components, form handling "
         "states, and responsive view containers matching mobile dimensions.",
         ft.Icons.DASHBOARD_CUSTOMIZE, "#A78BFA", "UI COMPONENTS"),
        ("Weeks 6–8: Core Route & Navigation Engineering",
         "Constructed state routing arrays, layout switching flows, and contextual "
         "tracking views for workers, technicians, and supervisors.",
         ft.Icons.ALT_ROUTE, "#4ADE80", "ROUTING MATRIX"),
        ("Weeks 9–10: Optimization & Offline Queue Strategy",
         "Configured system performance parameters, component rendering optimizations, "
         "and AsyncStorage local data fallback setups.",
         ft.Icons.CLOUD_SYNC, "#FB923C", "ASYNC STORAGE"),
        ("Weeks 11–12+: Deployment & Quality Assurance",
         "Assisted with end-to-end connectivity verification, Firestore document rule "
         "testing, and production behavior QA against SRS system benchmarks.",
         ft.Icons.VERIFIED, "#F472B6", "PRODUCTION QA"),
    ]

    cards = [
        ft.Container(
            padding=20,
            margin=ft.Margin(bottom=15, top=0, left=0, right=0),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.18, ACCENT_COLOR)),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.54, "#FFF7FB"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Icon(icon_node, color=node_color, size=24),
                        margin=ft.Margin(right=10, top=2, left=0, bottom=0),
                    ),
                    ft.Column(expand=True, spacing=8, controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(title, size=18,
                                        weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                                ft.Container(
                                    content=ft.Text(badge_text, size=11,
                                                    color=TEXT_COLOR,
                                                    weight=ft.FontWeight.W_600),
                                    bgcolor=ft.Colors.with_opacity(0.18, ACCENT_COLOR),
                                    padding=10, border_radius=15,
                                ),
                            ],
                        ),
                        ft.Text(desc, size=CONTENT_SIZE, color=SUBTLE_COLOR),
                    ]),
                ],
            ),
        )
        
        for title, desc, icon_node, node_color, badge_text in entries
    ]

    return ft.Column(controls=[
        ft.Text("Project Timeline", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "As the Documentation Lead for Group 1, I coordinated the EM-Lab SRS "
                "content and helped translate our project idea into clear requirements, "
                "system scope, role descriptions, Firebase data models, and use case "
                "documentation for the Computer Programming I submission.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=25, top=10),
        ),
        
        *cards,
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "(c) 2026 Anna NN Kambala | Computer Programming I ",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ], spacing=0)


# ── GITHUB ────────────────────────────────────────────────────────────────────
def github_body():
    return ft.Column(controls=[
        ft.Text("GitHub Evidence & Documentation", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "Working alongside our GitHub Managers and developers, I kept the "
                "project evidence aligned with the SRS by organizing requirement notes, "
                "documenting feature decisions, and connecting repository progress to "
                "the academic submission criteria.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=20, top=10),
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("Mining Documentation Impact Summary",
                        size=SUBHEADER_SIZE, weight=ft.FontWeight.BOLD,
                        color=ACCENT_COLOR),
                ft.Text(
                    "Problem Statement: Metallurgical laboratories need clearer digital "
                    "records for sample tracking, test result entry, furnace temperature "
                    "logging, and metallurgist approval workflows.\n\n"
                    "Individual Resolution: I documented the EM-Lab system requirements, "
                    "scope, assumptions, constraints, user roles, and Firebase data model "
                    "so the team could build from a shared and traceable SRS foundation.",
                    size=CONTENT_SIZE, color=TEXT_COLOR,
                ),
            ]),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.56, "#FFF7FB"),
            border_radius=10,
            margin=ft.Margin(bottom=20),
        ),
        ft.Divider(height=10, thickness=1,
                   color=ft.Colors.with_opacity(0.18, ACCENT_COLOR)),
        ft.Text("Project Repository", size=SUBHEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.ElevatedButton(
                "View Production Repository on GitHub",
                icon=ft.Icons.CODE,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE, bgcolor=ACCENT_COLOR,
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                url="https://github.com/",
            ),
            padding=ft.Padding(left=40, right=40),
        ),
        ft.Container(height=20),
        ft.Text("Verifiable Pull Request & Code Review Logs",
                size=SUBHEADER_SIZE, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column(controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALL_MERGE, color="green"),
                        title=ft.Text("SRS Update: Requirements Documentation",
                                      color=TEXT_COLOR,
                                      weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(
                            "Documented sample, testing, approval, and reporting flows",
                            color=ACCENT_COLOR),
                    ),
                    ft.Container(
                        content=ft.Image(src="github_contr.png",
                                         border_radius=4, fit=ft.BoxFit.COVER),
                        padding=ft.Padding(left=16, right=16, bottom=16),
                    ),
                ], spacing=0),
                col={"sm": 12, "md": 6},
                bgcolor=ft.Colors.with_opacity(0.56, "#FFF7FB"),
                border_radius=8,
            ),
            ft.Container(
                content=ft.Column(controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.RATE_REVIEW, color="amber"),
                        title=ft.Text("Feature Notes: EM-Lab Workflow Screens",
                                      color=TEXT_COLOR,
                                      weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(
                            "Reviewed documentation for sample and result screens",
                            color=ACCENT_COLOR),
                    ),
                    ft.Container(
                        content=ft.Image(src="report.png", height=200,
                                         border_radius=4, fit=ft.BoxFit.COVER),
                        padding=ft.Padding(left=16, right=16, bottom=16),
                    ),
                ], spacing=0),
                col={"sm": 12, "md": 6},
                bgcolor=ft.Colors.with_opacity(0.56, "#FFF7FB"),
                border_radius=8,
            ),
        ], spacing=15),
        ft.Container(height=15),
        ft.Container(
            content=ft.Column(controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HISTORY, color="blue"),
                    title=ft.Text("Development Commit History Screenshots",
                                  color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(
                        "Chronological stream of verified code repository updates",
                        color=ACCENT_COLOR),
                ),
                ft.Container(
                    content=ft.Image(src="history.png",
                                     border_radius=4, fit=ft.BoxFit.COVER),
                    padding=ft.Padding(left=16, right=16, bottom=16),
                ),
            ], spacing=0),
            bgcolor=ft.Colors.with_opacity(0.56, "#FFF7FB"),
            border_radius=8,
        ),
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "(c) 2026 Anna NN Kambala | Computer Programming I ",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ], spacing=10)


# ── MATLAB ────────────────────────────────────────────────────────────────────
def matlab_body():
    images = [
        "matlab1.png", "matlab2.png", "matlab3.png", "matlab4.png",
        "matlab5.png", "matlab6.png", "matlab7.png", "matlab8.png",
    ]
    labels = {
        "matlab1.png": "Wireless Communications Onramp",
        "matlab2.png": "Make and Manipulate Matrices",
        "matlab3.png": "Calculations with Vectors and Matrices",
        "matlab4.png": "Simulink Onramp",
        "matlab5.png": "Machine Learning Onramp",
        "matlab6.png": "MATLAB Onramp",
        "matlab7.png": "Explore Data with MATLAB Plots",
        
    }

    return ft.Column(controls=[
        ft.Text("MATLAB Academic Hub", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "Verified course completions from the MathWorks Learning Center. "
                "All 8 self-paced certificates were earned as part of the Computer "
                "Programming I module requirements for Semester 1, 2026.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=20, top=10),
        ),
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 6, "md": 3},
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            cert_card(img),
                            ft.Text(labels.get(img, "MATLAB Course"),
                                    size=14, weight=ft.FontWeight.W_500,
                                    color=TEXT_COLOR,
                                    text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                )
                for img in images
            ],
            spacing=10, run_spacing=20,
        ),
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "(c) 2026 Anna NN Kambala | Computer Programming I ",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ])


# ── DEMOS ─────────────────────────────────────────────────────────────────────
def demos_body():
    return ft.Column(
        controls=[
            ft.Column(
                [
                    ft.Text("EM-Lab System Demonstrations", size=HEADER_SIZE,
                            weight=ft.FontWeight.W_800, color=TEXT_COLOR,
                            style=ft.TextStyle(letter_spacing=0.5)),
                    ft.Text("Interactive media updates and core logic validations.", size=14, color=ft.Colors.with_opacity(0.7, TEXT_COLOR)),
                ],
                spacing=4,
            ),
            ft.Container(
                width=float("inf"),
                height=260,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1.0, -1.0),
                    end=ft.Alignment(1.0, 1.0),
                    colors=["#FFF7FB", "#F6C0DA"],
                ),
                border=ft.Border.all(1, ft.Colors.with_opacity(0.12, ACCENT_COLOR)),
                border_radius=16,
                padding=24,
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text("VIDEO RESOURCE", size=10, weight="bold", color=TEXT_COLOR),
                                    bgcolor=ft.Colors.with_opacity(0.16, ACCENT_COLOR),
                                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                                    border_radius=20,
                                ),
                                ft.Text("EM-Lab Project Contribution Video", color=TEXT_COLOR, size=20, weight="bold"),
                                ft.Text("Review system data processing architecture pipelines live.", color=ft.Colors.with_opacity(0.6, TEXT_COLOR), size=13),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.BLACK),
                                            ft.Text("Click here to Watch my project contribution video", color=ft.Colors.BLACK, weight="bold"),
                                        ],
                                        spacing=8,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=ACCENT_COLOR,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.Padding.symmetric(horizontal=20, vertical=12)
                                    ),
                                    on_click=lambda e: subprocess.Popen(["start", "https://unam164-my.sharepoint.com/:v:/g/personal/225150395_students_unam_na/IQC2PeHPz71KSKjtKo-hXlPGAb7Nvv_1nL_Y023tTGVc0dA?e=0odVyN"], shell=True),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            expand=True,
                            spacing=8,
                        ),
                        ft.Container(
                            content=(
                                ft.Video(
                                    src="assets/contribution_video.mp4",
                                    width=520,
                                    height=260,
                                    autoplay=False,
                                    controls=True,
                                    loop=False,
                                )
                                if hasattr(ft, "Video")
                                else ft.Column(
                                    [
                                        ft.Text(
                                            "Video playback is not supported by this Flet version.",
                                            size=14,
                                            color=TEXT_COLOR,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Container(height=12),
                                        ft.ElevatedButton(
                                            "Watch project video externally",
                                            icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                            on_click=lambda e: e.page.launch_url(
                                                "https://unam164-my.sharepoint.com/:v:/g/personal/225150395_students_unam_na/IQC2PeHPz71KSKjtKo-hXlPGAb7Nvv_1nL_Y023tTGVc0dA?e=0odVyN"
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                )
                            ),
                            alignment=ft.Alignment(0.0, 0.0),
                            expand=True,
                        ),
                    ],
                ),
            ),
            ft.Container(
                padding=ft.Padding.symmetric(vertical=10),
                content=ft.Divider(height=1, color=ft.Colors.with_opacity(0.08, TEXT_COLOR))
            ),
            ft.Text("Confidence in Concepts: System Mathematics",
                    size=SUBHEADER_SIZE, weight=ft.FontWeight.W_700, color=TEXT_COLOR),
            ft.ResponsiveRow(
                [
                    math_module_card(
                        "Sample Workflow",
                        "Digitization and systematic progression tracking of laboratory samples.",
                        "Status Lifecycle: Received -> Testing -> Completed",
                    ),
                    math_module_card(
                        "Result Approval Turnaround",
                        "Firestore records tracking how quickly submitted test results move through verification and approval.",
                        "Average Approval Time = Sum(Approval_Time) / N",
                        "N = Total Number of Approved Results",
                        "Notation Compliant Formula Model",
                    ),
                    math_module_card(
                        "Sample Status Indexing",
                        "Dynamic data mapping connecting samples, tests, furnace logs, and results.",
                        "Status Mapping: Received | In_Furnace | Testing | Completed",
                    ),
                    math_module_card(
                        "Operational Financial Model",
                        "Formula model verifying aggregate materials processing costs matching lecture criterion.",
                        "Total Cost = ∑ⁿᵢ₌₁ (Qᵢ × Pᵢ) + Overheads",
                        None,
                        "Aggregate Procurement Value Contract",
                    ),
                ],
                spacing=24,
                run_spacing=24,
            ),

            ft.Divider(color=DIVIDER_COLOR, height=60),
            ft.Column(
                [
                    ft.Text(
                        "(c) 2026 Anna NN Kambala | Computer Programming I",
                        color=SUBTLE_COLOR,
                        size=12, italic=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=float("inf"),
            ),
            ft.Container(height=20),
        ],
        spacing=24,
    )


# ── BLOG ──────────────────────────────────────────────────────────────────────
def blog_body():
    return ft.Column(controls=[
        ft.Text("Technical Engineering Blog", size=HEADER_SIZE,
                weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
        ft.Container(
            content=ft.Text(
                "A sequence of design analyses explaining our methodologies, "
                "implementation roadmaps, and optimization milestones completed "
                "during the development of EM-Lab for the University of Namibia.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR,
            ),
            margin=ft.Margin(bottom=30, top=10),
        ),
        blog_post_preview(
            "Cross-Platform Performance and React Native",
            "An evaluation of managed Expo frameworks for laboratory sample and "
            "test result tracking on Android platforms.",
        ),
        blog_post_preview(
            "Structuring NoSQL Document Boundaries",
            "Developing real-time relational data representations and permission "
            "matrices using Cloud Firestore schemas.",
        ),
        blog_post_preview(
            "Mitigating Information Loss in Laboratory Records",
            "Improving documentation for traceable records, approval decisions, "
            "and synchronized laboratory workflows.",
        ),
        
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "(c) 2026 Anna NN Kambala | Computer Programming I",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

        
    ])


# ── CONTACT ───────────────────────────────────────────────────────────────────
def contact_body(page: ft.Page):
    name_field  = ft.TextField(label="Name",    border_color=ACCENT_COLOR,
                                color=TEXT_COLOR, cursor_color=ACCENT_COLOR)
    email_field = ft.TextField(label="Email",   border_color=ACCENT_COLOR,
                                color=TEXT_COLOR)
    msg_field   = ft.TextField(label="Message", multiline=True, min_lines=3,
                                border_color=ACCENT_COLOR, color=TEXT_COLOR)

    return ft.Column(controls=[
        ft.Text("Contact Me", size=32, weight=ft.FontWeight.BOLD,
                color=TEXT_COLOR),
        ft.Container(
            padding=20,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        padding=20,
                        content=ft.Column([
                            ft.Text(
                                "I am always open to new academic collaborations, "
                                "development opportunities, or discussions surrounding "
                                "metallurgical laboratory systems, mining workflows, and technical documentation. "
                                "Drop me a message below to connect!",
                                size=16, color=TEXT_COLOR,
                                text_align=ft.TextAlign.LEFT,
                            ),
                            ft.Container(height=15),
                            ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.EMAIL, color=ACCENT_COLOR, size=18),
                                    ft.Text("Email: ", weight=ft.FontWeight.BOLD,
                                            color=TEXT_COLOR, size=15),
                                    ft.Text("anna.kambala@example.com",
                                            color=SUBTLE_COLOR, size=15),
                                ], spacing=5),
                                ft.Row([
                                    ft.Icon(ft.Icons.PHONE, color=ACCENT_COLOR, size=18),
                                    ft.Text("Cell: ", weight=ft.FontWeight.BOLD,
                                            color=TEXT_COLOR, size=15),
                                    ft.Text("+264 81 000 0000",
                                            color=SUBTLE_COLOR, size=15),
                                ], spacing=5),
                                ft.Row([
                                    ft.Icon(ft.Icons.CAMERA_ALT, color=ACCENT_COLOR, size=18),
                                    ft.Text("Instagram: ", weight=ft.FontWeight.BOLD,
                                            color=TEXT_COLOR, size=15),
                                    ft.Text("anna_kambala",
                                            color=SUBTLE_COLOR, size=15),
                                ], spacing=5),
                            ], spacing=10),
                        ])
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 5},
                        padding=30,
                        bgcolor=ft.Colors.with_opacity(0.56, "#FFF7FB"),
                        border=ft.Border.all(
                            1, ft.Colors.with_opacity(0.20, ACCENT_COLOR)),
                        border_radius=20,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                name_field, email_field, msg_field,
                                ft.ElevatedButton(
                                    "Send Message",
                                    style=ft.ButtonStyle(bgcolor=DIVIDER_COLOR,
                                                         color=ft.Colors.WHITE),
                                    width=float("inf"),
                                    on_click=lambda _: page.launch_url(
                                        f"mailto:anna.kambala@example.com"
                                        f"?subject=Message from {name_field.value}"
                                        f"&body=From: {email_field.value}"
                                        f"%0D%0A%0D%0A{msg_field.value}"
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ),
        ft.Divider(color=DIVIDER_COLOR, height=60),
        ft.Column(
            [
                ft.Text(
                    "(c) 2026 Anna NN Kambala | Computer Programming I",
                    color=SUBTLE_COLOR,
                    size=12, italic=True,
                    text_align=ft.TextAlign.CENTER, # Ensures multi-line text wraps centered
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=float("inf"), # Forces the alignment container to span the full window width
        ),
        ft.Container(height=20),

    ])


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main(page: ft.Page):
    page.title = "Web Portfolio - Anna NN Kambala"
    page.assets_dir = "."
    page.padding = 0
    page.scroll = "none"
    page.bgcolor = BG_COLOR

    def route_change(e):
        page.controls.clear()
        route = page.route or "/home"

        route_map = {
            "/home":     ("home",     home_body()),
            "/timeline": ("timeline", timeline_body()),
            "/github":   ("github",   github_body()),
            "/matlab":   ("matlab",   matlab_body()),
            "/demos":    ("demos",    demos_body()),
            "/blog":     ("blog",     blog_body()),
            "/contact":  ("contact",  contact_body(page)),
        }

        key, body = route_map.get(route, route_map["/home"])
        page.add(page_shell(page, key, body))
        page.update()

    page.on_route_change = route_change
    page.go("/home")


ft.app(
    target=main,
    assets_dir=".",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
    view=ft.AppView.WEB_BROWSER,
)
