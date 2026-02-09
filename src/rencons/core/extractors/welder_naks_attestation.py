from re import findall, sub

from lxml import html

from rencons.core.dto import CertDataDTO


class WelderNaksAttestationPageExtractor:
    def __call__(self, page: str, kleymo: str):
            
        tree: html.HtmlElement = html.fromstring(page)

        tables = tree.xpath("//table")

        main_data_tree: html.HtmlElement = html.fromstring(html.tostring(tables[0]))

        trs: list[html.HtmlElement] = main_data_tree.xpath("//tr")

        exp_date = findall(r"[0-9]{2}.[0-9]{2}.[0-9]{4}", trs[0].text_content())

        if len(exp_date) == 0:
            exp_date = "-"
        else:
            exp_date = exp_date[0]

        name = trs[2].text_content().strip()
        company = trs[3].text_content().strip()
        cert_number = trs[4].text_content().strip()
        method = trs[5].text_content().strip()
        gtds = trs[6].text_content().strip()

        cert_data_tree = html.fromstring(html.tostring(tables[-1]))

        materials = ""
        thikness = ""
        outer_diameter = ""
        detail_diameter = ""
        rod_diameter = ""
        detail_type = ""
        joint_type = ""

        trs: list[html.HtmlElement] = cert_data_tree.xpath("//tr")

        for tr in trs:
            tr: html.HtmlElement = html.fromstring(html.tostring(tr))

            tds: list[html.HtmlElement] = tr.xpath("//td")

            if len(tds) != 2:
                continue

            if "Вид деталей" in tds[0].text_content():
                detail_type = sub(
                    r"[\[\(][A-ZА-Я, \+]+[\]\)]", "", tds[1].text_content()
                ).strip()

            if "Типы швов" in tds[0].text_content():
                joint_type = sub(
                    r"[\[\(][A-ZА-Я, \+]+[\]\)]", "", tds[1].text_content()
                ).strip()

            if "Группа свариваемого материала" in tds[0].text_content():
                materials = sub(
                    r"[\[\(][W0-9 ,\+]+[\]\)]", "", tds[1].text_content()
                ).strip()

            if "Толщина деталей, мм" in tds[0].text_content():
                thikness = tds[1].text_content().strip()

            if "Наружный диаметр, мм" in tds[0].text_content():
                outer_diameter = tds[1].text_content().strip()

            if "Диаметр стержня, мм" in tds[0].text_content():
                rod_diameter = tds[1].text_content().strip()

            if "Диаметр деталей, мм" in tds[0].text_content():
                detail_diameter = tds[1].text_content().strip()

        return CertDataDTO(
            kleymo=kleymo,
            name=name,
            company=company,
            cert_number=cert_number,
            exp_date=exp_date,
            gtds=gtds,
            method=method,
            materials=materials,
            thikness=thikness,
            outer_diameter=outer_diameter,
            detail_diameter=detail_diameter,
            rod_diameter=rod_diameter,
            detail_type=detail_type,
            joint_type=joint_type,
        )
