import pandas as pd

from config import DATA_ROOT, MAPPINGS


def consolidation(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Renames the columns of a DataFrame based on a provided mapping.

    Parameters:
    df (pd.DataFrame): The DataFrame to be renamed.
    source (str): The key to access the correct mapping from the MAPPINGS dictionary.

    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    df = df.rename(columns=MAPPINGS[source])
    df = df[MAPPINGS[source].values()]
    return df

def read_data(source: str):
    """
    Reads a CSV file from a specified source and returns it as a pandas DataFrame.

    Parameters:
    source (str): The name of the CSV file (without the .csv extension).

    Returns:
    pd.DataFrame: The data from the CSV file as a pandas DataFrame.
    """
    df = pd.read_csv(f"./{DATA_ROOT}/{source}_reviews.csv")
    return df


def get_weekday(date: pd.Timestamp) -> str:
    """
    Returns the weekday of a given date.

    Parameters:
    date (pd.Timestamp): The date for which the weekday should be determined.

    Returns:
    str: The weekday of the given date.
    """
    return date.strftime("%A")


def contains_source_word(content: str, source: str) -> bool:
    """
    Checks if the source word is present in the content.

    Parameters:
    content (str): The content in which to search for the source word.
    source (str): The word to search for in the content.

    Returns:
    bool: True if the source word is in the content, False otherwise.
    """
    if source in content.lower():
        return True
    else:
        return False


def weigth_likes(likes: str, mean: str):
    """
    Weights the likes by 0.5 if they are greater than the mean.

    Parameters:
    likes (str): The number of likes.
    mean (str): The mean number of likes.

    Returns:
    float: The weighted number of likes.
    """
    if likes > mean:
        return likes * 0.5
    else:
        return likes


def clean(df: pd.DataFrame, run_old_pipeline: bool, source: str) -> pd.DataFrame:
    """
    Cleans the DataFrame by removing duplicates, formatting dates, handling null values,
    adding weekday information, checking if source word is in content, and weighting likes.

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.
    run_old_pipeline (bool): If True, runs the old pipeline, else runs the new pipeline.
    source (str): The source word to check in content.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Remove duplicates
    df = df.drop_duplicates().reset_index(drop=True)
    # Date format
    df["created_date"] = pd.to_datetime(df["created_date"])
    # Null Values
    df = df.dropna(subset=["content"])

    # Get weekday
    if run_old_pipeline:
        df["weekday"] = df["created_date"].apply(get_weekday)
    else:
        df["weekday"] = df["created_date"].dt.day_name()
    # Check if source word in content
    if run_old_pipeline:
        df["contains_source_word"] = df["content"].apply(
            contains_source_word,
            args=[source],
        )
    else:
        df["contains_source_word"] = df["content"].str.lower().str.contains(source)

    # Check if number of likes is greater than the mean and IF than weight it with 0.5
    if run_old_pipeline:
        df["likes_weighted"] = df["likes"].apply(
            weigth_likes, args=[df["likes"].mean()]
        )
    else:
        df["likes_weighted"] = df["likes"]
        df.loc[df["likes"] > df["likes"].mean(), "likes_weighted"] = df[
            "likes_weighted"
        ]
    return df
