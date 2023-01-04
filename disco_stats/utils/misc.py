from typing import List


async def average(values: List[int]) -> float:
    """Calculate the average of a list of numbers.

    Parameters
    ----------
    values : List[int]
        The list of numbers.

    Returns
    -------
    float
        The average.
    """
    return round(sum(values) / len(values), 2)
