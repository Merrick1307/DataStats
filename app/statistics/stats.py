import pandas as pd


def get_mean(df: pd.DataFrame) -> dict:
    """
    Calculate mean values for each SKU.

    Args:
        df (pd.DataFrame): DataFrame with 'Sku' and 'Value' columns

    Returns:
        dict: Dictionary of SKU to mean value
    """
    mean_series = df.groupby('Sku')['Value'].mean()
    mean_dict = mean_series.to_dict()
    return mean_dict


def get_variance(df: pd.DataFrame) -> dict:
    """
    Calculate variance for each SKU.

    Args:
        df (pd.DataFrame): DataFrame with 'Sku' and 'Value' columns

    Returns:
        dict: Dictionary of SKU to variance value
    """
    variance_series = df.groupby('Sku')['Value'].var()
    variance_dict = variance_series.to_dict()
    return variance_dict


def get_std_dev(df: pd.DataFrame) -> dict:
    """
    Calculate standard deviation for each SKU.

    Args:
        df (pd.DataFrame): DataFrame with 'Sku' and 'Value' columns

    Returns:
        dict: Dictionary of SKU to standard deviation value
    """
    std_series = df.groupby('Sku')['Value'].std()
    std_dict = std_series.to_dict()

    # for sku, std_value in std_dict.items():
    #     print(f"Standard Deviation for {sku} = {std_value:.2f}")

    return std_dict


def get_sigma(df: pd.DataFrame, LSL: dict, USL: dict) -> dict:
    """
    Calculate Sigma values for each SKU using the process capability formula:
    Sigma = min((USL - μ)/σ, (μ - LSL)/σ)

    Args:
        df (pd.DataFrame): DataFrame with 'Sku' and 'Value' columns
        LSL (dict): Dictionary of SKU to Lower Specification Limit
        USL (dict): Dictionary of SKU to Upper Specification Limit

    Returns:
        dict: Dictionary of SKU to Sigma value
    """
    mean_dict = get_mean(df)
    std_dict = get_std_dev(df)
    sigma_dict = {}

    for sku in mean_dict.keys():
        if sku in LSL and sku in USL and sku in std_dict:
            mean = mean_dict[sku]
            std = std_dict[sku]

            if std == 0:  # Avoid division by zero
                print(
                    f"Warning: Standard deviation for {sku} is "
                    f"0, skipping Sigma calculation"
                )
                continue

            sigma_upper = (USL[sku] - mean)
            sigma_lower = (mean - LSL[sku])
            sigma = min(sigma_upper, sigma_lower) / std
            sigma_dict[sku] = sigma

    return sigma_dict