import datetime
import base64
import sqlite3
from pathlib import Path
from urllib.parse import quote

import plotly.express as px
import pandas as pd
import streamlit as st

TRANSLATIONS = {
    "العربية": {
        "page_title": "المعرض الرقمي | قسم الحاسب", "brand": "المعرض الرقمي", "brand_sub": "قسم الحاسب الآلي · مساحة للإبداع والابتكار",
        "language": "اللغة / Language", "arabic": "العربية", "english": "English", "nav": "التنقل", "gallery": "المعرض", "admin": "لوحة تحكم الإدارة",
        "sidebar_note": "قسم الحاسب الآلي · 2026", "admin_eyebrow": "مساحة الإدارة", "admin_copy": "نظرة عامة على مشاريع المعرض وتفاعل المجتمع",
        "password": "كلمة مرور الإدارة", "login": "دخول لوحة الإدارة", "bad_password": "كلمة المرور غير صحيحة.",
        "total_projects": "إجمالي المشاريع", "total_likes": "إجمالي الإعجابات", "category_chart": "توزيع المشاريع حسب المسار", "category": "المسار", "project_count": "عدد المشاريع", "logout": "تسجيل الخروج من لوحة الإدارة",
        "manage_projects": "إدارة المشاريع", "project_title": "اسم المشروع", "student": "المتدرب", "likes_column": "الإعجابات", "date_column": "التاريخ", "delete_project": "حذف المشروع 🗑️", "choose_project": "اختر مشروعاً", "confirm_delete": "هل أنت متأكد من حذف هذا المشروع؟ لا يمكن التراجع عن الحذف.", "confirm": "تأكيد الحذف", "cancel_delete": "إلغاء", "deleted": "تم حذف المشروع.", "pending_projects": "المشاريع قيد المراجعة", "approve": "موافقة ✅", "reject": "رفض ❌", "approved": "تمت الموافقة على المشروع.", "rejected": "تم رفض المشروع وحذفه.", "status": "الحالة", "status_approved": "معتمد", "status_pending": "قيد المراجعة", "success_added": "تم إرسال مشروعك بنجاح، وسيتم مراجعته من قبل إدارة القسم قريباً",
        "download_csv": "تحميل البيانات كملف CSV 📥", "csv_filename": "مشاريع_المعرض.csv",
        "hero_eyebrow": "معرض المشاريع الطلابية · 2026", "hero_title": "معرض إبداعات قسم الحاسب", "hero_copy": "منصة رقمية دائمة لعرض إبداعات متدربينا في الذكاء الاصطناعي، الأمن السيبراني، وتطوير البرمجيات",
        "chip_ideas": "✧ أفكار تصنع المستقبل", "chip_learning": "⌘ مشاريع من واقع التعلّم", "chip_community": "◉ مجتمع تقني ملهم",
        "add_project": "أضف مشروعك　➕", "search_label": "ابحث عن مشروع بالاسم", "search_placeholder": "اكتب اسم المشروع للبحث…",
        "add_heading": "أضف مشروعك إلى المعرض", "add_caption": "شارك فكرتك مع مجتمع قسم الحاسب", "field_title": "اسم المشروع", "field_student": "اسم المتدرب / المتدربة",
        "field_title_en": "اسم المشروع بالإنجليزية (اختياري)", "field_student_en": "اسم المتدرب بالإنجليزية (اختياري)", "field_description_en": "وصف المشروع بالإنجليزية (اختياري)",
        "field_category": "التصنيف", "field_description": "نبذة عن المشروع", "field_url": "رابط المشروع", "field_image": "رابط صورة (اختياري)", "image_placeholder": "رابط صورة من Unsplash أو غيره",
        "submit_project": "إرسال المشروع ✨", "cancel": "إلغاء ❌", "required_error": "يرجى تعبئة اسم المشروع واسم المتدرب والنبذة.",
        "discover": "اكتشف المشاريع", "discover_caption": "أفكار مميزة تحولت إلى تجارب رقمية ملهمة", "filter_label": "تصفية المشاريع", "all": "الكل", "games": "ألعاب", "ai": "ذكاء اصطناعي", "cyber": "أمن سيبراني", "apps": "تطبيقات",
        "empty": "لا توجد مشاريع في هذا التصنيف حالياً.", "featured": "✧ مشروع مميز", "details": "عرض التفاصيل　↗", "modal": "تفاصيل المشروع", "added_on": "تاريخ الإضافة", "likes": "إعجاب", "like": "أعجبني 👍", "liked": "تم الإعجاب ❤️", "visit": "زيارة المشروع ↗", "share_whatsapp": "مشاركة عبر واتساب", "share_telegram": "مشاركة عبر تيليجرام", "footer": "نبني اليوم أفكار الغد　 ✦　 صُنع بشغف تقني",
        "categories": {"ألعاب": "ألعاب", "ذكاء اصطناعي": "ذكاء اصطناعي", "أمن سيبراني": "أمن سيبراني", "تطبيقات": "تطبيقات"},
    },
    "English": {
        "page_title": "Digital Showcase | Computer Science", "brand": "Digital Showcase", "brand_sub": "Computer Science Department · A space for creativity and innovation",
        "language": "Language / اللغة", "arabic": "العربية", "english": "English", "nav": "Navigation", "gallery": "Gallery", "admin": "Admin Dashboard",
        "sidebar_note": "Computer Science Department · 2026", "admin_eyebrow": "ADMIN SPACE", "admin_copy": "An overview of showcase projects and community engagement",
        "password": "Admin password", "login": "Open admin dashboard", "bad_password": "Incorrect password.",
        "total_projects": "Total projects", "total_likes": "Total likes", "category_chart": "Projects by category", "category": "Category", "project_count": "Project count", "logout": "Log out of admin dashboard",
        "manage_projects": "Manage projects", "project_title": "Project title", "student": "Student", "likes_column": "Likes", "date_column": "Date", "delete_project": "Delete project 🗑️", "choose_project": "Select a project", "confirm_delete": "Are you sure you want to delete this project? This cannot be undone.", "confirm": "Confirm deletion", "cancel_delete": "Cancel", "deleted": "Project deleted.", "pending_projects": "Projects pending review", "approve": "Approve ✅", "reject": "Reject ❌", "approved": "Project approved.", "rejected": "Project rejected and deleted.", "status": "Status", "status_approved": "Approved", "status_pending": "Pending review", "success_added": "Your project was submitted successfully and will be reviewed by the department administration soon.",
        "download_csv": "Download data as CSV 📥", "csv_filename": "showcase_projects.csv",
        "hero_eyebrow": "STUDENT PROJECT SHOWCASE · 2026", "hero_title": "Computer Science Creations", "hero_copy": "A lasting digital home for our trainees’ work in artificial intelligence, cybersecurity, and software development.",
        "chip_ideas": "✧ Ideas shaping tomorrow", "chip_learning": "⌘ Projects built through learning", "chip_community": "◉ An inspiring tech community",
        "add_project": "Add your project　➕", "search_label": "Search projects by name", "search_placeholder": "Type a project name to search…",
        "add_heading": "Add your project to the showcase", "add_caption": "Share your idea with the Computer Science community", "field_title": "Project title", "field_student": "Student name",
        "field_title_en": "Project title in English (optional)", "field_student_en": "Student name in English (optional)", "field_description_en": "Project description in English (optional)",
        "field_category": "Category", "field_description": "Project description", "field_url": "Project URL", "field_image": "Image URL (optional)", "image_placeholder": "Image link from Unsplash or another source",
        "submit_project": "Submit project ✨", "cancel": "Cancel ❌", "required_error": "Please enter a project title, student name, and description.",
        "discover": "Explore projects", "discover_caption": "Distinctive ideas transformed into inspiring digital experiences", "filter_label": "Filter projects", "all": "All", "games": "Games", "ai": "Artificial Intelligence", "cyber": "Cybersecurity", "apps": "Applications",
        "empty": "There are no projects in this category yet.", "featured": "✧ Featured project", "details": "View details　↗", "modal": "Project details", "added_on": "Added on", "likes": "likes", "like": "Like 👍", "liked": "Liked ❤️", "visit": "Visit project ↗", "share_whatsapp": "Share on WhatsApp", "share_telegram": "Share on Telegram", "footer": "Building tomorrow’s ideas today　 ✦　 Made with a passion for technology",
        "categories": {"ألعاب": "Games", "ذكاء اصطناعي": "Artificial Intelligence", "أمن سيبراني": "Cybersecurity", "تطبيقات": "Applications"},
    },
}

st.set_page_config(
    layout="wide",
    page_title="Digital Showcase | المعرض الرقمي",
    page_icon="🚀",
    initial_sidebar_state="auto",
)

if "language" not in st.session_state:
    st.session_state.language = "العربية"
LANG = st.session_state.language
RTL = LANG == "العربية"


def t(key):
    return TRANSLATIONS[LANG][key]

with st.sidebar:
    st.selectbox(t("language"), ["العربية", "English"], key="language", format_func=lambda value: "🌍  " + value)
LANG = st.session_state.language
RTL = LANG == "العربية"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Tajawal:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg: #0B0F19;
        --panel: rgba(255,255,255,.055);
        --panel-strong: rgba(255,255,255,.085);
        --line: rgba(255,255,255,.11);
        --muted: #9AA8BF;
        --text: #F3F7FF;
        --blue: #48C8FF;
        --violet: #9A7BFF;
        --mint: #64F0C8;
    }
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: '__FONT__', sans-serif !important;
        direction: __DIRECTION__;
    }
    [data-testid="stAppViewContainer"] {
        color: var(--text);
        background:
          radial-gradient(ellipse at 12% 4%, rgba(30,105,185,.18), transparent 34%),
          radial-gradient(ellipse at 88% 15%, rgba(117,63,204,.14), transparent 31%),
          linear-gradient(145deg, #0B0F19 0%, #0D1422 55%, #090D16 100%);
    }
    [data-testid="stToolbar"], #MainMenu, footer, [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0; }
    @media(min-width:769px) { [data-testid="stHeader"] { visibility:hidden; height:0; } }
    [data-testid="stMainBlockContainer"] { max-width: 1440px; padding: 1.2rem 3rem 4rem; }
    [data-testid="stVerticalBlock"] { gap: .85rem; }
    p, label, span, div { font-family: '__FONT__', sans-serif; }

    .topline { height: 1px; width:100%; margin: 0 auto 1.8rem; background: linear-gradient(90deg, transparent, rgba(72,200,255,.55), rgba(154,123,255,.38), transparent); }
    .brand-row { display:flex; align-items:center; gap:12px; color:#dce8f7; font-weight:700; letter-spacing:.2px; }
    .brand-mark { display:inline-flex; width:40px; height:40px; align-items:center; justify-content:center; border-radius:13px; background:linear-gradient(140deg,rgba(72,200,255,.22),rgba(154,123,255,.23)); border:1px solid rgba(117,206,255,.25); box-shadow:0 0 28px rgba(51,163,255,.13); font-size:20px; }
    .brand-sub { color:#8392aa; font-size:13px; font-weight:400; margin-top:2px; }
    .hero { position:relative; overflow:hidden; text-align:center; padding:3.1rem 1rem 1.25rem; }
    .hero:before { content:""; position:absolute; width:390px; height:170px; border-radius:50%; filter:blur(80px); background:rgba(32,145,255,.12); top:4px; left:calc(50% - 195px); pointer-events:none; }
    .eyebrow { display:inline-flex; gap:9px; align-items:center; border:1px solid rgba(112,193,255,.22); background:rgba(33,116,184,.1); color:#9edfff; padding:7px 14px; border-radius:99px; font-size:13px; margin-bottom:17px; }
    .eyebrow i { display:block; width:7px; height:7px; background:#55e4c4; border-radius:50%; box-shadow:0 0 12px #55e4c4; }
    .hero-title { position:relative; margin:0 auto 12px; font-size:clamp(2.35rem,5.6vw,4.7rem); font-weight:900; line-height:1.2; letter-spacing:-1.6px; background:linear-gradient(100deg,#f8fbff 8%,#68d6ff 37%,#9c8aff 67%,#62efd1 92%); background-size:220% auto; color:transparent; -webkit-background-clip:text; background-clip:text; animation:gradientFlow 8s ease-in-out infinite; }
    @keyframes gradientFlow { 0%,100%{background-position:0% center} 50%{background-position:100% center} }
    .hero-copy { position:relative; color:#aab6ca; font-size:19px; line-height:1.8; max-width:760px; margin:auto; }
    .college-logo-wrap { display:flex; justify-content:center; align-items:center; width:142px; height:142px; box-sizing:border-box; margin:0 auto 20px; padding:12px; overflow:hidden; border-radius:24px; background:rgba(255,255,255,.95); border:1px solid rgba(255,255,255,.72); box-shadow:0 0 25px rgba(255,255,255,.2),0 12px 36px rgba(36,157,255,.16); }
    .college-logo { display:block; width:100%; height:100%; object-fit:contain; filter:none !important; opacity:1 !important; mix-blend-mode:normal !important; }
    .hero-meta { display:flex; justify-content:center; gap:10px; margin-top:25px; flex-wrap:wrap; }
    .meta-chip { border:1px solid rgba(255,255,255,.09); background:rgba(255,255,255,.035); border-radius:99px; color:#b9c6d9; font-size:13px; padding:7px 13px; }
    .section-heading { font-size:21px; font-weight:800; color:#f3f7ff; margin: 0 0 2px; }
    .section-caption { color:#8290a6; font-size:14px; margin-bottom:14px; }

    /* Filter pills */
    div[role="radiogroup"] { direction:__DIRECTION__; display:flex; flex-wrap:wrap; justify-content:center; gap:9px; padding:10px 0 17px; }
    div[role="radiogroup"] label { background:rgba(255,255,255,.045); border:1px solid rgba(255,255,255,.09); border-radius:99px; padding:8px 18px; transition:.22s ease; color:#b5c1d3 !important; cursor:pointer; }
    div[role="radiogroup"] label:hover { border-color:rgba(72,200,255,.45); color:white !important; transform:translateY(-2px); }
    div[role="radiogroup"] label:has(input:checked) { color:#ecfaff !important; background:linear-gradient(110deg,rgba(31,144,217,.27),rgba(117,87,218,.22)); border-color:rgba(83,196,255,.55); box-shadow:0 0 24px rgba(49,166,255,.12), inset 0 0 14px rgba(69,186,255,.06); }
    div[role="radiogroup"] label p { margin:0; font-weight:600; }
    div[role="radiogroup"] input { display:none; }

    /* Project cards */
    .project-card { height:100%; overflow:hidden; border-radius:20px; border:1px solid rgba(255,255,255,.10); background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.028)); backdrop-filter:blur(10px); box-shadow:0 16px 42px rgba(0,0,0,.18); transition:transform .28s ease,border-color .28s ease,box-shadow .28s ease; }
    .project-card:hover { transform:translateY(-5px); border-color:rgba(72,200,255,.62); box-shadow:0 18px 42px rgba(20,137,255,.16),0 0 0 1px rgba(72,200,255,.12); }
    .card-cover { height:205px; position:relative; overflow:hidden; background:#101827; }
    .card-cover img { width:100%; height:100%; object-fit:cover; opacity:.82; transition:transform .55s ease,opacity .35s ease; }
    .project-card:hover .card-cover img { transform:scale(1.055); opacity:1; }
    .card-cover:after { content:""; position:absolute; inset:35% 0 0; background:linear-gradient(transparent,rgba(8,12,21,.92)); }
    .cover-index { position:absolute; z-index:1; top:14px; right:15px; color:rgba(255,255,255,.85); font-size:12px; border-radius:99px; background:rgba(8,13,23,.55); border:1px solid rgba(255,255,255,.18); padding:5px 10px; backdrop-filter:blur(8px); }
    .card-body { padding:19px 20px 17px; }
    .card-top { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:9px; }
    .card-title { color:#f1f6ff; font-size:21px; font-weight:800; line-height:1.35; }
    .badge { flex-shrink:0; color:#8bdfff; background:rgba(41,155,214,.12); border:1px solid rgba(81,195,245,.2); border-radius:99px; padding:5px 10px; font-size:11px; font-weight:700; }
    .card-desc { color:#98a7bb; font-size:14px; line-height:1.75; min-height:49px; }
    .card-foot { display:flex; align-items:center; justify-content:space-between; border-top:1px solid rgba(255,255,255,.07); padding-top:13px; margin-top:14px; color:#a8b5c8; font-size:13px; }
    .student { display:flex; align-items:center; gap:8px; }
    .avatar { width:27px; height:27px; display:inline-flex; align-items:center; justify-content:center; border-radius:50%; background:linear-gradient(135deg,rgba(72,200,255,.3),rgba(154,123,255,.3)); color:#d8f5ff; font-size:12px; }
    div.stButton > button { font-family:'__FONT__',sans-serif; border-radius:11px; border:1px solid rgba(72,200,255,.3); background:rgba(55,156,220,.11); color:#bcecff; font-weight:700; transition:.2s ease; }
    div.stButton > button:hover { border-color:#55caff; color:white; background:rgba(43,151,220,.25); box-shadow:0 0 20px rgba(49,166,255,.12); transform:translateY(-1px); }
    .card-action div.stButton > button { width:100%; margin-top:0; }
    .empty-state { text-align:center; padding:55px 20px; border:1px dashed rgba(255,255,255,.14); border-radius:20px; color:#9baac0; background:rgba(255,255,255,.025); }
    .footer-line { height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,.12),transparent); margin:3rem 0 1.3rem; }
    .site-footer { color:#65748c; text-align:center; font-size:13px; }
    .site-footer strong { color:#94a5bd; }

    /* Streamlit controls and dialogs */
    [data-testid="stDialog"] > div > div { background:#111927; border:1px solid rgba(95,190,255,.22); border-radius:20px; }
    [data-testid="stDialog"] h2 { color:#f3f7ff; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] [data-baseweb="select"] > div { direction:__DIRECTION__; text-align:__TEXT_ALIGN__; background:rgba(255,255,255,.055); color:#edf5ff; border-color:rgba(255,255,255,.15); border-radius:10px; }
    [data-testid="stForm"] { padding:15px 18px; border:1px solid rgba(255,255,255,.1); border-radius:17px; background:rgba(255,255,255,.035); }
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button[kind="secondary"] { background:rgba(255,105,120,.10); color:#ffc0c8; border:1px solid rgba(255,120,135,.28); }
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button[kind="secondary"]:hover { background:rgba(255,105,120,.20); border-color:rgba(255,120,135,.55); color:#fff; }
    [data-testid="stForm"] label { color:#c8d4e4 !important; }
    [data-testid="stLinkButton"] a { border-radius:11px; background:linear-gradient(110deg,#168bd4,#7866e8); border:0; color:white !important; font-family:'__FONT__',sans-serif; font-weight:700; }
    .stAlert { direction:__DIRECTION__; }
    @media(max-width:768px) {
        [data-testid="stHeader"] {
            display:block !important;
            visibility:visible !important;
            height:auto !important;
            min-height:3rem !important;
            background:transparent !important;
            box-shadow:none !important;
            overflow:visible !important;
        }
        [data-testid="stToolbar"] {
            display:flex !important;
            visibility:visible !important;
            height:auto !important;
            min-height:3rem !important;
            background:transparent !important;
        }
        .viewerBadge_container__1QSob { display:none !important; }
        [data-testid="stSidebar"] {
            min-width:250px !important;
            background-color:#0B0F19 !important;
            transform:translateX(-100%) !important;
            transition:transform .3s ease-in-out !important;
        }
        [data-testid="stSidebar"][aria-expanded="true"] {
            transform:translateX(0) !important;
        }
        [data-testid="collapsedControl"] {
            left:10px !important;
            top:10px !important;
        }
        [data-testid="stMainBlockContainer"]{padding:1rem 1rem 2.5rem}
        .hero{padding:2rem .2rem 1rem}
        .hero-copy{font-size:16px}
        .card-cover{height:185px}
        .college-logo-wrap{width:116px;height:116px;margin-bottom:18px;border-radius:21px}
    }
    </style>
    """.replace("__DIRECTION__", "rtl" if RTL else "ltr")
       .replace("__TEXT_ALIGN__", "right" if RTL else "left")
       .replace("__FONT__", "Tajawal" if RTL else "Inter"),
    unsafe_allow_html=True,
)


PROJECTS = {
    "p1": {"name": "مساعد الطالب الذكي", "name_en": "Smart Student Assistant", "student": "عبدالله الحربي", "student_en": "Abdullah Alharbi", "category": "ذكاء اصطناعي", "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85", "description": "مساعد محادثة ذكي يفهم أسئلة الطلاب ويقترح مصادر تعلم وخططاً دراسية مخصصة. يجمع بين معالجة اللغة العربية وتجربة استخدام بسيطة تساعد الطالب على الوصول للمعلومة بسرعة.", "description_en": "An intelligent conversational assistant that answers student questions and recommends learning resources and personalized study plans. It combines Arabic language processing with a simple experience that helps learners find information quickly.", "url": "https://github.com/", "added": "2026-01-18", "likes": 15},
    "p2": {"name": "درع الحماية", "name_en": "Shield of Protection", "student": "محمد العتيبي", "student_en": "Mohammed Alotaibi", "category": "أمن سيبراني", "image": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?q=80&w=1000&auto=format&fit=crop", "description": "لوحة توعوية تفاعلية تساعد المستخدم على اكتشاف رسائل التصيد وممارسات الاحتيال الرقمي، مع إرشادات عملية لتقوية كلمات المرور وحماية الحسابات والأجهزة.", "description_en": "An interactive awareness dashboard that helps users spot phishing messages and online scams, with practical guidance for strengthening passwords and protecting accounts and devices.", "url": "https://github.com/", "added": "2026-02-06", "likes": 23},
    "p3": {"name": "متاهة النيون", "name_en": "Neon Maze", "student": "خالد القحطاني", "student_en": "Khalid Alqahtani", "category": "ألعاب", "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=85", "description": "لعبة ألغاز ثنائية الأبعاد تدور في عالم مستقبلي نابض بالألوان. على اللاعب حل التحديات وجمع الطاقة لفتح المراحل، مع تصاعد تدريجي في الصعوبة ومؤثرات بصرية تفاعلية.", "description_en": "A 2D puzzle game set in a vibrant futuristic world. Players solve challenges and collect energy to unlock levels, with steadily increasing difficulty and interactive visual effects.", "url": "https://github.com/", "added": "2026-03-12", "likes": 31},
    "p4": {"name": "بصيرة البيانات", "name_en": "Data Insight", "student": "فهد الدوسري", "student_en": "Fahad Aldosari", "category": "ذكاء اصطناعي", "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=85", "description": "منصة تستكشف مجموعات البيانات وتحوّلها إلى لوحات ورسوم واضحة، مع نماذج تنبؤية مبسطة تكشف الأنماط والاتجاهات وتدعم اتخاذ القرار.", "description_en": "A platform for exploring datasets and turning them into clear dashboards and visualizations. Simple predictive models reveal patterns and trends to support informed decisions.", "url": "https://github.com/", "added": "2026-04-02", "likes": 18},
    "p5": {"name": "نبض المدينة", "name_en": "City Pulse", "student": "سعود الشهري", "student_en": "Saud Alshehri", "category": "تطبيقات", "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1200&q=85", "description": "تطبيق ذكي يعرض معلومات المدينة اليومية في تجربة موحدة؛ من جودة الهواء والطقس إلى اقتراحات الأماكن والأنشطة، بتصميم يركز على سهولة الوصول للمعلومة.", "description_en": "A smart app bringing daily city information into one experience, from air quality and weather to place and activity suggestions, with a focus on easy access to useful information.", "url": "https://github.com/", "added": "2026-05-14", "likes": 12},
    "p6": {"name": "شفرة الظلال", "name_en": "Shadow Cipher", "student": "يوسف الزهراني", "student_en": "Yousef Alzahrani", "category": "أمن سيبراني", "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1000&auto=format&fit=crop", "description": "مختبر تعليمي مصغر يقدم تحديات آمنة في أساسيات التشفير وتحليل الشيفرات. يتدرج المتعلم من مفاهيم الحماية الأولى إلى بناء عقلية تحليلية واعية بالمخاطر.", "description_en": "A compact learning lab with safe challenges in cryptography fundamentals and code analysis. Learners progress from basic security concepts to a thoughtful, risk-aware mindset.", "url": "https://github.com/", "added": "2026-06-21", "likes": 27},
}

DB_PATH = "showcase.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        table_existed = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='projects'"
        ).fetchone() is not None
        connection.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                student_name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                image_url TEXT NOT NULL,
                date_added TEXT NOT NULL,
                likes INTEGER NOT NULL DEFAULT 0,
                title_en TEXT,
                student_name_en TEXT,
                description_en TEXT,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        """)
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(projects)").fetchall()}
        for column in ("title_en", "student_name_en", "description_en"):
            if column not in columns:
                connection.execute(f"ALTER TABLE projects ADD COLUMN {column} TEXT")
        if "status" not in columns:
            connection.execute("ALTER TABLE projects ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'")
            if table_existed:
                # Existing projects predate moderation and remain visible after the schema upgrade.
                connection.execute("UPDATE projects SET status = 'approved'")

        # Preserve older database records and provide Arabic fallback until translations are supplied.
        connection.execute("UPDATE projects SET title_en = title WHERE title_en IS NULL OR TRIM(title_en) = ''")
        connection.execute("UPDATE projects SET student_name_en = student_name WHERE student_name_en IS NULL OR TRIM(student_name_en) = ''")
        connection.execute("UPDATE projects SET description_en = description WHERE description_en IS NULL OR TRIM(description_en) = ''")

        # Add English translations to the six demo rows created by earlier app versions.
        for project in PROJECTS.values():
            connection.execute("""
                UPDATE projects
                SET title_en = ?, student_name_en = ?, description_en = ?
                WHERE title = ? AND title_en = title AND student_name_en = student_name AND description_en = description
            """, (project["name_en"], project["student_en"], project["description_en"], project["name"]))

        shield_project = PROJECTS["p2"]
        connection.execute(
            "UPDATE projects SET image_url = ? WHERE title = ? AND image_url LIKE ?",
            (shield_project["image"], shield_project["name"], "https://images.unsplash.com/photo-1550751827-4bd374c3f58b%"),
        )

        project_count = connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        if project_count == 0:
            seed_rows = [
                (p["name"], p["student"], p["category"], p["description"], p["image"], p["added"], p["likes"],
                 p["name_en"], p["student_en"], p["description_en"], "approved")
                for p in PROJECTS.values()
            ]
            connection.executemany("""
                INSERT INTO projects (title, student_name, category, description, image_url, date_added, likes, title_en, student_name_en, description_en, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, seed_rows)


def get_projects():
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM projects ORDER BY id").fetchall()
    return {
        str(row["id"]): {
            "name": (row["title_en"] or row["title"]) if LANG == "English" else row["title"],
            "student": (row["student_name_en"] or row["student_name"]) if LANG == "English" else row["student_name"],
            "category": row["category"],
            "description": (row["description_en"] or row["description"]) if LANG == "English" else row["description"],
            "image": row["image_url"],
            "added": row["date_added"], "likes": row["likes"], "status": row["status"], "url": "https://github.com/",
        }
        for row in rows
    }


def add_project(title, student_name, category, description, image_url, title_en, student_name_en, description_en):
    added_at = datetime.datetime.now().isoformat(timespec="seconds")
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO projects (title, student_name, category, description, image_url, date_added, likes, title_en, student_name_en, description_en, status)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, 'pending')
        """, (title, student_name, category, description, image_url, added_at, title_en, student_name_en, description_en))
        return str(cursor.lastrowid)


def increment_project_likes(project_id):
    with get_connection() as connection:
        connection.execute("UPDATE projects SET likes = likes + 1 WHERE id = ?", (int(project_id),))


def delete_project(project_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM projects WHERE id = ?", (int(project_id),))


def set_project_status(project_id, status):
    with get_connection() as connection:
        connection.execute("UPDATE projects SET status = ? WHERE id = ?", (status, int(project_id)))


initialize_database()
if st.session_state.get("active_filter") not in {"all", "ألعاب", "ذكاء اصطناعي", "أمن سيبراني", "تطبيقات"}:
    st.session_state.active_filter = "all"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "liked_project_ids" not in st.session_state:
    st.session_state.liked_project_ids = set()

with st.sidebar:
    st.markdown(f"## 🚀 {t('brand')}")
    page = st.radio(t("nav"), ["gallery", "admin"], format_func=lambda value: t(value), label_visibility="collapsed")
    st.markdown("---")
    st.caption(t("sidebar_note"))


@st.dialog(t("modal"), width="large")
def show_project(project_key):
    project = get_projects()[project_key]
    already_liked = project_key in st.session_state.liked_project_ids
    st.image(project["image"], use_container_width=True)
    st.markdown(f"### {project['name']}")
    display_category = TRANSLATIONS[LANG]["categories"].get(project["category"], project["category"])
    st.markdown(f"**{project['student']}**　 ·　 `{display_category}`")
    st.caption(f"{t('added_on')}: {project['added']}　 ·　 {project['likes']} {t('likes')}")
    st.write(project["description"])
    like_col, visit_col = st.columns(2)
    with like_col:
        like_label = t("liked") if already_liked else t("like")
        if st.button(like_label, key=f"like_{project_key}", disabled=already_liked, use_container_width=True):
            increment_project_likes(project_key)
            st.session_state.liked_project_ids.add(project_key)
    with visit_col:
        st.link_button(t("visit"), project["url"], use_container_width=True)
    share_text = f"{project['name']} — {project['url']}"
    whatsapp_url = f"https://wa.me/?text={quote(share_text)}"
    telegram_url = f"https://t.me/share/url?url={quote(project['url'])}&text={quote(project['name'])}"
    share_left, share_right = st.columns(2)
    with share_left:
        st.link_button(t("share_whatsapp"), whatsapp_url, use_container_width=True)
    with share_right:
        st.link_button(t("share_telegram"), telegram_url, use_container_width=True)


if page == "admin":
    st.markdown('<div class="topline"></div>', unsafe_allow_html=True)
    st.markdown(f'<section class="hero"><div class="eyebrow"><i></i> {t("admin_eyebrow")}</div><h1 class="hero-title">{t("admin")}</h1><p class="hero-copy">{t("admin_copy")}</p></section>', unsafe_allow_html=True)
    if not st.session_state.admin_authenticated:
        with st.form("admin_login"):
            password = st.text_input(t("password"), type="password")
            login = st.form_submit_button(t("login"), use_container_width=True)
        if login:
            if password == "admin123":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error(t("bad_password"))
    else:
        project_map = get_projects()
        project_items = list(project_map.items())
        projects = list(project_map.values())
        total_likes = sum(project.get("likes", 0) for project in projects)
        metric1, metric2 = st.columns(2)
        metric1.metric(t("total_projects"), len(projects))
        metric2.metric(t("total_likes"), total_likes)

        st.markdown(f"### {t('manage_projects')}")
        table_records = [{
            t("project_title"): project["name"],
            t("student"): project["student"],
            t("category"): TRANSLATIONS[LANG]["categories"].get(project["category"], project["category"]),
            t("likes_column"): project["likes"],
            t("date_column"): project["added"],
            t("status"): t("status_approved") if project["status"] == "approved" else t("status_pending"),
        } for project in projects]
        projects_df = pd.DataFrame(table_records, columns=[t("project_title"), t("student"), t("category"), t("likes_column"), t("date_column"), t("status")])
        table_col, action_col = st.columns([2.3, 1], gap="large")
        with table_col:
            st.dataframe(projects_df, use_container_width=True, hide_index=True)
        with action_col:
            if project_items:
                selected_delete_id = st.selectbox(
                    t("choose_project"),
                    options=[project_id for project_id, _ in project_items],
                    format_func=lambda project_id: project_map[project_id]["name"],
                    key="admin_delete_project_id",
                )
                if st.button(t("delete_project"), use_container_width=True, key="start_project_delete"):
                    st.session_state.pending_delete_id = selected_delete_id

                pending_id = st.session_state.get("pending_delete_id")
                if pending_id and pending_id in project_map:
                    st.warning(t("confirm_delete"))
                    confirm_col, cancel_col = st.columns(2)
                    with confirm_col:
                        if st.button(t("confirm"), type="primary", use_container_width=True, key="confirm_project_delete"):
                            delete_project(pending_id)
                            st.session_state.liked_project_ids.discard(pending_id)
                            st.session_state.pop("pending_delete_id", None)
                            st.success(t("deleted"))
                            st.rerun()
                    with cancel_col:
                        if st.button(t("cancel_delete"), use_container_width=True, key="cancel_project_delete"):
                            st.session_state.pop("pending_delete_id", None)
                            st.rerun()
            else:
                st.info(t("empty"))

        st.download_button(
            t("download_csv"),
            data=projects_df.to_csv(index=False).encode("utf-8-sig"),
            file_name=t("csv_filename"),
            mime="text/csv",
            use_container_width=True,
        )

        pending_items = [(project_id, project) for project_id, project in project_items if project["status"] == "pending"]
        st.markdown(f"### {t('pending_projects')}")
        if pending_items:
            for project_id, project in pending_items:
                review_info, approve_col, reject_col = st.columns([5, 1.4, 1.2])
                with review_info:
                    category_label = TRANSLATIONS[LANG]["categories"].get(project["category"], project["category"])
                    st.markdown(f"**{project['name']}**　 ·　 {project['student']}　 ·　 {category_label}　 ·　 {project['added']}")
                    st.caption(project["description"][:220] + ("…" if len(project["description"]) > 220 else ""))
                with approve_col:
                    if st.button(t("approve"), key=f"approve_{project_id}", use_container_width=True):
                        set_project_status(project_id, "approved")
                        st.success(t("approved"))
                        st.rerun()
                with reject_col:
                    if st.button(t("reject"), key=f"reject_{project_id}", type="secondary", use_container_width=True):
                        delete_project(project_id)
                        st.session_state.liked_project_ids.discard(project_id)
                        st.warning(t("rejected"))
                        st.rerun()
                st.markdown('<div class="footer-line" style="margin:10px 0"></div>', unsafe_allow_html=True)
        else:
            st.info(t("empty"))

        category_counts = {}
        for project in projects:
            category_counts[project["category"]] = category_counts.get(project["category"], 0) + 1
        chart_data = [{t("category"): TRANSLATIONS[LANG]["categories"].get(category, category), t("project_count"): count} for category, count in category_counts.items()]
        st.markdown(f"### {t('category_chart')}")
        if chart_data:
            fig = px.pie(chart_data, names=t("category"), values=t("project_count"), hole=0.58,
                         color_discrete_sequence=["#48C8FF", "#9A7BFF", "#64F0C8", "#FFB86B"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font={"family": "Tajawal" if RTL else "Inter", "color": "#F3F7FF"},
                              legend={"orientation": "h", "y": -0.12}, margin={"l": 15, "r": 15, "t": 35, "b": 35})
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info(t("empty"))

        if st.button(t("logout")):
            st.session_state.admin_authenticated = False
            st.rerun()
    st.stop()

st.markdown('<div class="topline"></div>', unsafe_allow_html=True)
header_left, header_right = st.columns([7, 2])
with header_left:
    st.markdown(f'<div class="brand-row"><span class="brand-mark">✦</span><div>{t("brand")}<div class="brand-sub">{t("brand_sub")}</div></div></div>', unsafe_allow_html=True)
with header_right:
    if st.button(t("add_project"), use_container_width=True, key="toggle_add"):
        st.session_state.show_add_form = not st.session_state.get("show_add_form", False)

st.markdown(
    f'<section class="hero"><div class="eyebrow"><i></i> {t("hero_eyebrow")}</div>'
    f'<div class="college-logo-wrap"><img class="college-logo" src="data:image/png;base64,{base64.b64encode(Path(__file__).with_name("logo.png").read_bytes()).decode("ascii")}" alt="College logo"></div>'
    f'<h1 class="hero-title">{t("hero_title")}</h1>'
    f'<p class="hero-copy">{t("hero_copy")}</p>'
    f'<div class="hero-meta"><span class="meta-chip">{t("chip_ideas")}</span><span class="meta-chip">{t("chip_learning")}</span><span class="meta-chip">{t("chip_community")}</span></div></section>',
    unsafe_allow_html=True,
)

st.text_input(t("search_label"), placeholder=t("search_placeholder"), key="search_query", label_visibility="collapsed")

if st.session_state.get("show_add_form", False):
    st.markdown(f'<div class="section-heading">{t("add_heading")}</div><div class="section-caption">{t("add_caption")}</div>', unsafe_allow_html=True)
    with st.form("add_project_form", clear_on_submit=True):
        name = st.text_input(t("field_title"))
        student = st.text_input(t("field_student"))
        name_en = st.text_input(t("field_title_en"))
        student_en = st.text_input(t("field_student_en"))
        category_options = ["ألعاب", "ذكاء اصطناعي", "أمن سيبراني", "تطبيقات"]
        category = st.selectbox(t("field_category"), category_options, format_func=lambda value: TRANSLATIONS[LANG]["categories"][value])
        description = st.text_area(t("field_description"), max_chars=500)
        description_en = st.text_area(t("field_description_en"), max_chars=500)
        url = st.text_input(t("field_url"), placeholder="https://")
        image_url = st.text_input(t("field_image"), placeholder=t("image_placeholder"))
        submit_col, cancel_col = st.columns(2)
        with submit_col:
            submitted = st.form_submit_button(t("submit_project"), use_container_width=True)
        with cancel_col:
            cancelled = st.form_submit_button(t("cancel"), type="secondary", use_container_width=True)
        if cancelled:
            st.session_state.show_add_form = False
            st.rerun()
        if submitted:
            if not name.strip() or not student.strip() or not description.strip():
                st.error(t("required_error"))
            else:
                add_project(
                    name.strip(), student.strip(), category, description.strip(),
                    image_url.strip() or "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85",
                    name_en.strip() or name.strip(), student_en.strip() or student.strip(),
                    description_en.strip() or description.strip(),
                )
                st.session_state.show_add_form = False
                st.session_state.project_submission_notice = True
                st.rerun()

if st.session_state.pop("project_submission_notice", False):
    st.success(t("success_added"))

st.markdown(f'<div style="height:30px"></div><div class="section-heading">{t("discover")}</div><div class="section-caption">{t("discover_caption")}</div>', unsafe_allow_html=True)
filters = ["all", "ألعاب", "ذكاء اصطناعي", "أمن سيبراني", "تطبيقات"]
filter_labels = {"all": t("all"), "ألعاب": t("games"), "ذكاء اصطناعي": t("ai"), "أمن سيبراني": t("cyber"), "تطبيقات": t("apps")}
selected_filter = st.radio(t("filter_label"), filters, format_func=lambda value: filter_labels[value], horizontal=True, label_visibility="collapsed", key="active_filter")
selected_category = None if selected_filter == "all" else selected_filter
query = st.session_state.search_query.strip().casefold()
all_projects = get_projects()
visible_projects = [(key, project) for key, project in all_projects.items()
                    if project["status"] == "approved"
                    if (selected_category is None or project["category"] == selected_category)
                    and query in project["name"].casefold()]

if not visible_projects:
    st.markdown(f'<div class="empty-state">{t("empty")}</div>', unsafe_allow_html=True)
else:
    for row_start in range(0, len(visible_projects), 3):
        cols = st.columns(3, gap="large")
        for col, (key, project) in zip(cols, visible_projects[row_start:row_start + 3]):
            with col:
                st.markdown(
                    f'''<article class="project-card"><div class="card-cover"><img src="{project['image']}" alt="{project['name']}"><span class="cover-index">PROJECT / {row_start + 1 + list(visible_projects).index((key, project)):02d}</span></div>
                    <div class="card-body"><div class="card-top"><div class="card-title">{project['name']}</div><span class="badge">{TRANSLATIONS[LANG]['categories'].get(project['category'], project['category'])}</span></div>
                    <div class="card-desc">{project['description'][:105]}{'…' if len(project['description']) > 105 else ''}</div>
                    <div class="card-foot"><span class="student"><span class="avatar">✦</span>{project['student']}</span><span>{t('featured')}</span></div></div></article>''',
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="card-action">', unsafe_allow_html=True)
                if st.button(t("details"), key=f"details_{key}", use_container_width=True):
                    show_project(key)
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="footer-line"></div><div class="site-footer"><strong>{t("brand")} · {t("sidebar_note")}</strong><br>{t("footer")}</div>', unsafe_allow_html=True)
