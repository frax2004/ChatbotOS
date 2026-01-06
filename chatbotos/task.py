

class Task:
  def __init__(self, labels: list[str] = []):
    self.frame: dict[str, Task | str | None] = dict.fromkeys(labels)