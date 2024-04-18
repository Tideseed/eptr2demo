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
all_calls = ss["eptr"].get_available_calls()
missing_calls = [k for k in all_calls if k not in d.keys()]

default_values = {
    "start_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "end_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "se_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
    "date_time": (datetime.now() - timedelta(days=1)).strftime(
        "%Y-%m-%dT%H:00:00+03:00"
    ),
    "period": (datetime.now() - timedelta(days=1)).replace(day=1).strftime("%Y-%m-%d"),
    "org_id": "294",
    "uevcb_id": "3205891",
    "pp_id": "2800",  ## Real Time generation
    "idm_contract_id": "2066419679",  # PH23050120
    "year": "2021",
    "intl_direction": "TRGR",
    "uevcb_name": "AFY",
}

ss["call_data"] = ss.get("call_data", {})


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
    "![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2)"
)
st.markdown(
    "[eptr2](https://www.pypi.org/project/eptr2) Python paketini kullanarak Şeffaflık 2.0 üzerinden istediğiniz API'yi aşağıdaki kodları kullanarak çağırabilirsiniz."
)
st.warning(
    "Demo bütün APIler için örnek çağırma yapılamayabilir. İyileştirme çalışmalarımız devam etmektedir."
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
    try:
        seffaflik_url = ss["call_data"]["help"].get(
            "url", "https://seffaflik.epias.com.tr/transparency"
        )
    except:
        seffaflik_url = "https://seffaflik.epias.com.tr/transparency"

    st.link_button(
        "⚡️ EPİAŞ Şeffaflık",
        url=seffaflik_url,
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

st.selectbox("Veri seti seçin", list(d2.keys()) + missing_calls, key="eptr2_call")

if ss.get("eptr2_call", None) is not None:
    ss["call_data"] = get_call_help(
        d2[ss["eptr2_call"]]["key"]
        if d2.get(ss["eptr2_call"], None) is not None
        else ss["eptr2_call"]
    )
    st.subheader(
        ss["call_data"]["help"]["title"]["tr"]
        if d2.get(ss["eptr2_call"], None) is not None
        else "_(başlık yok)_"
    )
    st.markdown(
        ss["call_data"]["help"]["desc"]["tr"]
        if d2.get(ss["eptr2_call"], None) is not None
        else "_(açıklama yok)_"
    )

    st.subheader("Örnek Kullanım")
    st.code(
        call_code(
            help_d=ss["call_data"],
            key=(
                d2[ss["eptr2_call"]]["key"]
                if d2.get(ss["eptr2_call"], None) is not None
                else ss["eptr2_call"]
            ),
        ),
        language="python",
    )

    st.subheader("API Sonucu")

    get_result = st.button("API Sonucunu Getir")

    if get_result:
        bod_params = call_code(
            help_d=ss["call_data"],
            key=d2[ss["eptr2_call"]]["key"],
            just_body_params=True,
        )

        res = ss["eptr"].call(d2[ss["eptr2_call"]]["key"], **bod_params)
        print(res)
        st.dataframe(res)
        # try:
        #     bod_params = call_code(
        #         help_d=ss["call_data"],
        #         key=d2[ss["eptr2_call"]]["key"],
        #         just_body_params=True,
        #     )

        #     res = ss["eptr"].call(d2[ss["eptr2_call"]]["key"], **bod_params)
        #     print(res)
        #     st.dataframe(res)
        # except Exception as e:
        #     st.warning("Bu API için örnek çağırma yapılamadı.")

# st.divider()
# st.subheader("Debug")
# st.json(ss)
