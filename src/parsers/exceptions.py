"""Parser specific exceptions."""

class ParserError(Exception):
    """Base exception for all parser errors."""
    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.message = message
        self.details = details

class FileNotReadableError(ParserError):
    """Exception raised when file cannot be read/opened."""
    pass

class CorruptedFileError(ParserError):
    """Exception raised when file is corrupted or content cannot be parsed."""
    pass

class UnsupportedFormatError(ParserError):
    """Exception raised when file format is not supported."""
    pass

class ParsingLimitExceededError(ParserError):
    """Exception raised when file is too large or has too many elements to parse."""
    pass
