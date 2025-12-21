import pandas as pd
import matplotlib.pyplot as plt


def check_treat_na_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Checking and treating not available values inside a dataframe, dropping if the whole row is not available.
    """
    empty_rows = df.isna().all(axis=1).sum()

    if empty_rows > 0:
        print(f"Detected {empty_rows} empty rows - dropping them.")
        df = df.dropna(how="all")
    else:
        print("Detected no empty rows.")
    return df


def detect_numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Detect numeric columns of a dataframe and return a list of them.
    """
    return list(df.select_dtypes(include="number").columns)


def detect_categorical_columns(df: pd.DataFrame) -> list[str]:
    """
    Detect categorical columns of a dataframe and return a list of them.
    """
    return list(df.select_dtypes(include="object").columns)


def check_duplicate_samples(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect duplicate samples and drop them if so.
    """
    if df.duplicated().any():
        print("Duplicate samples exist!")
        df = df.drop_duplicates()
    else:
        print("No duplicate samples detected!")
    return df


def check_duplicate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check duplicate features - columns.
    We transpose - columns to rows cause for rows we have a method to check duplicated.
    """
    df_transposed = df.T
    if df_transposed.duplicated().any():
        print("Duplicate features exist!")
        df_transposed_cleaned = df_transposed.drop_duplicates()
        return df_transposed_cleaned.T
    else:
        print("No duplicate features detected!")
        return df


def prepare_data(
    df: pd.DataFrame,
    organization_col: str,
    organization_country_mapping: dict[str, str],
    country_to_iso: dict[str, str],
    country_to_continent: dict[str, str],
    rating_col: str | None = None,
    enroll_col: str | None = None,
    success_col: str | None = None,
    bayes_strategy: str | None = None,
    strong_shrinkage: float = 15.0
) -> pd.DataFrame:
    """
    Prepares dataframe for Plotly visualization by mapping organizations to countries
    and aggregating metrics with optional Bayesian shrinkage.
    
    This function performs the following operations:
    1. Maps organizations to countries using provided mappings
    2. Adds ISO codes and continent information
    3. Removes entries that cannot be mapped
    4. Aggregates data by country, calculating course counts and optional metrics
    5. Applies Bayesian shrinkage to success scores if specified

    Returns:
    pd.DataFrame
        Aggregated dataframe with columns:
        - country: Country name
        - iso_alpha: ISO country code
        - continent: Continent name  
        - course_count: Number of courses per country
        - avg_rating: Average rating (if rating_col provided)
        - med_enroll, avg_enroll, total_enroll: Enrollment statistics (if enroll_col provided)
        - avg_success, med_success: Success statistics (if success_col provided)
        - bayes_success: Bayesian-adjusted success score (always calculated when success_col provided)
    
    Notes:
    Bayesian shrinkage helps stabilize estimates for countries with limited data by pulling
    extreme values toward the global average. The amount of shrinkage depends on the evidence
    (enrollment or course count).
    """

    # Create working copy
    df_work = df.copy()

    # Map to countries
    df_work["country"] = df_work[organization_col].map(organization_country_mapping)
    df_work["iso_alpha"] = df_work["country"].map(country_to_iso)
    df_work["continent"] = df_work["country"].map(country_to_continent)

    # Remove unmapped entries
    df_work = df_work.dropna(subset=["country", "iso_alpha", "continent"])

    # Build aggregation using NamedAgg for clear output names
    agg_kwargs = {"course_count": (organization_col, "count")}
    if rating_col:
        agg_kwargs["avg_rating"] = (rating_col, "mean")
    if enroll_col:
        agg_kwargs["med_enroll"] = (enroll_col, "median")
        agg_kwargs["avg_enroll"] = (enroll_col, "mean")
        agg_kwargs["total_enroll"] = (enroll_col, "sum")
    if success_col:
        agg_kwargs["avg_success"] = (success_col, "mean")
        agg_kwargs["med_success"] = (success_col, "median")

    result = (
        df_work.groupby(["country", "iso_alpha", "continent"])
        .agg(**agg_kwargs)
        .reset_index()
    )

    # Apply Bayesian shrinkage to success scores if success column is available
    if success_col and "avg_success" in result.columns:
        global_avg_success = df_work[success_col].mean()
        if bayes_strategy == "bayesian_shrinkage":
            n = result["course_count"].astype(float)
            mu = result["avg_success"].astype(float)
            c = float(strong_shrinkage)
            result["bayes_success"] = (
                (mu * n) + (global_avg_success * c)
            ) / (n + c)

    return result

def course_difficulty_comparison(data: pd.DataFrame, feature: str) -> pd.DataFrame:
    """
    Comparison between features by calculating min, max, mean, std based on given dataframe with course difficulty and feature.
    Afterwards creating a simple boxplot to showcase comparisons.
    """
    genre_statistics: pd.DataFrame = data.groupby("course_difficulty")[
        feature
    ].describe()
    # Box Plot
    plt.subplot(1, 2, 1)
    data.boxplot(column=feature, by="course_difficulty", ax=plt.gca())
    plt.title(f"{feature.capitalize()} - Box Plot")
    plt.suptitle("")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return genre_statistics


def course_certificate_comparison(data: pd.DataFrame, feature: str) -> pd.DataFrame:
    """
    Comparison between features by calculating min, max, mean, std based on given dataframe with course certificate type and feature.
    Afterwards creating a simple boxplot to showcase comparisons.
    """
    genre_statistics: pd.DataFrame = data.groupby("course_Certificate_type")[
        feature
    ].describe()
    # Box Plot
    plt.subplot(1, 2, 1)
    data.boxplot(column=feature, by="course_Certificate_type", ax=plt.gca())
    plt.title(f"{feature.capitalize()} - Box Plot")
    plt.suptitle("")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return genre_statistics


def categorize_course(title):
    """
    We want to categorize the titles based on keywords.
    """
    title_lower = title.lower()

    # Technology & Computer Science keywords
    tech_keywords = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "programming",
        "python",
        "java",
        "javascript",
        "computer",
        "data science",
        "aws",
        "cloud",
        "cybersecurity",
        "security",
        "algorithm",
        "software",
        "tensorflow",
        "android",
        "ios",
        "web development",
        "coding",
        "css",
        "html",
        "sql",
        "database",
        "blockchain",
        "iot",
        "internet of things",
        "google cloud",
        "big data",
        "neural network",
        "deep learning",
        "robotics",
        "automation",
        "devops",
        "agile",
        "scrum",
        "git",
        "unity",
        "mobile app",
        "frontend",
        "backend",
        "api",
        "microservices",
        "containers",
        "kubernetes",
        "networking",
        "it support",
        "system administration",
        "linux",
        "matlab",
        "r programming",
        "statistics programming",
        "data structures",
        "object-oriented",
    ]

    # Business & Management keywords
    business_keywords = [
        "business",
        "management",
        "marketing",
        "finance",
        "accounting",
        "entrepreneurship",
        "leadership",
        "strategy",
        "operations",
        "supply chain",
        "project management",
        "human resources",
        "negotiation",
        "sales",
        "analytics",
        "economics",
        "investment",
        "corporate",
        "fintech",
        "valuation",
        "mergers",
        "acquisitions",
        "venture capital",
        "brand",
        "advertising",
        "pricing",
        "business model",
        "innovation management",
        "organizational",
        "customer",
        "retail",
        "hospitality",
        "logistics",
        "procurement",
        "consulting",
        "change management",
        "performance",
        "quality management",
        "six sigma",
        "lean",
        "agile business",
        "digital transformation",
        "compliance",
        "risk management",
        "audit",
        "financial markets",
        "banking",
        "insurance",
    ]

    # Health & Medicine keywords
    health_keywords = [
        "medical",
        "health",
        "medicine",
        "healthcare",
        "clinical",
        "patient",
        "therapy",
        "nursing",
        "anatomy",
        "physiology",
        "diagnosis",
        "treatment",
        "pharmaceutical",
        "drug",
        "disease",
        "cancer",
        "diabetes",
        "mental health",
        "psychology",
        "psychiatry",
        "epidemiology",
        "public health",
        "nutrition",
        "diet",
        "exercise",
        "wellness",
        "addiction",
        "neuroscience",
        "brain",
        "dental",
        "veterinary",
        "biomedical",
        "genetics",
        "genomics",
        "immunology",
        "microbiology",
        "pathology",
        "radiology",
        "surgery",
        "emergency medicine",
        "pediatrics",
        "geriatrics",
        "rehabilitation",
        "physical therapy",
        "occupational therapy",
        "health informatics",
        "telemedicine",
        "covid",
        "pandemic",
        "infectious disease",
        "vaccine",
        "biostatistics",
    ]

    # Arts & Humanities keywords
    arts_keywords = [
        "art",
        "music",
        "literature",
        "history",
        "philosophy",
        "language",
        "english",
        "writing",
        "creative writing",
        "poetry",
        "novel",
        "journalism",
        "media",
        "film",
        "photography",
        "design",
        "graphic design",
        "fashion",
        "architecture",
        "archaeology",
        "anthropology",
        "cultural",
        "religion",
        "theology",
        "linguistics",
        "foreign language",
        "spanish",
        "french",
        "german",
        "chinese",
        "japanese",
        "korean",
        "russian",
        "arabic",
        "museum",
        "gallery",
        "performing arts",
        "theater",
        "dance",
        "classical",
        "contemporary",
        "medieval",
        "ancient",
        "renaissance",
        "modern art",
        "sculpture",
        "painting",
        "drawing",
        "typography",
        "storytelling",
        "narrative",
        "communication",
        "rhetoric",
    ]

    # Science & Engineering keywords
    science_keywords = [
        "engineering",
        "physics",
        "chemistry",
        "biology",
        "mathematics",
        "calculus",
        "statistics",
        "probability",
        "geometry",
        "algebra",
        "science",
        "research",
        "laboratory",
        "experiment",
        "environmental",
        "sustainability",
        "renewable energy",
        "solar",
        "climate",
        "ecology",
        "geology",
        "astronomy",
        "space",
        "materials",
        "mechanical",
        "electrical",
        "civil",
        "chemical engineering",
        "bioengineering",
        "aerospace",
        "nuclear",
        "petroleum",
        "mining",
        "construction",
        "manufacturing",
        "industrial",
        "systems engineering",
        "control systems",
        "thermodynamics",
        "fluid mechanics",
        "structural",
        "transportation",
        "water",
        "agriculture",
        "food science",
        "biotechnology",
        "nanotechnology",
        "optics",
        "electronics",
        "semiconductors",
        "circuits",
        "power",
        "telecommunications",
        "signal processing",
    ]

    # Social Sciences & Education keywords
    social_keywords = [
        "education",
        "teaching",
        "learning",
        "pedagogy",
        "curriculum",
        "instruction",
        "classroom",
        "student",
        "teacher",
        "school",
        "university",
        "academic",
        "sociology",
        "social",
        "political science",
        "government",
        "policy",
        "law",
        "legal",
        "criminology",
        "international relations",
        "diplomacy",
        "conflict",
        "peace",
        "security",
        "terrorism",
        "migration",
        "refugee",
        "human rights",
        "gender",
        "diversity",
        "inclusion",
        "equity",
        "community",
        "development",
        "poverty",
        "inequality",
        "justice",
        "ethics",
        "moral",
        "welfare",
        "social work",
        "counseling",
        "family",
        "child",
        "youth",
        "aging",
        "gerontology",
        "demography",
        "urban planning",
        "geography",
        "environmental policy",
        "sustainable development",
        "globalization",
        "cultural studies",
        "communication studies",
        "journalism ethics",
    ]

    # Categorize
    if any(keyword in title_lower for keyword in tech_keywords):
        return "Technology & Computer Science"
    elif any(keyword in title_lower for keyword in business_keywords):
        return "Business & Management"
    elif any(keyword in title_lower for keyword in health_keywords):
        return "Health & Medicine"
    elif any(keyword in title_lower for keyword in arts_keywords):
        return "Arts & Humanities"
    elif any(keyword in title_lower for keyword in science_keywords):
        return "Science & Engineering"
    elif any(keyword in title_lower for keyword in social_keywords):
        return "Social Sciences & Education"
    else:
        # Fallback
        if "law" in title_lower or "legal" in title_lower:
            return "Social Sciences & Education"
        elif (
            "finance" in title_lower
            or "economic" in title_lower
            or "money" in title_lower
        ):
            return "Business & Management"
        elif "game" in title_lower and "theory" not in title_lower:
            return "Technology & Computer Science"
        else:
            return "Other"

def tech_vs_nontech(category):
    """
    Function to differentiate between Tech and Non-Tech titles, excluding Other.
    """
    tech_categories = ['Technology & Computer Science', 'Science & Engineering']
    if category in tech_categories:
        return 'Tech'
    elif category == 'Other':
        return 'Other'
    else:
        return 'Non-Tech'