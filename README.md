# Olympic Games Data Analysis and Interactive Dashboard

### Exploring Olympic History Through Data, Statistics and Interactive Visualizations

<p align="center">

**An End-to-End Exploratory Data Analysis and Interactive Business Intelligence Project**

Built with Python · Pandas · NumPy · Plotly · Streamlit

</p>

---

## Table of Contents:

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Project Motivation](#-project-motivation)
4. [Project Objectives](#-project-objectives)
5. [Scope of the Project](#-scope-of-the-project)
6. [Dataset Description](#-dataset-description)
7. [Data Dictionary](#-data-dictionary)
8. [Technology Stack](#-technology-stack)
9. [Project Architecture](#-project-architecture)
10. [Data Cleaning and Preprocessing](#-data-cleaning-and-preprocessing)
11. [Exploratory Data Analysis](#-exploratory-data-analysis)
12. [Dashboard Features and Modules](#-dashboard-features-and-modules)
13. [Interactive Features](#-interactive-features)
14. [Analytical Methodologies](#-analytical-methodologies)
15. [Key Performance Indicators](#-key-performance-indicators)
16. [Project Structure](#-project-structure)
17. [Installation and Setup](#-installation-and-setup)
18. [Running the Application](#-running-the-application)
19. [Dashboard Screenshots](#-dashboard-screenshots)
20. [Insights and Analytical Applications](#-insights-and-analytical-applications)
21. [Data Quality Considerations](#-data-quality-considerations)
22. [Limitations](#-limitations)
23. [Future Enhancements](#-future-enhancements)
24. [Learning Outcomes](#-learning-outcomes)
25. [Author](#-author)

---

# 1.Project Overview: 

The **Olympic Games Data Analysis & Interactive Analytics Dashboard** is an end-to-end data analytics project designed to explore, analyze, and visualize historical Summer Olympic Games data.

The project transforms historical Olympic athlete and event records into meaningful statistical insights through data cleaning, preprocessing, exploratory data analysis (EDA), aggregation, and interactive data visualization.

It provides an interactive analytical environment where users can explore Olympic history across different dimensions, including:

- Athlete participation.
- Country and National Olympic Committee (NOC) performance.
- Gold, silver, and bronze medal achievements.
- Sports and sporting events.
- Athlete demographics.
- Physical characteristics of athletes.
- Gender participation patterns.
- Historical Olympic trends.
- Dataset quality and statistical characteristics.

The project features a multi-page Streamlit dashboard containing ten analytical modules, supported by interactive Plotly visualizations and global data filters.

Rather than presenting Olympic statistics as static reports, the application enables users to dynamically explore historical data and investigate different analytical questions.

**Project Type:** Exploratory Data Analysis (EDA), Data Analytics, Data Visualization and Interactive Dashboard Development.

**Domain:** Sports Analytics.

**Dataset Coverage:** Historical Summer Olympic Games records, subject to the coverage of the supplied dataset.

---

# 2.Problem Statement:

The Olympic Games generate a substantial amount of historical data involving athletes, countries, sporting disciplines, events, participation, and medal achievements.

However, this information is distributed across numerous records and dimensions, making it difficult to identify meaningful patterns through raw datasets alone.

Without appropriate data processing and visualization, answering questions such as the following becomes challenging:

- How has athlete participation evolved throughout Olympic history?
- Which countries have achieved the greatest medal success?
- Which athletes have won the most Olympic medals?
- How has female participation changed over time?
- Which sports have experienced significant growth in participation?
- What age groups are most represented among Olympic athletes?
- Are there observable relationships between athletes' height and weight?
- How does sporting participation vary across countries and Olympic editions?

The central problem addressed by this project is:

**How can historical Summer Olympic Games data be transformed into an interactive analytical platform that makes Olympic participation, performance, demographic patterns, and historical trends easier to explore, compare, and understand?**

The project addresses this problem by combining data preprocessing, exploratory analysis, statistical aggregation, and interactive visualization within a unified dashboard.

---

# 3.Project Motivation:

The Olympic Games represent one of the largest and most diverse international sporting events.

Their historical records provide an opportunity to investigate several interesting analytical dimensions:

- International sporting performance.
- Changes in global participation.
- Evolution of different sporting disciplines.
- Representation of male and female athletes.
- Athlete demographic characteristics.
- Country-level sporting achievements.
- Historical patterns across Olympic editions.

This project was undertaken to demonstrate how data analytics can convert large historical datasets into structured information and meaningful visual insights.

It also provides practical experience in developing a complete Python-based analytics application, from raw data ingestion to interactive dashboard presentation.

---

# 4.Project Objectives:

The primary objectives are:

### Data Management and Preparation

- Load and inspect historical Olympic datasets.
- Understand dataset structure and variable relationships.
- Identify missing values and duplicate records.
- Clean and standardize relevant data fields.
- Integrate athlete event records with country/NOC information.
- Prepare structured data for analysis.

### Exploratory Data Analysis

- Investigate historical athlete participation.
- Analyze country-level medal achievements.
- Examine sports and event distributions.
- Study athlete age distributions.
- Explore height and weight characteristics.
- Analyze male and female participation trends.
- Identify historical patterns and variations.

### Data Visualization

- Develop informative statistical visualizations.
- Use appropriate chart types for different analytical questions.
- Create interactive charts with Plotly.
- Present important statistics through KPI cards.
- Improve the readability and usability of analytical results.

### Application Development

- Build a multi-page Streamlit dashboard.
- Implement reusable data-processing functions.
- Introduce global filters for interactive exploration.
- Organize analytical modules into a structured interface.
- Develop a consistent visual design system.

---

# 5. 🔍 Scope of the Project

The project focuses on the analysis of historical Summer Olympic Games data.

Its analytical scope includes:

| Analytical Dimension | Coverage |
|---|---|
| Historical analysis | Olympic editions and years |
| Athlete analysis | Athlete participation and demographics |
| Country analysis | Country/NOC participation and performance |
| Medal analysis | Gold, silver, bronze and total medals |
| Sports analysis | Sports and sporting events |
| Age analysis | Athlete age distribution |
| Physical analysis | Height and weight |
| Gender analysis | Male and female participation |
| Data quality | Missing values, duplicates and dataset characteristics |

The application primarily performs descriptive and exploratory analysis.

It is not intended to predict future Olympic medal winners or establish causal relationships between athlete characteristics and sporting performance.

---

# 6.Dataset Description:

The project uses two CSV datasets:

### 6.1 Athlete Events Dataset

**File:** `athlete_events.csv`

This dataset contains athlete-level participation records associated with Olympic editions, including information about athletes, sports, events, countries/NOCs, and medal achievements.

It serves as the primary dataset for the project's analytical operations.

### 6.2 NOC Regions Dataset

**File:** `noc_regions.csv`

This dataset provides country or regional information associated with National Olympic Committee codes.

It is used to enrich the athlete event dataset with readable country/region names.

### Dataset Integration

The two datasets are integrated using the NOC identifier.

This allows the application to perform country-level analysis using readable country or region names rather than relying exclusively on NOC codes.

**Note:** The exact dataset source, original publisher, download URL, version, record count, and redistribution licence should be documented here once verified against the original dataset files and their source. These details should not be assumed.

---

# 7.Data Dictionary:

The athlete event dataset contains several analytical variables.

| Variable | Description |
|---|---|
| ID | Unique athlete identifier |
| Name | Athlete name |
| Sex | Athlete gender code |
| Age | Athlete age |
| Height | Athlete height |
| Weight | Athlete weight |
| Team | Team or participating delegation |
| NOC | National Olympic Committee code |
| Games | Olympic edition |
| Year | Year of the Olympic Games |
| Season | Olympic season |
| City | Host city |
| Sport | Sporting discipline |
| Event | Specific sporting event |
| Medal | Medal achievement |

The NOC regions dataset contains the information used to associate NOC codes with readable country or regional names.

*Note: The table describes the analytical fields used by the application. Actual column availability and missingness depend on the supplied dataset.*

---

# 8.Technology Stack:

The project uses the following technologies and Python libraries.

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation, cleaning and aggregation |
| NumPy | Numerical operations and data processing |
| Plotly Express | Interactive data visualizations |
| Streamlit | Interactive web application and dashboard |
| Matplotlib | Statistical visualization support |
| Seaborn | Statistical data visualization support |
| Git | Version control |
| GitHub | Source code management and project hosting |

### Why These Technologies?

**Python**

Provides a flexible programming environment for data analysis and application development.

**Pandas**

Enables efficient data loading, cleaning, transformation, grouping, aggregation, and analysis.

**NumPy**

Supports numerical operations and data processing.

**Plotly Express**

Creates interactive charts that allow users to explore data through hovering, zooming, and chart interactions.

**Streamlit**

Makes it possible to build an interactive multi-page-style analytics application directly using Python.

**Git and GitHub**

Provide version control, code history, collaboration support, and public project presentation.

---

# 9.Project Architecture:

The application follows a structured data analytics workflow.

```text
             RAW DATASETS
                   |
          +--------+--------+
          |                 |
   athlete_events.csv   noc_regions.csv
          |                 |
          +--------+--------+
                   |
             DATA INGESTION
                   |
          DATA VALIDATION
                   |
         DATA CLEANING
                   |
       DATA TRANSFORMATION
                   |
          DATA INTEGRATION
          (NOC-based merge)
                   |
         CLEANED DATAFRAME
                   |
       ANALYTICAL PROCESSING
                   |
       +-----------+-----------+
       |           |           |
    Athlete     Medal       Country
    Analysis   Analysis     Analysis
       |           |           |
       +-----------+-----------+
                   |
        INTERACTIVE FILTERS
                   |
        PLOTLY VISUALIZATIONS
                   |
         STREAMLIT DASHBOARD
                   |
          USER INTERACTION
```

### Application Workflow

1. Load the CSV datasets.
2. Validate the expected data structure.
3. Remove exact duplicate records.
4. Filter records to Summer Olympic Games.
5. Integrate NOC region information.
6. Normalize and prepare relevant fields.
7. Handle missing values in essential variables.
8. Convert numerical fields to appropriate data types.
9. Generate analytical datasets and aggregations.
10. Apply interactive dashboard filters.
11. Render metrics, charts, tables, and insights.

---

# 10.Data Cleaning and Preprocessing:

Data preprocessing is an important component of the project because the quality of analytical results depends on the quality of the input data.

The application performs several preparation operations.

### 10.1 Data Loading

The datasets are loaded from the project's local `data` directory using Pandas.

### 10.2 Data Validation

The application checks for the presence of required columns before proceeding with analysis.

This helps identify structural problems in the supplied datasets.

### 10.3 Duplicate Removal

Exact duplicate records are removed to reduce unintended duplication during analysis.

### 10.4 Season Filtering

The analytical dataset is restricted to Summer Olympic Games.

This ensures consistency across the dashboard's historical comparisons.

### 10.5 Dataset Integration

The athlete events dataset is merged with the NOC regions dataset using the NOC identifier.

A many-to-one merge validation is used to help prevent unintended multiplication of athlete event records.

### 10.6 Missing Value Handling

The preprocessing workflow:

- Handles missing country/region information using the available NOC code as a fallback.
- Removes records missing essential fields required by the analytical workflow.
- Preserves medal participation information by representing missing medal values as `No Medal`.
- Retains optional athlete characteristics where possible for analyses that do not require those fields.

### 10.7 Data Type Conversion

Numerical fields such as age, height, weight, and year are converted into appropriate numerical representations.

### 10.8 Text Standardization

Relevant text fields are stripped of unnecessary surrounding whitespace.

### 10.9 Analytical Data Preparation

Additional data transformations and aggregations are performed for individual dashboard modules.

The cleaned dataset becomes the foundation for subsequent analysis.

---

# 11.Exploratory Data Analysis:

Exploratory Data Analysis is used to understand the structure, distribution, and characteristics of historical Olympic records.

The project investigates several analytical dimensions:

### Athlete Participation Analysis

- Number of participating athletes.
- Unique athlete counts.
- Participation across Olympic editions.
- Participation across countries and sports.

### Medal Analysis

- Gold medal achievements.
- Silver medal achievements.
- Bronze medal achievements.
- Total medal achievements.
- Country-level medal comparisons.

### Sports and Events Analysis

- Distribution of sports.
- Number of sporting events.
- Historical sporting participation.
- Sport-level participation patterns.

### Demographic Analysis

- Athlete age distribution.
- Gender representation.
- Participation patterns across demographic groups.

### Physical Characteristics Analysis

- Athlete height distribution.
- Athlete weight distribution.
- Relationship between height and weight.

### Country-Level Analysis

- Country participation.
- Medal achievements.
- Sporting representation.
- Historical performance comparisons.

---

# 12.Dashboard Features and Analytical Modules:

The dashboard contains ten analytical modules.

## 12.1 Dashboard Overview

Provides a high-level summary of the selected Olympic data.

**Key components:**

- Total athletes.
- Participating countries/NOCs.
- Number of sports.
- Number of events.
- Medal entries.
- Medal distribution.
- Top medal-winning countries.
- Athlete participation trends.

**Purpose:** Give users an immediate understanding of the selected Olympic dataset.

## 12.2 Medal Tally

Provides a detailed analysis of Olympic medal achievements.

**Key components:**

- Gold medal counts.
- Silver medal counts.
- Bronze medal counts.
- Total medal counts.
- Country-wise medal comparison.
- Historical medal distribution.

**Purpose:** Understand country-level Olympic performance and medal achievements.

## 12.3 Participation Over Time

Examines how athlete participation has evolved throughout Olympic history.

**Key components:**

- Olympic editions.
- Unique athlete participation.
- Country/NOC participation.
- Sport participation.
- Historical participation trends.

**Purpose:** Investigate changes in Olympic participation across different editions.

## 12.4 Most Successful Athletes

Identifies athletes with significant medal achievements.

**Key components:**

- Athlete medal rankings.
- Medal achievement comparisons.
- Sport-wise athlete performance.
- Athlete-level medal records.

**Purpose:** Explore individual sporting achievements and identify historically successful athletes.

## 12.5 Sport Heatmap

Provides a visual comparison of sporting activity across different dimensions.

**Key components:**

- Sports.
- Sporting events.
- Olympic editions.
- Athlete participation.
- Heatmap-based comparisons.

**Purpose:** Identify patterns in sporting participation and event representation.

## 12.6 Athlete Age Distribution

Examines the age characteristics of Olympic athletes.

**Key components:**

- Average athlete age.
- Youngest recorded athlete.
- Oldest recorded athlete.
- Athletes with available age information.
- Age distribution visualization.

**Purpose:** Understand the demographic composition of Olympic participants.

## 12.7 Height vs Weight

Explores the physical characteristics of Olympic athletes.

**Key components:**

- Average athlete height.
- Average athlete weight.
- Number of athletes with available physical data.
- Sport-level comparisons.
- Height-versus-weight visualization.

**Purpose:** Investigate the distribution and relationship of physical characteristics across athletes.

## 12.8 Gender Participation Trend

Studies historical changes in male and female Olympic participation.

**Key components:**

- Male athlete participation.
- Female athlete participation.
- Total athlete participation.
- Olympic editions.
- Gender participation trends.

**Purpose:** Understand the evolution of gender representation in the Summer Olympic Games.

## 12.9 Country Performance

Provides a country-focused analytical view.

**Key components:**

- Country/NOC selection.
- Athlete participation.
- Sporting representation.
- Medal achievements.
- Country-level statistics.

**Purpose:** Examine Olympic participation and performance from an individual country's perspective.

## 12.10 Data Quality & Insights

Provides an overview of dataset characteristics and preprocessing outcomes.

**Key components:**

- Total records.
- Unique athletes.
- Country/NOC coverage.
- Olympic editions.
- Data quality statistics.
- Dataset-level visualizations.

**Purpose:** Help users understand the structure and quality of the underlying analytical data.

---

# 13.Interactive Features:

The dashboard is designed to support dynamic exploration.

### Global Filters

Users can filter the analytical dataset using:

- Year range.
- Country/region.
- Sport.
- Gender.

These filters allow users to investigate different subsets of Olympic history.

Individual modules may use additional logic where a comparison requires a broader dataset than the global selection.

### Interactive Visualizations

Plotly visualizations support:

- Hover-based information.
- Interactive exploration.
- Zooming.
- Panning.
- Dynamic chart interaction.

### Dynamic KPI Cards

Important statistics are displayed through metric cards that respond to the selected data.

### Multi-Page Analytical Navigation

The sidebar provides access to all ten analytical modules.

### Consistent Visual Design

The dashboard uses a navy and gold visual theme, with structured navigation, contrasting typography, and dedicated chart styling.

---

# 14.Analytical Methodologies:

The project uses descriptive analytical techniques.

### Aggregation

Pandas grouping and aggregation operations are used to calculate statistics across:

- Countries.
- Years.
- Sports.
- Events.
- Athletes.
- Medal categories.

### Unique Athlete Analysis

Unique athlete identifiers are used to avoid counting the same athlete multiple times when the objective is to measure the number of distinct participants.

### Medal Aggregation

Medal records are aggregated according to medal category and analytical grouping.

### Team Event Medal Handling

For country-level medal tally calculations, team-event records are deduplicated using a combination of:

- Games.
- Year.
- City.
- NOC.
- Team.
- Sport.
- Event.
- Medal.

This helps avoid counting every member of a medal-winning team as a separate country-level medal achievement.

### Distribution Analysis

Statistical distributions are used to investigate athlete age and physical characteristics.

### Trend Analysis

Year-wise aggregation is used to identify historical changes in participation and performance.

### Comparative Analysis

Country, sport, gender, and athlete-level comparisons are used to explore differences across Olympic dimensions.

---

# 15. 📌 Key Performance Indicators

The dashboard uses several descriptive KPIs.

| KPI | Analytical Meaning |
|---|---|
| Athletes | Number of unique athlete identifiers |
| Countries / NOCs | Number of distinct country/region values |
| Sports | Number of distinct sporting disciplines |
| Events | Number of distinct event names |
| Medal entries | Number of deduplicated medal records where the medal aggregation helper is used |
| Olympic editions | Number of distinct Olympic editions |
| Average age | Mean age among records with available age information |
| Average height | Mean height among records with available height information |
| Average weight | Mean weight among records with available weight information |

**Important analytical distinction:** Athlete participation records, athlete medal achievements, and country-level medal counts are different measures. They should not be treated as interchangeable.

---

# 16.Project Structure:

The repository is organized as follows:

```text
Olympic-Games-Data-Analysis/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
└── data/
    │
    ├── athlete_events.csv
    │
    └── noc_regions.csv
```

| File / Directory | Description |
|---|---|
| `app.py` | Main Streamlit application containing data processing, dashboard logic, and visualizations |
| `requirements.txt` | Python dependency list |
| `README.md` | Project documentation |
| `data/` | Directory containing the input datasets |
| `athlete_events.csv` | Athlete event participation data |
| `noc_regions.csv` | NOC-to-region mapping information |

A local backup file, if maintained, is not required for running the application.

---

# 17.Installation and Setup:

Follow these steps to run the application locally.

## Prerequisites

Ensure that the following are installed:

- Python 3.10 or later (a compatible Python environment is required).
- Git.
- A code editor such as Visual Studio Code.
- Access to the project datasets.

## Step 1: Clone the Repository

```bash
git clone https://github.com/ayushpratapS/Olympic-Games-Data-Analysis.git
```

## Step 2: Navigate to the Project Directory

```bash
cd Olympic-Games-Data-Analysis
```

## Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Step 5: Verify the Dataset Structure

Ensure that the following files exist:

```text
data/athlete_events.csv
data/noc_regions.csv
```

## Step 6: Launch the Dashboard

```bash
python -m streamlit run app.py
```

The application will normally be accessible at:

```text
http://localhost:8501
```

---

# 18.Running the Application:

Once the application starts:

1. Open the local Streamlit URL in a browser.
2. Navigate through the analytical modules using the sidebar.
3. Select a year range.
4. Choose countries or regions.
5. Select sports.
6. Apply gender filters.
7. Explore the KPI cards and interactive charts.
8. Compare different subsets of Olympic history.

The dashboard updates its analytical views based on the applicable selections.

---

# 19.Dashboard Screenshots:

Visual documentation is an important part of understanding the application.

Screenshots will be maintained in the repository under a dedicated directory.

Suggested screenshot structure:

```text
screenshots/
│
├── dashboard_overview.png
├── medal_tally.png
├── participation_over_time.png
├── most_successful_athletes.png
├── sport_heatmap.png
├── athlete_age_distribution.png
├── height_vs_weight.png
├── gender_participation_trend.png
├── country_performance.png
└── data_quality_insights.png
```

### Dashboard Overview

![Dashboard Overview](screenshots/dashboard_overview.png)

### Medal Tally

![Medal Tally](screenshots/medal_tally.png)

### Participation Over Time

![Participation Over Time](screenshots/participation_over_time.png)

*Additional screenshots can be included for the remaining analytical modules.*

---

# 20.Insights and Analytical Applications:

The dashboard provides an environment for investigating several important sports analytics questions.

Examples include:

- Comparing medal achievements between countries.
- Examining the historical growth of athlete participation.
- Investigating changes in female participation.
- Identifying athletes with significant medal achievements.
- Comparing the representation of different sporting disciplines.
- Exploring age distributions across Olympic athletes.
- Studying physical characteristics across sporting categories.
- Understanding the geographical distribution of Olympic participation.

These analytical applications demonstrate how historical sporting data can support descriptive analysis and data-driven exploration.

**Note:** Specific numerical findings and statistical conclusions should be added after validating the corresponding dashboard results.

---

# 21.Data Quality Considerations:

Data quality is important when analyzing historical sporting records.

The project considers several issues:

### Duplicate Records

Exact duplicate rows are removed during preprocessing.

### Missing Values

Some athlete characteristics may not be available for every record.

Analyses involving age, height, and weight therefore depend on the availability of those fields.

### Country and NOC Representation

Country names and NOC codes are not always interchangeable.

The country mapping dataset is used to provide more readable regional labels.

### Team Events

Team-event medals require special consideration because multiple athletes can receive medals for the same event.

The medal aggregation helper accounts for this when calculating country-level medal totals.

### Historical Comparability

The structure and participation patterns of the Olympic Games have changed over time.

Consequently, historical comparisons should be interpreted in the context of the relevant Olympic edition.

---

# 22.Limitations:

The project is primarily descriptive and exploratory.

Some limitations should be considered when interpreting its results:

1. The analysis is restricted to the coverage of the supplied historical Summer Olympic datasets.
2. Missing athlete characteristics may affect demographic and physical analyses.
3. Historical country names and NOC representations may differ across editions.
4. Medal aggregation requires special treatment of team events.
5. Height and weight comparisons do not establish that physical characteristics cause sporting success.
6. Historical participation changes should not automatically be interpreted as changes in global sporting popularity.
7. The application does not currently provide predictive medal forecasting or machine learning-based performance modelling.
8. The completeness and accuracy of conclusions depend on the original dataset's quality and documentation.

---

# 23.Future Enhancements:

The project can be expanded in several directions.

### Advanced Analytics

- Statistical hypothesis testing.
- Correlation analysis.
- Regression analysis.
- Athlete performance comparisons.
- More detailed country-level trend analysis.

### Machine Learning

- Medal prediction models.
- Athlete performance classification.
- Country-level medal forecasting.
- Feature importance analysis.

These would require carefully defined prediction targets and suitable historical training data.

### Dashboard Enhancements

- Additional chart types.
- More detailed drill-down analysis.
- Improved export functionality.
- Advanced country comparisons.
- Dedicated athlete profiles.
- Custom date and edition comparisons.

### Data Engineering

- Automated dataset validation.
- Improved preprocessing pipelines.
- Structured analytical data storage.
- Reusable data transformation modules.
- Automated data quality reporting.

### Deployment

- Public deployment through Streamlit Community Cloud.
- Improved application configuration.
- Deployment documentation.
- Automated dependency and application checks.

---

# 24. 🎓 Learning Outcomes

This project provides practical experience in several areas of data analytics and software development.

### Programming

- Python programming.
- Functions and modular code organization.
- File handling.
- Data structures.
- Error handling.

### Data Analysis

- Data loading and inspection.
- Data cleaning and preprocessing.
- Missing-value handling.
- Duplicate detection.
- Data integration.
- Grouping and aggregation.
- Exploratory Data Analysis.

### Data Visualization

- Statistical chart selection.
- Interactive Plotly visualizations.
- KPI presentation.
- Dashboard layout design.
- Visual storytelling.

### Application Development

- Streamlit application development.
- Interactive filters.
- Sidebar navigation.
- Reusable analytical functions.
- Dashboard styling.

### Development Tools

- Git version control.
- GitHub repository management.
- Python dependency management.
- Local application execution.

---

# 25. 👨‍💻 Author

## Ayush Pratap

**Data Analytics Project | Python | Exploratory Data Analysis | Interactive Dashboard Development**

GitHub: [ayushpratapS](https://github.com/ayushpratapS)

Project Repository:

[Olympic Games Data Analysis](https://github.com/ayushpratapS/Olympic-Games-Data-Analysis)

---

# Acknowledgements and Data Attribution:

This project uses historical Olympic athlete event records and NOC region mapping data.

The original dataset publisher, source URL, and applicable licence should be credited here after verification against the downloaded dataset's original source and terms of use.

All dataset attribution and redistribution conditions should be respected.

---

<p align="center">

**Olympic Games Data Analysis & Interactive Analytics Dashboard**

*Turning historical Olympic records into meaningful data insights.*

</p>