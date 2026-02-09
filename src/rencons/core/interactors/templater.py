from pathlib import Path
from random import randint
from typing import TypedDict, cast

from docxtpl import DocxTemplate


class WelderNaksAttestationRequestBase(TypedDict):
    profTraining: str
    specialTraining: str
    method: str
    gtds: str
    nds: str
    materials: str
    detailTypes: str
    jointTypes: str
    connectionTypes: str
    thikness: str
    diameter: str
    positions: str
    weldingMaterials: str


class WelderNaksAttestationRequestTemplateData(WelderNaksAttestationRequestBase):
    id: str


class WelderNaksAttestationRequestData(WelderNaksAttestationRequestBase):
    template_id: str | None
    attestationType: str


class PersonalData(TypedDict):
    name: str
    birthday: str
    expAge: str
    passNumber: str
    issuePlace: str
    issueDate: str
    regAdress: str
    nation: str

    requests: list[WelderNaksAttestationRequestData]


class WelderNaksAttesttaionConfig(TypedDict):
    ac: str
    requestDate: str
    templates: list[WelderNaksAttestationRequestTemplateData]
    personals: list[PersonalData]


class GenerateWelderNaksAttestationRequestsInteractor:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir

    def __call__(self, data: WelderNaksAttesttaionConfig, save_dir: Path):
        for personal in data["personals"]:
            for request in personal["requests"]:
                template = self._get_template(data, request["template_id"])

                request_data = {
                    **template,
                    **request,
                    "requestDate": data["requestDate"],
                }

                doc = self._get_doc(request["attestationType"])

                file_name = f"{personal['name']} {request_data['attestationType']} {request_data['method']}.docx"  # noqa: E501

                context = {**personal, **request_data}

                doc.render(context)

                doc.save(
                    save_dir
                    / f"{personal['passNumber']} {personal['name']}"
                    / file_name
                )

    def _get_template(
        self, data: WelderNaksAttesttaionConfig, template_id: str | None
    ) -> WelderNaksAttestationRequestTemplateData | dict:
        for template in data["templates"]:
            if template["id"] == template_id:
                return template

        return {}

    def _get_doc(self, attestation_type: str) -> DocxTemplate:
        personal_template = (
            self.templates_dir / "personal-naks-request-template.docx"
        )

        if attestation_type in ["П1", "П2"]:
            renewal_template = (
                self.templates_dir / "renewal-personal-naks-request-template.docx"
            )

            if renewal_template.exists():
                return DocxTemplate(renewal_template)

        return DocxTemplate(personal_template)


class GenerateWelderExperienceAgeCertsInteractor:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir

    def __call__(self, data: WelderNaksAttesttaionConfig, save_dir: Path):
        for personal in data["personals"]:
            file_name = f"{personal['name']} experience cert.docx"

            doc = self._get_doc()

            context = personal | {
                "certNumber": randint(100000, 999999),
                "jobTitle": "электрогазосварщик",
                "requestDate": data["requestDate"]
            }

            doc.render(context)

            doc.save(
                save_dir / f"{personal['passNumber']} {personal['name']}" / file_name
            )

    def _get_doc(self) -> DocxTemplate:
        return DocxTemplate(self.templates_dir / "experience-cert-template.docx")


class GenerateWelderNaksAgreementsInteractor:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir

    def __call__(self, data: WelderNaksAttesttaionConfig, save_dir: Path):
        for personal in data["personals"]:
            file_name = f"{personal['name']} naks agreement.docx"

            doc = self._get_doc(data["ac"])

            doc.render(cast(dict, personal))

            doc.save(
                save_dir / f"{personal['passNumber']} {personal['name']}" / file_name
            )

    def _get_doc(self, ac: str) -> DocxTemplate:
        return DocxTemplate(self.templates_dir / f"{ac} welder naks agreement.docx")
