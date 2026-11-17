from pathlib import Path
import textwrap
import pandas as pd
import plotly.express as px
import streamlit as st

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Olympic Games Data Analysis",
    page_icon="olympic_rings.svg",
    layout="wide",
)
DATA_DIR = Path(__file__).resolve().parent / "data"
ATHLETE_FILE = DATA_DIR / "athlete_events.csv"
NOC_FILE = DATA_DIR / "noc_regions.csv"

MEDAL_ORDER = ["Gold", "Silver", "Bronze"]
MEDAL_COLORS = {
    "Gold": "#E5B642",
    "Silver": "#A7B0BA",
    "Bronze": "#B87950",
}
st.markdown(
    textwrap.dedent("""
    
    <style>

    /* SIDEBAR FILTER READABILITY */

    /* Filter headings: Country, Year, Sport, Gender */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    }

    /* Selected values in dropdowns */
    [data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #FFFFFF !important;
    }

    /* Dropdown input background */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #263B56 !important;
    border: 1px solid #60758F !important;
    }

    /* Dropdown arrow */
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    }

    /* Year slider labels and values */
    [data-testid="stSidebar"] [data-testid="stSlider"] {
    color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] p,
    [data-testid="stSidebar"] [data-testid="stSlider"] div {
    color: #E2E8F0;
    }   

    /* Gender and other radio options */
    [data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #F1F5F9 !important;
    }

    /* Checkbox labels */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
    color: #F1F5F9 !important;
    }

    /* Dropdown menu options */
    [data-baseweb="popover"] li {
    color: #1E293B !important;
    }



    /* REMOVE EXCESS TOP SPACING */
    [data-testid="stHeader"] {
    background: transparent;
    height: 0;
    }

    [data-testid="stAppViewBlockContainer"] {
    padding-top: 1rem;
    }

    [data-testid="stMainBlockContainer"] {
    padding-top: 1rem;
    }

    /* GLOBAL BACKGROUND */

    .stApp {
    background: linear-gradient(
        135deg,
        #17263D 0%,
        #1D304A 50%,
        #192A41 100%
    );
    color: #F8FAFC;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* HEADINGS */

    h1 {
        color: #F8FAFC !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
    }

    /* METRIC CARDS */

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #263B56, #20344D);
        border: 1px solid #293B55;
        padding: 20px 18px;
        border-radius: 14px;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.20);
        transition: all 0.25s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: #D6A83C;
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(214, 168, 60, 0.12);
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }
    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 800 !important;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #14243A,
        #1B3049
    );
    border-right: 1px solid #405570;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    
    /* SIDEBAR NAVIGATION */

    [data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.035);
    padding: 11px 12px;
    border-radius: 9px;
    margin-bottom: 6px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(214, 168, 60, 0.12);
    border-color: rgba(229, 182, 66, 0.4);
    }

    /* Selected navigation item */

    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        90deg,
        rgba(229, 182, 66, 0.20),
        rgba(229, 182, 66, 0.06)
    );
    border: 1px solid rgba(229, 182, 66, 0.55);
    }

    /* Navigation text */

    [data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #E2E8F0;
    font-weight: 600;
    font-size: 13px;
}
    /* CHART CONTAINER */

    [data-testid="stPlotlyChart"] {
        background: #111D30;
        border: 1px solid #293B55;
        border-radius: 14px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }

    /* TABLES */

    [data-testid="stDataFrame"] {
        border: 1px solid #293B55;
        border-radius: 12px;
        overflow: hidden;
    }

    /* DIVIDERS */

    hr {
        border-color: #293B55 !important;
    }

    /* DOWNLOAD BUTTON */

    .stDownloadButton button {
        background: linear-gradient(90deg, #C99A2E, #E5B642);
        color: #101827;
        border: none;
        border-radius: 8px;
        font-weight: 700;
    }

    .stDownloadButton button:hover {
        background: #F0C75E;
        color: #101827;
        border: none;
    }

    /* INPUTS  */

    [data-baseweb="select"] > div {
        background-color: #17253B;
        border-color: #354761;
        border-radius: 8px;
    }

    </style>
    """).strip(),
    unsafe_allow_html=True,
)

# DATA LOADING AND VALIDATION

@st.cache_data(show_spinner="Loading Olympic datasets...")
def load_data(athlete_path: str, noc_path: str) -> pd.DataFrame:
    """Load, validate and prepare Summer Olympic athlete records."""

    athlete_df = pd.read_csv(athlete_path)
    noc_df = pd.read_csv(noc_path)

    required_athlete_columns = {
        "ID", "Name", "Sex", "Age", "Height", "Weight",
        "Team", "NOC", "Games", "Year", "Season", "City",
        "Sport", "Event", "Medal",
    }
    missing = required_athlete_columns.difference(athlete_df.columns)
    if missing:
        raise ValueError(
            "Missing columns in athlete_events.csv: "
            + ", ".join(sorted(missing))
        )

    required_noc_columns = {"NOC", "region"}
    missing_noc = required_noc_columns.difference(noc_df.columns)
    if missing_noc:
        raise ValueError(
            "Missing columns in noc_regions.csv: "
            + ", ".join(sorted(missing_noc))
        )

    # Avoid multiplying athlete rows if the mapping contains repeated NOC codes.
    noc_df = noc_df[["NOC", "region"]].drop_duplicates(subset=["NOC"]).copy()

    athlete_df = athlete_df.drop_duplicates().copy()
    athlete_df = athlete_df.loc[athlete_df["Season"].eq("Summer")].copy()

    athlete_df = athlete_df.merge(
        noc_df,
        on="NOC",
        how="left",
        validate="many_to_one",
    )

    # Retain records with an unmapped NOC instead of discarding them.
    athlete_df["region"] = athlete_df["region"].fillna(athlete_df["NOC"])

    for column in ["Age", "Height", "Weight", "Year"]:
        athlete_df[column] = pd.to_numeric(athlete_df[column], errors="coerce")

    text_columns = [
        "Name", "Sex", "Team", "NOC", "Games", "City",
        "Sport", "Event", "region",
    ]
    for column in text_columns:
        athlete_df[column] = athlete_df[column].astype("string").str.strip()

    athlete_df = athlete_df.dropna(
        subset=["ID", "Name", "NOC", "Year", "Games", "Sport", "Event"]
    ).copy()
    athlete_df["Year"] = athlete_df["Year"].astype(int)
    athlete_df["Medal"] = athlete_df["Medal"].fillna("No Medal")
    return athlete_df

def get_data() -> pd.DataFrame:
    """Load datasets and show clear setup errors in Streamlit."""

    missing_files = []
    if not ATHLETE_FILE.exists():
        missing_files.append("data/athlete_events.csv")
    if not NOC_FILE.exists():
        missing_files.append("data/noc_regions.csv")

    if missing_files:
        st.error("Dataset file(s) not found: " + ", ".join(missing_files))
        st.info(
            "Your project should contain a `data` folder with both CSV files."
        )
        st.stop()

    try:
        return load_data(str(ATHLETE_FILE), str(NOC_FILE))
    except Exception as error:
        st.error(f"Could not load the Olympic datasets: {error}")
        st.info("Check the CSV files and their column names, then try again.")
        st.stop()

# REUSABLE ANALYSIS FUNCTIONS

def medal_event_records(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return one row per country/team medal-winning event.

    Team-event medals appear on each participating athlete's row in the
    source dataset. Deduplicating at event level avoids counting the same
    team medal once for every athlete.
    """
    medals = data.loc[data["Medal"].isin(MEDAL_ORDER)].copy()

    event_key = [
        "Games", "Year", "City", "NOC", "Team",
        "Sport", "Event", "Medal",
    ]
    return medals.drop_duplicates(subset=event_key)

def make_medal_tally(data: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """Create a medal table using deduplicated event-level medal records."""
    medals = medal_event_records(data)

    columns = [group_column, *MEDAL_ORDER, "Total"]
    if medals.empty:
        return pd.DataFrame(columns=columns)

    tally = (
        medals.pivot_table(
            index=group_column,
            columns="Medal",
            values="Event",
            aggfunc="count",
            fill_value=0,
        )
        .reindex(columns=MEDAL_ORDER, fill_value=0)
        .reset_index()
    )
    tally.columns.name = None

    for medal in MEDAL_ORDER:
        tally[medal] = tally[medal].astype(int)

    tally["Total"] = tally[MEDAL_ORDER].sum(axis=1)
    return tally.sort_values(
        ["Gold", "Silver", "Bronze", "Total"],
        ascending=False,
    ).reset_index(drop=True)

def no_data(message="No data available for the current selection."):
    st.info(message)

def style_chart(fig, height: int = 420):
    fig.update_layout(
        height=height,
        template="plotly_dark",
        paper_bgcolor="#111D30",
        plot_bgcolor="#111D30",
        font=dict(
            family="Arial, sans-serif",
            color="#E2E8F0",
            size=12,
        ),
        title_font=dict(
            color="#F8FAFC",
            size=19,
        ),
        margin=dict(l=35, r=25, t=65, b=40),
        legend_title_text="",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#293B55",
            zerolinecolor="#354761",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#293B55",
            zerolinecolor="#354761",
        ),
    )
    return fig

def show_table(data: pd.DataFrame, height: int = 420):
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
        height=height,
    )

def page_header(title: str, description: str, eyebrow: str = "OLYMPIC ANALYTICS"):
    st.markdown(
        f"""
        <div style="
            margin-bottom: 25px;
            padding: 5px 0 18px 0;
            border-bottom: 1px solid #293B55;
        ">
            <div style="
                color: #E5B642;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2.5px;
                margin-bottom: 9px;
            ">
                {eyebrow}
            </div>
            <div style="
                color: #F8FAFC;
                font-size: 30px;
                font-weight: 800;
                letter-spacing: -0.5px;
                margin-bottom: 7px;
            ">
                {title}
            </div>
            <div style="
                color: #94A3B8;
                font-size: 14px;
                line-height: 1.6;
            ">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# LOAD DATA
df = get_data()
if df.empty:
    st.error("No Summer Olympic records were found in the supplied datasets.")
    st.stop()
 
# SIDEBAR AND GLOBAL FILTERS
PAGES = [
    "Dashboard Overview",
    "Medal Tally",
    "Participation Over Time",
    "Most Successful Athletes",
    "Sport Heatmap",
    "Athlete Age Distribution",
    "Height vs Weight",
    "Gender Participation Trend",
    "Country Performance",
    "Data Quality & Insights",
]

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 15px 5px 22px 5px;
            border-bottom: 1px solid #293B55;
            margin-bottom: 20px;
        ">
            <div style="margin-bottom: 15px; display: flex; justify-content: center;">
    <svg xmlns="http://www.w3.org/2000/svg"
         width="115" height="65" viewBox="0 0 220 120">
        <g fill="none" stroke-width="8">
            <circle cx="48" cy="42" r="29" stroke="#0085C7"/>
            <circle cx="110" cy="42" r="29" stroke="#000000"/>
            <circle cx="172" cy="42" r="29" stroke="#DF0024"/>
            <circle cx="79" cy="78" r="29" stroke="#F4C300"/>
            <circle cx="141" cy="78" r="29" stroke="#009F3D"/>
        </g>
    </svg>
</div>
            <div style="
                color: #F8FAFC;
                font-size: 19px;
                font-weight: 800;
            ">
                OLYMPIC
            </div>
            <div style="
                color: #E5B642;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 3px;
            ">
                DATA EXPLORER
            </div>
            <div style="
                color: #94A3B8;
                font-size: 11px;
                margin-top: 8px;
            ">
                SUMMER GAMES ANALYTICS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="
            color: #E5B642;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 8px;
        ">
            EXPLORE DASHBOARD
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Select Analysis",
        PAGES,
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown(
        """
        <div style="
            color: #E5B642;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            margin: 12px 0 15px 2px;
        ">
            FILTER YOUR DATA
        </div>
        """,
        unsafe_allow_html=True,
    )
    first_year = int(df["Year"].min())
    last_year = int(df["Year"].max())
    year_range = st.slider(
        "Olympic year range",
        min_value=first_year,
        max_value=last_year,
        value=(first_year, last_year),
        step=4,
    )
    all_countries = sorted(
        df["region"].dropna().unique().tolist()
    )
    countries_selected = st.multiselect(
        "Countries",
        all_countries,
        default=[],
        help="Leave empty to include all countries.",
    )
    all_sports = sorted(
        df["Sport"].dropna().unique().tolist()
    )
    sports_selected = st.multiselect(
        "Sports",
        all_sports,
        default=[],
        help="Leave empty to include all sports.",
    )
    genders_selected = st.multiselect(
        "Gender",
        ["Male", "Female"],
        default=["Male", "Female"],
    )

# Apply the global filters to every page.
filtered_df = df.loc[df["Year"].between(*year_range)].copy()
if countries_selected:
    filtered_df = filtered_df.loc[
        filtered_df["region"].isin(countries_selected)
    ]
if sports_selected:
    filtered_df = filtered_df.loc[
        filtered_df["Sport"].isin(sports_selected)
    ]
gender_codes = {"Male": "M", "Female": "F"}
if genders_selected:
    filtered_df = filtered_df.loc[
        filtered_df["Sex"].isin([gender_codes[g] for g in genders_selected])
    ]
else:
    filtered_df = filtered_df.iloc[0:0].copy()

# PAGE 1 — DASHBOARD OVERVIEW

if page == "Dashboard Overview":
    st.html(
    """
<div style="
    background: linear-gradient(120deg, #17253B, #203653);
    padding: 30px 32px;
    border-radius: 18px;
    border: 1px solid #354761;
    border-left: 5px solid #E5B642;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.20);
">
    <div style="
        color: #E5B642;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 3px;
        margin-bottom: 10px;
    ">
        THE OLYMPIC DATA EXPERIENCE
    </div>

    <div style="
        color: #F8FAFC;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 10px;
    ">
        Olympic Games Analytics
    </div>

    <div style="
        color: #B8C7D9;
        font-size: 16px;
        line-height: 1.6;
    ">
        Explore the history of Summer Olympics through athlete
        participation, medal achievements, sporting events
        and country performance.
    </div>
</div>
"""
)

    # CALCULATE DASHBOARD OVERVIEW METRICS

    athlete_count = filtered_df["ID"].nunique()
    country_count = filtered_df["region"].nunique()
    sport_count = filtered_df["Sport"].nunique()
    event_count = filtered_df["Event"].nunique()
    medal_rows = medal_event_records(filtered_df)
    medal_count = len(medal_rows)
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Athletes", f"{athlete_count:,}")
    with m2:
        st.metric("Countries / NOCs", f"{country_count:,}")
    with m3:
        st.metric("Sports", f"{sport_count:,}")
    with m4:
        st.metric("Events", f"{event_count:,}")
    with m5:
        st.metric("Medal entries", f"{medal_count:,}")  
    st.divider()
    st.markdown(
        """
        <div style="margin: 10px 0 18px 2px;">
            <div style="
                color: #E5B642;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
                margin-bottom: 5px;
            ">
                PERFORMANCE ANALYTICS
            </div>
            <div style="
                color: #F8FAFC;
                font-size: 23px;
                font-weight: 750;
            ">
                Olympic Medal Insights
            </div>
            <div style="
                color: #94A3B8;
                font-size: 13px;
                margin-top: 5px;
            ">
                Explore medal distribution and the countries leading the rankings.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Medals by type")
        medal_counts = (
            medal_rows["Medal"]
            .value_counts()
            .reindex(MEDAL_ORDER, fill_value=0)
            .rename_axis("Medal")
            .reset_index(name="Count")
        )
        fig = px.pie(
            medal_counts,
            names="Medal",
            values="Count",
            hole=0.58,
            color="Medal",
            color_discrete_map=MEDAL_COLORS,
            title="Medal Distribution",
        )
        fig.update_traces(
            textinfo="percent+label",
            textfont=dict(size=13, color="#F8FAFC"),
            marker=dict(
                line=dict(color="#111D30", width=3)
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Entries: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            ),
        )
        fig.update_layout(
            annotations=[
                dict(
                    text="<b>MEDALS</b>",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="#E5B642"),
                )
            ]
        )
        st.plotly_chart(style_chart(fig, 360), use_container_width=True) 
        with right:
            st.subheader("Top countries by medals")
            tally = make_medal_tally(filtered_df, "region").head(10)
            if tally.empty:
                no_data("No medal records match the selected filters.")
            else:
                chart_data = tally.sort_values("Total", ascending=True)
                fig = px.bar(
                    chart_data,
                    x="Total",
                    y="region",
                    orientation="h",
                    color="Total",
                    color_continuous_scale=[
                        "#263B57",
                        "#8F7130",
                        "#E5B642",
                    ],
                    text="Total",
                    labels={
                        "region": "Country / region",
                        "Total": "Medals",
                    },
                    title="Top 10 Medal-Winning Countries",
                )
                fig.update_traces(
                    textposition="outside",
                    textfont=dict(color="#F8FAFC", size=12),
                    marker_line_width=0,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Medals: %{x:,}"
                        "<extra></extra>"
                    ),
                )
                fig.update_layout(
                    coloraxis_showscale=False,
                    xaxis_title="Total medals",
                    yaxis_title="",
                    yaxis=dict(
                        showgrid=False,
                        zeroline=False,
                    ),
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#293B55",
                    ),
                )
                st.plotly_chart(
                    style_chart(fig, 420),
                    use_container_width=True,
                )    
        st.markdown(
            """
            <div style="margin: 28px 0 12px 2px;">
                <div style="
                    color: #E5B642;
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 2px;
                    margin-bottom: 5px;
                ">
                    HISTORICAL TRENDS
                </div>
                <div style="
                    color: #F8FAFC;
                    font-size: 23px;
                    font-weight: 750;
                ">
                    Athlete Participation
                </div>
                <div style="
                    color: #94A3B8;
                    font-size: 13px;
                    margin-top: 5px;
                ">
                    Discover how athlete participation has evolved across Olympic editions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        yearly = (
            filtered_df.groupby("Year")["ID"]
            .nunique()
            .reset_index(name="Athletes")
        )
        fig = px.area(
            yearly,
            x="Year",
            y="Athletes",
            title="Athlete Participation Across Olympic Editions",
        )
        fig.update_traces(
            line=dict(
                color="#E5B642",
                width=3,
            ),
            fillcolor="rgba(229, 182, 66, 0.13)",
            mode="lines+markers",
            marker=dict(
                size=7,
                color="#E5B642",
                line=dict(
                    color="#111D30",
                    width=2,
                ),
            ),
            hovertemplate=(
                "<b>Year: %{x}</b><br>"
                "Athletes: %{y:,}"
                "<extra></extra>"
            ),
        )
        fig.update_layout(
            xaxis_title="Olympic Year",
            yaxis_title="Unique Athletes",
        )
        st.plotly_chart(
            style_chart(fig, 400),
            use_container_width=True,
        )
    st.caption(
        "Medal totals use deduplicated country/team-event records to avoid "
        "counting a team medal once for every athlete."
    )

# PAGE 2 — MEDAL TALLY

elif page == "Medal Tally":
    page_header(
    "Medal Tally",
    "Compare gold, silver and bronze medal achievements by country and Olympic year.",
    "MEDAL PERFORMANCE",
)
    if filtered_df.empty:
        no_data()
        st.stop()
    medal_rows = medal_event_records(filtered_df)
    if medal_rows.empty:
        no_data("No medal-winning records match the selected filters.")
        st.stop()
    year_options = sorted(medal_rows["Year"].unique().tolist())
    country_options = sorted(medal_rows["region"].dropna().unique().tolist())
    c1, c2 = st.columns(2)
    year_choice = c1.selectbox("Select Year", ["Overall"] + year_options)
    country_choice = c2.selectbox(
        "Select Country", ["Overall"] + country_options
    )
    view = medal_rows.copy()
    if year_choice != "Overall":
        view = view.loc[view["Year"].eq(year_choice)]
    if country_choice != "Overall":
        view = view.loc[view["region"].eq(country_choice)]
    if country_choice != "Overall" and year_choice == "Overall":
        tally = make_medal_tally(view, "Year")
        st.subheader(f"Year-wise medal tally: {country_choice}")
    else:
        tally = make_medal_tally(view, "region")
        st.subheader("Country medal tally")
    if tally.empty:
        no_data()
    else:
        show_table(tally)
        st.download_button(
            "Download medal tally (CSV)",
            data=tally.to_csv(index=False).encode("utf-8"),
            file_name="olympic_medal_tally.csv",
            mime="text/csv",
        )                
        if "region" in tally.columns:
            chart_data = tally.head(15).sort_values("Total", ascending=True)
            fig = px.bar(
                chart_data,
                x="Total",
                y="region",
                orientation="h",
                color="Total",
                color_continuous_scale=[
                    "#263B57",
                    "#8F7130",
                    "#E5B642",
                ],
                text="Total",
                labels={"region": "Country / region", "Total": "Medals"},
                title="Top 15 Countries by Medal Count",
            )
            fig.update_traces(
                textposition="outside",
                textfont=dict(color="#F8FAFC", size=12),
                marker_line_width=0,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Medals: %{x:,}"
                    "<extra></extra>"
                ),
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Total medals",
                yaxis_title="",
                yaxis=dict(showgrid=False, zeroline=False),
                xaxis=dict(showgrid=True, gridcolor="#293B55"),
            )
            st.plotly_chart(style_chart(fig, 500), use_container_width=True)               
        else:
            chart_data = tally.sort_values("Year")
            fig = px.area(
                chart_data,
                x="Year",
                y="Total",
                title="Medal Performance Across Olympic Years",
            )
            fig.update_traces(
                line=dict(color="#E5B642", width=3),
                fillcolor="rgba(229, 182, 66, 0.13)",
                mode="lines+markers",
                marker=dict(
                    size=8,
                    color="#E5B642",
                    line=dict(color="#111D30", width=2),
                ),
                hovertemplate=(
                    "<b>Year: %{x}</b><br>"
                    "Medal entries: %{y:,}"
                    "<extra></extra>"
                ),
            )
            fig.update_layout(
                xaxis_title="Olympic Year",
                yaxis_title="Total medals",
            )
            st.plotly_chart(style_chart(fig, 420), use_container_width=True)

# PAGE 3 — PARTICIPATION OVER TIME

elif page == "Participation Over Time":
    page_header(
    "Participation Over Time",
    "Track athletes, participating countries, sports and events across Olympic editions.",
    "HISTORICAL TRENDS",
)
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">PARTICIPATION SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Olympic Editions",
        filtered_df["Year"].nunique(),
    )
    metric2.metric(
        "Unique Athletes",
        filtered_df["ID"].nunique(),
    )
    metric3.metric(
        "Countries / NOCs",
        filtered_df["NOC"].nunique(),
    )
    metric4.metric(
        "Sports",
        filtered_df["Sport"].nunique(),
    )
    st.divider()
    if filtered_df.empty:
        no_data()
        st.stop()
    yearly_athletes = (
        filtered_df.groupby("Year")["ID"]
        .nunique()
        .reset_index(name="Athletes")
    )
    yearly_countries = (
        filtered_df.drop_duplicates(["Year", "NOC"])
        .groupby("Year")
        .size()
        .reset_index(name="Countries")
    )
    yearly_sports = (
        filtered_df.drop_duplicates(["Year", "Sport"])
        .groupby("Year")
        .size()
        .reset_index(name="Sports")
    )
    yearly_events = (
        filtered_df.drop_duplicates(["Year", "Sport", "Event"])
        .groupby("Year")
        .size()
        .reset_index(name="Events")
    )
    yearly = yearly_athletes.merge(yearly_countries, on="Year")
    yearly = yearly.merge(yearly_sports, on="Year")
    yearly = yearly.merge(yearly_events, on="Year")
    measure = st.selectbox(
        "Select participation measure",
        ["Athletes", "Countries", "Sports", "Events"],
    )
    fig = px.line(
        yearly,
        x="Year",
        y=measure,
        markers=True,
        title=f"{measure} across Summer Olympic editions",
    )
    st.plotly_chart(style_chart(fig, 430), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Countries over time")
        fig = px.line(yearly, x="Year", y="Countries", markers=True)
        st.plotly_chart(style_chart(fig, 340), use_container_width=True)
    with c2:
        st.subheader("Athletes over time")
        fig = px.line(yearly, x="Year", y="Athletes", markers=True)
        st.plotly_chart(style_chart(fig, 340), use_container_width=True)
    st.subheader("Participation summary")
    show_table(yearly)

# PAGE 4 — MOST SUCCESSFUL ATHLETES

elif page == "Most Successful Athletes":
    page_header(
    "Most Successful Athletes",
    "Discover the athletes who have achieved the most medal-winning performances.",
    "ATHLETE ACHIEVEMENTS",
)
    medal_records = medal_event_records(filtered_df)
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">ATHLETE PERFORMANCE SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Medal-winning Athletes",
        medal_records["ID"].nunique(),
    )
    metric2.metric(
        "Medal Entries",
        len(medal_records),
    )
    metric3.metric(
        "Sports",
        medal_records["Sport"].nunique(),
    )
    metric4.metric(
        "Countries / NOCs",
        medal_records["NOC"].nunique(),
    )
    st.divider()
    if filtered_df.empty:
        no_data()
        st.stop()
    sport_options = ["All Sports"] + sorted(
        filtered_df["Sport"].dropna().unique().tolist()
    )
    chosen_sport = st.selectbox("Choose a Sport", sport_options)
    athlete_medals = filtered_df.loc[
        filtered_df["Medal"].isin(MEDAL_ORDER)
    ].copy()
    if chosen_sport != "All Sports":
        athlete_medals = athlete_medals.loc[
            athlete_medals["Sport"].eq(chosen_sport)
        ]
    athlete_medals = athlete_medals.drop_duplicates(
        subset=["ID", "Games", "Sport", "Event", "Medal"]
    )
    top_athletes = (
        athlete_medals.groupby(["ID", "Name"])
        .size()
        .reset_index(name="Medal records")
        .sort_values("Medal records", ascending=False)
        .head(15)
    )
    if top_athletes.empty:
        no_data("No medal-winning athletes match this selection.")
    else:
        fig = px.bar(
            top_athletes.sort_values("Medal records"),
            x="Medal records",
            y="Name",
            orientation="h",
            hover_data=["ID"],
            labels={"Name": "Athlete"},
        )
        st.plotly_chart(style_chart(fig, 500), use_container_width=True)
        show_table(top_athletes)

# PAGE 5 — SPORT HEATMAP

elif page == "Sport Heatmap":
    page_header(
    "Sport Participation Heatmap",
    "Explore how sporting events have evolved across different Olympic editions.",
    "SPORT ANALYTICS",
)
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">SPORT PARTICIPATION SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Sports",
        filtered_df["Sport"].nunique(),
    )
    metric2.metric(
        "Events",
        filtered_df["Event"].nunique(),
    )
    metric3.metric(
        "Olympic Editions",
        filtered_df["Year"].nunique(),
    )
    metric4.metric(
        "Athletes",
        filtered_df["ID"].nunique(),
    )
    st.divider()
    if filtered_df.empty:
        no_data()
        st.stop()
    heatmap_data = (
        filtered_df[["Year", "Sport", "Event"]]
        .drop_duplicates()
        .pivot_table(
            index="Sport",
            columns="Year",
            values="Event",
            aggfunc="count",
            fill_value=0,
        )
    )
    if heatmap_data.empty:
        no_data()
    else:
        fig = px.imshow(
            heatmap_data,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            labels={
                "x": "Olympic Year",
                "y": "Sport",
                "color": "Events",
            },
        )
        st.plotly_chart(
            style_chart(fig, max(500, 24 * len(heatmap_data))),
            use_container_width=True,
        )

# PAGE 6 — ATHLETE AGE DISTRIBUTION

elif page == "Athlete Age Distribution":
    page_header(
        "Athlete Age Distribution",
        "Explore the age profile of athletes and medal winners.",
        "ATHLETE ANALYTICS",
    )
    age_data = filtered_df.dropna(subset=["Age"])
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">ATHLETE AGE SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Average Age",
        f"{age_data['Age'].mean():.1f}" if not age_data.empty else "N/A",
    )
    metric2.metric(
        "Youngest Athlete",
        f"{age_data['Age'].min():.0f}" if not age_data.empty else "N/A",
    )
    metric3.metric(
        "Oldest Athlete",
        f"{age_data['Age'].max():.0f}" if not age_data.empty else "N/A",
    )
    metric4.metric(
        "Athletes with Age Data",
        age_data["ID"].nunique(),
    )
    st.divider()
    if filtered_df.empty:
        no_data()
        st.stop()
    age_data = filtered_df.dropna(subset=["Age"]).copy()
    age_data = age_data.loc[age_data["Age"].between(10, 90)]
    if age_data.empty:
        no_data("Age information is not available for this selection.")
        st.stop()
    # One row per athlete per Olympic edition/event, rather than one row
    # per athlete across their entire career.
    age_data = age_data.drop_duplicates(
        subset=["ID", "Games", "Sport", "Event"]
    )
    fig = px.histogram(
        age_data,
        x="Age",
        color="Medal",
        barmode="overlay",
        opacity=0.65,
        nbins=35,
        category_orders={"Medal": ["Gold", "Silver", "Bronze", "No Medal"]},
        title="Age distribution by medal status",
    )
    st.plotly_chart(style_chart(fig, 420), use_container_width=True)
    st.subheader("Age summary")
    age_summary = age_data.groupby("Medal")["Age"].agg(
        ["count", "mean", "median", "min", "max"]
    ).reset_index()
    age_summary.columns = [
        "Medal status", "Records", "Average age",
        "Median age", "Youngest", "Oldest",
    ]
    age_summary["Average age"] = age_summary["Average age"].round(1)
    age_summary["Median age"] = age_summary["Median age"].round(1)
    show_table(age_summary)
    st.subheader("Age distribution of gold medalists by sport")
    gold_ages = age_data.loc[age_data["Medal"].eq("Gold")]
    if gold_ages.empty:
        no_data("No gold medalists with recorded ages match these filters.")
    else:
        fig = px.box(
            gold_ages,
            x="Sport",
            y="Age",
            points=False,
            title="Gold medalist ages across sports",
        )
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(style_chart(fig, 550), use_container_width=True)

# PAGE 7 — HEIGHT VS WEIGHT

elif page == "Height vs Weight":
    page_header(
        "Height vs Weight",
        "Explore athlete body measurements across different sports.",
        "PHYSICAL CHARACTERISTICS",
    )
    physical_data = filtered_df.dropna(subset=["Height", "Weight"])
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">ATHLETE PHYSICAL PROFILE</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Athletes with Data",
        physical_data["ID"].nunique(),
    )
    metric2.metric(
        "Average Height",
        f"{physical_data['Height'].mean():.1f} cm"
        if not physical_data.empty else "N/A",
    )
    metric3.metric(
        "Average Weight",
        f"{physical_data['Weight'].mean():.1f} kg"
        if not physical_data.empty else "N/A",
    )
    metric4.metric(
        "Sports Represented",
        physical_data["Sport"].nunique(),
    )
    st.divider()
    if filtered_df.empty:
        no_data()
        st.stop()
    physical_data = filtered_df.dropna(
        subset=["Height", "Weight", "Sport"]
    ).copy()
    # Exclude historical non-competitive demonstration categories where
    # body-measurement comparisons are not useful.
    physical_data = physical_data.loc[
        ~physical_data["Sport"].isin(["Aeronautics", "Alpinism"])
    ]
    if physical_data.empty:
        no_data("No height and weight measurements match these filters.")
        st.stop()
    sport_options = sorted(physical_data["Sport"].unique().tolist())
    selected_sport = st.selectbox("Choose Sport", sport_options)
    plot_data = physical_data.loc[
        physical_data["Sport"].eq(selected_sport)
    ]
    fig = px.scatter(
        plot_data,
        x="Weight",
        y="Height",
        color="Medal",
        symbol="Sex",
        hover_data=["Name", "Team", "Year"],
        color_discrete_map={
            "Gold": MEDAL_COLORS["Gold"],
            "Silver": MEDAL_COLORS["Silver"],
            "Bronze": MEDAL_COLORS["Bronze"],
            "No Medal": "#4C78A8",
        },
        labels={"Weight": "Weight (kg)", "Height": "Height (cm)"},
        title=f"Height vs Weight — {selected_sport}",
    )
    st.plotly_chart(style_chart(fig, 520), use_container_width=True)
    st.caption(
        "Only records with both height and weight measurements are included."
    )

# PAGE 8 — GENDER PARTICIPATION TREND

elif page == "Gender Participation Trend":
    page_header(
        "Gender Participation Trend",
        "Compare male and female athlete participation across editions.",
        "GENDER ANALYTICS",
    )
    # Use all genders for this page so the comparison remains visible even
    # when the global gender filter is set to only one category.  
    gender_data = filtered_df.copy()
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">GENDER PARTICIPATION SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Male Athletes",
        gender_data.loc[gender_data["Sex"] == "M", "ID"].nunique(),
    )
    metric2.metric(
        "Female Athletes",
        gender_data.loc[gender_data["Sex"] == "F", "ID"].nunique(),
    )
    metric3.metric(
        "Total Athletes",
        gender_data["ID"].nunique(),
    )
    metric4.metric(
        "Olympic Editions",
        gender_data["Year"].nunique(),
    )
    st.divider()
    if countries_selected:
        gender_data = gender_data.loc[
            gender_data["region"].isin(countries_selected)
        ]
    if sports_selected:
        gender_data = gender_data.loc[
            gender_data["Sport"].isin(sports_selected)
        ]
    gender_data = gender_data.drop_duplicates(
        subset=["ID", "Year", "Sport", "Event"]
    )
    if gender_data.empty:
        no_data()
        st.stop()
    yearly_gender = (
        gender_data.groupby(["Year", "Sex"])["ID"]
        .nunique()
        .reset_index(name="Athletes")
    )
    yearly_gender = yearly_gender.loc[
        yearly_gender["Sex"].isin(["M", "F"])
    ].copy()
    yearly_gender["Gender"] = yearly_gender["Sex"].map(
        {"M": "Male", "F": "Female"}
    )
    fig = px.line(
        yearly_gender,
        x="Year",
        y="Athletes",
        color="Gender",
        markers=True,
        title="Male and female participation over time",
    )
    st.plotly_chart(style_chart(fig, 450), use_container_width=True)
    pivot = yearly_gender.pivot(
        index="Year", columns="Gender", values="Athletes"
    ).fillna(0).reset_index()
    pivot.columns.name = None
    show_table(pivot)

# PAGE 9 — COUNTRY PERFORMANCE

elif page == "Country Performance":
    page_header(
        "Country Performance",
        "Explore medal performance for a selected country or region.",
        "COUNTRY ANALYTICS",
    )
    country_data = filtered_df.copy()
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">NATIONAL PERFORMANCE SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Countries / NOCs",
        country_data["NOC"].nunique(),
    )
    metric2.metric(
        "Athletes",
        country_data["ID"].nunique(),
    )
    metric3.metric(
        "Sports",
        country_data["Sport"].nunique(),
    )
    metric4.metric(
        "Medal Entries",
        len(medal_event_records(country_data)),
    )

    st.divider()
    if filtered_df.empty:
        no_data()
        st.stop()
    country_options = sorted(filtered_df["region"].dropna().unique().tolist())
    if not country_options:
        no_data("No countries are available for the current filters.")
        st.stop()
    # If a country filter is active, it will naturally appear as the only
    # available choice; otherwise the user can choose any country.
    selected_country = st.selectbox("Choose Country", country_options)
    country_df = filtered_df.loc[
        filtered_df["region"].eq(selected_country)
    ].copy()
    country_medals = medal_event_records(country_df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Athletes", f"{country_df['ID'].nunique():,}")
    c2.metric("Sports", f"{country_df['Sport'].nunique():,}")
    c3.metric("Medal entries", f"{len(country_medals):,}")
    if country_medals.empty:
        no_data("This country has no medal-winning records in the selected range.")
    else:
        yearly_medals = (
            country_medals.groupby(["Year", "Medal"])
            .size()
            .reset_index(name="Medals")
        )
        fig = px.bar(
            yearly_medals,
            x="Year",
            y="Medals",
            color="Medal",
            barmode="stack",
            category_orders={"Medal": MEDAL_ORDER},
            color_discrete_map=MEDAL_COLORS,
            title=f"Medals by year — {selected_country}",
        )
        st.plotly_chart(style_chart(fig, 430), use_container_width=True)
        sport_medals = (
            country_medals.groupby(["Sport", "Medal"])
            .size()
            .reset_index(name="Medals")
        )
        top_sports = (
            sport_medals.groupby("Sport")["Medals"]
            .sum()
            .sort_values(ascending=False)
            .head(12)
            .index
        )
        sport_medals = sport_medals.loc[
            sport_medals["Sport"].isin(top_sports)
        ]
        fig = px.bar(
            sport_medals,
            x="Sport",
            y="Medals",
            color="Medal",
            barmode="stack",
            category_orders={"Medal": MEDAL_ORDER},
            color_discrete_map=MEDAL_COLORS,
            title=f"Medal-winning sports — {selected_country}",
        )
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(style_chart(fig, 470), use_container_width=True)

        country_tally = make_medal_tally(country_df, "region")
        st.subheader("Medal summary")
        show_table(country_tally)
elif page == "Data Quality & Insights":
    page_header(
        "Data Quality & Insights",
        "Explore the quality, completeness, and reliability of the Olympic Games dataset.",
        "DATA QUALITY",
    )
    st.markdown(
        '<div style="color:#E5B642;font-size:11px;'
        'font-weight:700;letter-spacing:2px;'
        'margin-bottom:12px;">DATASET QUALITY SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(
        "Total Records",
        f"{len(df):,}",
    )
    metric2.metric(
        "Unique Athletes",
        f"{df['ID'].nunique():,}",
    )
    metric3.metric(
        "Countries / NOCs",
        f"{df['NOC'].nunique():,}",
    )
    metric4.metric(
        "Olympic Editions",
        f"{df['Year'].nunique():,}",
    )
    st.divider()
    # Dataset metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Unique Athletes", f"{df['ID'].nunique():,}")
    with col3:
        st.metric("Countries", f"{df['region'].nunique():,}")
    with col4:
        st.metric("Olympic Years", f"{df['Year'].nunique():,}")
    st.divider()
    # Missing values
    st.subheader("Missing Values Analysis")
    missing_data = df.isnull().sum().reset_index()
    missing_data.columns = ["Column", "Missing Values"]
    missing_data["Missing Percentage"] = (
        missing_data["Missing Values"] / len(df) * 100
    ).round(2)
    missing_data = missing_data.sort_values(
        by="Missing Percentage",
        ascending=False
    )
    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True
    )
    # Duplicate records
    st.subheader("Duplicate Records")
    duplicate_count = df.duplicated().sum()
    st.metric(
        "Remaining Exact Duplicate Rows",
        f"{duplicate_count:,}"
    )
    st.caption(
        "Exact duplicate rows are removed during data preparation."
    )
    # Medal distribution-count each country/team event once
    st.subheader("Medal Distribution")
    medal_records = medal_event_records(df)
    medal_data = (
        medal_records["Medal"]
        .value_counts()
        .reindex(MEDAL_ORDER, fill_value=0)
        .rename_axis("Medal")
        .reset_index(name="Count")
    )
    fig = px.pie(
        medal_data,
        names="Medal",
        values="Count",
        title="Distribution of Olympic Medals",
        hole=0.4,
        color="Medal",
        color_discrete_map=MEDAL_COLORS,
    )
    st.plotly_chart(
    style_chart(fig, 400),
    use_container_width=True,
    )
    # Dataset preview
    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# FOOTER

st.markdown(
    f"""
    <div style="
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        padding: 12px 16px;
        margin-top: 25px;
        background: rgba(23, 37, 59, 0.75);
        border: 1px solid #293B55;
        border-radius: 10px;
        color: #94A3B8;
        font-size: 12px;
    ">
        <span>📊 Dataset: Summer Olympic Games</span>
        <span>📅 Coverage: {int(df["Year"].min())} – {int(df["Year"].max())}</span>
        <span>🏅 Records: {len(df):,}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    textwrap.dedent("""
    <div style="
        margin-top: 45px;
        padding: 22px 10px;
        border-top: 1px solid #293B55;
        text-align: center;
    ">
        <div style="
            color: #E5B642;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
        ">
            OLYMPIC GAMES ANALYTICS
        </div>
        <div style="
            color: #94A3B8;
            font-size: 12px;
            margin-top: 8px;
        ">
            Exploring Olympic history through data and insights
        </div>
        <div style="
            color: #64748B;
            font-size: 11px;
            margin-top: 6px;
        ">
            Built with Python · Pandas · Plotly · Streamlit
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)