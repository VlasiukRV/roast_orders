import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.services.simple_cache import SimpleCache
from app.common.utils import logger

# Google Sheet settings
WORKSHEET = "Roaster Orders"
JSON_KEY_FILE_NAME = "google_service_account_file.json"

# Caches
_sheet_cache = {}
_data_cache = SimpleCache(ttl_seconds=600)
product_cache = SimpleCache(ttl_seconds=600)


def __get_google_sheet(sheet_name):
    """
    Establishes a new connection to the Google Sheet and returns the worksheet by name.

    Args:
        sheet_name (str): The name of the worksheet tab to retrieve.

    Returns:
        gspread.Worksheet: The requested worksheet object.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE_NAME, scope)
    client = gspread.authorize(creds)
    return client.open(WORKSHEET).worksheet(sheet_name)

def __get_sheet(sheet_name: str):
    """
    Returns a cached worksheet object, or loads and caches it if not already present.

    Args:
        sheet_name (str): The name of the worksheet tab to retrieve.

    Returns:
        gspread.Worksheet: The worksheet object.
    """
    if sheet_name in _sheet_cache:
        return _sheet_cache[sheet_name]

    sheet = __get_google_sheet(sheet_name)
    _sheet_cache[sheet_name] = sheet
    return sheet

def append_row_to_sheet(sheet_name: str, row: list):
    """
    Appends a single row to the specified worksheet.

    Args:
        sheet_name (str): Name of the worksheet tab.
        row (list): A list representing the row data to append.
    """
    sheet = __get_sheet(sheet_name)
    sheet.append_row(row)

def get_all_records(sheet_name: str, use_cache: bool = False):
    """
    Retrieves all records from the specified worksheet as a list of dictionaries.

    Args:
        sheet_name (str): Name of the worksheet tab.
        use_cache (bool):
    Returns:
        List[Dict]: List of rows as dictionaries (header -> value).

    """
    if use_cache:
        cached = _data_cache.get(sheet_name)
        if cached is not None:
            return cached

    sheet = __get_sheet(sheet_name)
    result =  sheet.get_all_records()
    if use_cache:
        _data_cache.set(sheet_name, result)

    return result

def append_rows_to_sheet(sheet_name: str, rows: list[list]):
    """
    Appends multiple rows to the specified worksheet in a batch.

    Args:
        sheet_name (str): Name of the worksheet tab.
        rows (list of lists): List of rows to append.
    """
    sheet = __get_sheet(sheet_name)
    sheet.append_rows(rows)

def update_sheet_cell(sheet_name: str, row: int, col: int, value):
    """
    Updates a single cell in the worksheet.

    Args:
        sheet_name (str): Name of the worksheet tab.
        row (int): Row index (1-based).
        col (int): Column index (1-based).
        value (Any): New value to set in the cell.
    """
    sheet = __get_sheet(sheet_name)
    sheet.update_cell(row, col, value)

def find_row_by_value(sheet_name: str, column: str, value):
    """
    Searches for a row in the specified Google Sheet where a given column matches the provided value.

    Args:
        sheet_name (str): The name of the worksheet tab to search.
        column (str): The header name of the column to look in.
        value (Any): The value to search for in the specified column.

    Returns:
        int | None: The 1-based index of the matching row (including +1 for the header row),
                    or None if no match is found.
    """
    records = get_all_records(sheet_name)
    for i, row in enumerate(records):
        if row.get(column) == value:

            return i + 2  # +2 to account for the header row and 1-based indexing
    return None

def read_row(sheet_name: str, row_index: int) -> dict:
    """
    Reads a specific row from the worksheet by its 1-based index.

    Args:
        sheet_name (str): Name of the worksheet tab.
        row_index (int): 1-based index of the row to read.

    Returns:
        list: A list of cell values from the row.
    """
    sheet = __get_sheet(sheet_name)

    headers = sheet.row_values(1)
    row_values = sheet.row_values(row_index)
    return dict(zip(headers, row_values))

def update_row(sheet_name: str, row_index: int, row_values: list):
    """
    Updates an entire row in the specified worksheet with new values.

    Args:
        sheet_name (str): The name of the worksheet tab.
        row_index (int): The 1-based index of the row to update.
        row_values (list): A list of values to write into the row, starting from column A.

    Returns:
        None
    """
    sheet = __get_sheet(sheet_name)
    sheet.update(f"A{row_index}", [row_values])
