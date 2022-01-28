"""
This module should contain project specific io functionality.

Loading and saving of files should be deferred to this class for easy and consistent file handling between different
sources and to have a single location where file references are held.
"""
import os
import pandas as pd
from statoilds import datalake


class IO:
    local_data_path = '.'

    def __init__(self, local_data_path: str):
        """
        Constructor that can set the data path from where we will access local data..

        Args:
            path: Path to the data folder.
        """
        self.local_data_path = local_data_path

    def load_cleaned_file(self, download_always: bool = True):
        """
        Load the cleaned file, optionally logging into to Azure to download.

        If token is passed then this will only login if token isn't already valid

        Args:
            download_always: Whether to always download the file even if it exists locally

        Returns:
            A dataframe used for logging in and the login token
        """
        local_path = os.path.join(self.local_data_path, self.cleaned_file_local)

        token = datalake.login_and_download_file(self.cleaned_file_remote,
                                                 local_path,
                                                 download_always=download_always)

        df = pd.read_csv(local_path,
                         dtype={'Well_name': 'category'},
                         parse_dates=['start'])
        return df
