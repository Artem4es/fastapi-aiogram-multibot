class ProcessQuestionError(Exception):
    """Error during ALF GPT request"""


class AnotherQuestionProcessing(Exception):
    """Another question from user is already processing"""


class StorageError(Exception):
    """Value is already in storage"""
