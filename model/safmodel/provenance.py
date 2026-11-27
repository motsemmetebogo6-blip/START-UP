"""
provenance.py – every number in the model carries a provenance tag.

Tags (strongest evidence first):
  MEASURED     – measured plant data (workbook status "Measured" / "Measured mean")
  SUPPLIED     – supplied/confirmed by supervisor (workbook status "Supplied")
  CALIBRATED   – back-solved from plant data (workbook status "Calibrated")
  DERIVED_WB   – derived inside the workbook (workbook status "Derived")
  TARGET       – target value, not an achieved state
  ASSUMED      – assumption (workbook "Assumed", or project assumption register A-xx)
  LITERATURE   – published value (reference register R-xx)
  CALCULATED   – calculated by this model
  PROPOSED     – design value proposed by the project (a decision, not a fact)
"""
from dataclasses import dataclass, field

TAGS = ("MEASURED", "SUPPLIED", "CALIBRATED", "DERIVED_WB", "TARGET",
        "ASSUMED", "LITERATURE", "CALCULATED", "PROPOSED")

WORKBOOK_STATUS_TO_TAG = {
    "measured": "MEASURED", "measured mean": "MEASURED", "measured with model estimates": "MEASURED",
    "supplied": "SUPPLIED", "calibrated": "CALIBRATED", "derived": "DERIVED_WB",
    "target": "TARGET", "assumed": "ASSUMED",
}


@dataclass(frozen=True)
class Q:
    """A quantity with value, unit and provenance."""
    name: str
    value: float
    unit: str
    tag: str
    source: str = ""
    note: str = ""

    def __post_init__(self):
        if self.tag not in TAGS:
            raise ValueError(f"unknown provenance tag {self.tag!r} for {self.name}")

    def __float__(self):
        return float(self.value)


@dataclass
class Record:
    """An output row: scenario, metric, value, unit, tag, equation, note."""
    scenario: str
    metric: str
    value: float
    unit: str
    tag: str = "CALCULATED"
    equation: str = ""
    note: str = ""
    inputs: list = field(default_factory=list)

    def row(self):
        return [self.scenario, self.metric, self.value, self.unit, self.tag, self.equation, self.note,
                ";".join(self.inputs)]


RECORD_HEADER = ["scenario", "metric", "value", "unit", "provenance", "equation", "note", "input_tags"]
