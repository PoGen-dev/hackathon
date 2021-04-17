import pathlib

from .Settings import Settings

class Checks: 
    
    def CheckTypeDocument(FileName: str) -> bool: 
        """
        File should be .fpx or .frx

        :param str FileName: 
        :return bool: 
        """
        Suffix = pathlib.Path(FileName).suffix.lower()
        if Suffix == '.fpx' or Suffix == '.frx': return True
        return False 
    
    def CheckTypeOfIndexDocument(Text: str) -> bool: 
        """
        Text should be only with digit.

        :param str Text:
        :return bool: 
        """
        if Text.isdigit(): 
            return int(Text)
        return False
    
    def CheckRangeOfDocument(UserID: str, Index: int) -> bool:
        """
        History dict shouldn't be empty. Index of document shouldn't
        be out of the range dict.

        :param str UserID:
        :param int Index:
        """
        HistoryDict = Settings.History.get(UserID)
        if HistoryDict: 
            Count = HistoryDict.get(Index) 
            if Count: 
                return True
        return False 

        