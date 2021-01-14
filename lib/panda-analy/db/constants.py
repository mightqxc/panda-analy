import enum

class JobState(enum.Enum):
    FINISHED = 'FINISHED'
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    CANCEL = 'CANCEL'

