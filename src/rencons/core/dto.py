from dataclasses import dataclass


@dataclass
class CertDataDTO:
    kleymo: str
    name: str
    company: str
    cert_number: str
    exp_date: str
    gtds: str
    method: str
    materials: str
    thikness: str
    outer_diameter: str
    detail_diameter: str
    rod_diameter: str
    detail_type: str
    joint_type: str
