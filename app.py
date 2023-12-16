import streamlit as st
from eptr2 import EPTR2
from eptr2.mapping import get_call_help, get_help_d
from datetime import datetime, timedelta

st.set_page_config(
    page_title="eptr2 Demo",
    page_icon="👩‍💻",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


ss = st.session_state

d = get_help_d()
# x = get_call_help()
d2 = {v["title"]["tr"]: {"key": k, **v} for k, v in d.items()}

ss["eptr"] = ss.get("eptr", EPTR2())

default_values = {
    "start_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "end_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "date_time": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:00:00.000"),
    "period": (datetime.now() - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d"),
    "org_id": "294",
    "uevcb_id": "3205891",
    "pp_id": "2800",  ## Real Time generation
    "year": "2021",
    "intl_direction": "TRGR",
}


def call_code(help_d, key, just_body_params=False):
    req_params = help_d["required_body_params"]

    opt_params = help_d["optional_body_params"]
    req_params = req_params + opt_params

    body_param_d = ", ".join(
        [x + "=" + '"' + default_values.get(x, "") + '"' for x in req_params]
    )

    if just_body_params:
        bod_params = {
            x: default_values.get(x, "")
            for x in req_params
            if x in default_values.keys()
        }
        return bod_params

    txt = f"""from eptr2 import EPTR2
eptr = EPTR2()

eptr.call("{key}", {body_param_d})
"""

    return txt


st.title("EPTR2 Demo")
st.markdown(
    "[eptr2](https://www.pypi.org/project/eptr2) Python paketini kullanarak Şeffaflık 2.0 üzerinden istediğiniz API'yi aşağıdaki kodları kullanarak çağırabilirsiniz."
)
col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

with col1:
    st.link_button(
        "✉️ İletişim",
        "https://robokami.com/#iletisim",
        type="primary",
        use_container_width=True,
    )
with col2:
    st.link_button(
        "⚡️ EPİAŞ Şeffaflık",
        ss["call_data"]["help"]["url"],
        type="secondary",
        use_container_width=True,
    )
with col3:
    st.link_button(
        "🔎 Github",
        "https://www.github.com/Tideseed/eptr2",
        use_container_width=True,
    )
with col4:
    st.link_button(
        "🐍 PyPI",
        "https://www.pypi.org/project/eptr2",
        use_container_width=True,
    )

st.selectbox("Veri seti seçin", list(d2.keys()), key="eptr2_call")

if ss.get("eptr2_call", None) is not None:
    ss["call_data"] = get_call_help(d2[ss["eptr2_call"]]["key"])
    st.subheader(ss["call_data"]["help"]["title"]["tr"])
    st.markdown(ss["call_data"]["help"]["desc"]["tr"])

    st.subheader("Örnek Kullanım")
    st.code(
        call_code(help_d=ss["call_data"], key=d2[ss["eptr2_call"]]["key"]),
        language="python",
    )

    st.subheader("API Sonucu")

    get_result = st.button("API Sonucunu Getir")

    if get_result:
        try:
            bod_params = call_code(
                help_d=ss["call_data"],
                key=d2[ss["eptr2_call"]]["key"],
                just_body_params=True,
            )

            res = ss["eptr"].call(d2[ss["eptr2_call"]]["key"], **bod_params)

            st.dataframe(res)
        except Exception as e:
            st.warning("Bu API için örnek çağırma yapılamadı.")

st.divider()
st.subheader("Debug")
st.json(ss)
