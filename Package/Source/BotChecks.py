import pathlib

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