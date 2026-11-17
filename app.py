from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Olympic Games Data Analysis",
    page_icon="🏅",
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
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.18);
        padding: 14px;
        border-radius: 10px;
    }
    </style>
    """,
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


# ============================================================
# REUSABLE ANALYSIS FUNCTIONS
# ============================================================

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


def style_chart(fig, height: int = 420):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=25),
        legend_title_text="",
    )
    return fig


def show_table(data: pd.DataFrame, height: int = 420):
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
        height=height,
    )


def no_data(message: str = "No data is available for the current selection."):
    st.info(message)

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
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg",
        width=110,
    )
    st.title("Olympic Data Explorer")
    st.caption("Summer Olympic Games analysis")
    page = st.radio("Select Analysis", PAGES)

    st.divider()
    st.subheader("Global filters")

    first_year = int(df["Year"].min())
    last_year = int(df["Year"].max())

    year_range = st.slider(
        "Olympic year range",
        min_value=first_year,
        max_value=last_year,
        value=(first_year, last_year),
        step=4,
    )

    all_countries = sorted(df["region"].dropna().unique().tolist())
    countries_selected = st.multiselect(
        "Countries",
        all_countries,
        default=[],
        help="Leave empty to include all countries.",
    )

    all_sports = sorted(df["Sport"].dropna().unique().tolist())
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
    st.title("Olympic Games Data Analysis")
    st.write(
        "Explore Summer Olympic participation, countries, sports and "
        "medal-winning performances."
    )

    if filtered_df.empty:
        no_data()
        st.stop()

    medal_rows = medal_event_records(filtered_df)
    athlete_count = filtered_df["ID"].nunique()
    country_count = filtered_df["NOC"].nunique()
    sport_count = filtered_df["Sport"].nunique()
    event_count = (
        filtered_df[["Games", "Sport", "Event"]].drop_duplicates().shape[0]
    )
    medal_count = len(medal_rows)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Athletes", f"{athlete_count:,}")
    m2.metric("Countries / NOCs", f"{country_count:,}")
    m3.metric("Sports", f"{sport_count:,}")
    m4.metric("Events", f"{event_count:,}")
    m5.metric("Medal entries", f"{medal_count:,}")

    st.divider()
    left, right = st.columns(2)

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
            hole=0.5,
            color="Medal",
            color_discrete_map=MEDAL_COLORS,
        )
        st.plotly_chart(style_chart(fig, 360), use_container_width=True)

    with right:
        st.subheader("Top countries by medals")
        tally = make_medal_tally(filtered_df, "region").head(10)
        if tally.empty:
            no_data("No medal records match the selected filters.")
        else:
            fig = px.bar(
                tally.sort_values("Total"),
                x="Total",
                y="region",
                orientation="h",
                color="Total",
                color_continuous_scale="Blues",
                labels={"region": "Country / region", "Total": "Medals"},
            )
            st.plotly_chart(style_chart(fig, 400), use_container_width=True)

    st.subheader("Athlete participation over time")
    yearly = (
        filtered_df.groupby("Year")["ID"]
        .nunique()
        .reset_index(name="Athletes")
    )
    fig = px.line(yearly, x="Year", y="Athletes", markers=True)
    st.plotly_chart(style_chart(fig, 360), use_container_width=True)

    st.caption(
        "Medal totals use deduplicated country/team-event records to avoid "
        "counting a team medal once for every athlete."
    )

# PAGE 2 — MEDAL TALLY

elif page == "Medal Tally":
    st.title("Medal Tally")
    st.write("Compare gold, silver and bronze medals by country or year.")

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
            chart_data = tally.head(15).sort_values("Total")
            fig = px.bar(
                chart_data,
                x="Total",
                y="region",
                orientation="h",
                color="Total",
                color_continuous_scale="Blues",
                labels={"region": "Country / region", "Total": "Medals"},
            )
            st.plotly_chart(style_chart(fig, 500), use_container_width=True)
        else:
            fig = px.line(
                tally.sort_values("Year"),
                x="Year",
                y="Total",
                markers=True,
                labels={"Total": "Medal-winning entries"},
            )
            st.plotly_chart(style_chart(fig, 400), use_container_width=True)

# PAGE 3 — PARTICIPATION OVER TIME

elif page == "Participation Over Time":
    st.title("Participation Over Time")
    st.write(
        "Track the number of athletes, participating countries, sports "
        "and events across Olympic editions."
    )

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
    st.title("Most Successful Athletes")
    st.write("Find athletes with the most medal-winning event performances.")

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
    st.title("Sport Participation Heatmap")
    st.write("Compare the number of events represented in each sport by year.")

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
    st.title("Athlete Age Distribution")
    st.write("Explore the age profile of athletes and medal winners.")

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
    st.title("Height vs Weight")
    st.write("Explore athlete body measurements across different sports.")

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
    st.title("Gender Participation Trend")
    st.write("Compare male and female athlete participation across editions.")

    # Use all genders for this page so the comparison remains visible even
    # when the global gender filter is set to only one category.
    gender_data = df.loc[df["Year"].between(*year_range)].copy()

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
    st.title("Country Performance")
    st.write("Explore medal performance for a selected country or region.")

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

    st.title("Data Quality & Insights")
    st.markdown(
        "Explore the quality, completeness, and reliability "
        "of the Olympic Games dataset."
    )
    st.info(
    "The metrics on this page describe the complete cleaned dataset, "
    "independent of the global sidebar filters."
    )
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



    # Medal distribution - count each country/team event once
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

    st.plotly_chart(fig, use_container_width=True)

    # Dataset preview
    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# FOOTER

st.divider()
st.caption(
    "Olympic Games Data Analysis | Summer Olympic athlete-event dataset. "
    "Figures depend on the selected filters and the records available in the CSV files."
)
