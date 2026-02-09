# rencons-cli

Python CLI for working with NAKS welder data:

- Fetch certificate/attestation details by **kleymo** via Telegram bot `@statnaksbot`
- Append parsed results into an Excel welder registry (`.xlsx`)
- Generate NAKS-related `.docx` documents from JSON + `.docx` templates

The entrypoint is `rencons-cli` (Typer).

## Requirements

- Python `>= 3.13`
- Telegram API credentials (`API_ID`, `API_HASH`) for Telethon features
- `docxtpl` for `.docx` generation

## Install

Using Poetry (recommended):

```bash
poetry install
poetry run rencons-cli --help
```

## Configuration (Telegram)

Create `.env` in the repo root:

```env
API_ID=123456
API_HASH=0123456789abcdef0123456789abcdef0123456789abcdef
```

Notes:

- Don’t commit secrets. `*.env` and `*.session` are ignored by git.
- On first run, Telethon may prompt you to sign in and will create `session.session`.

## Quickstart (end-to-end)

1) Put kleymos into a file (JSON list of strings), e.g. `kleymos.json`:

```json
["A123", "B567"]
```

2) Parse NAKS bot output into structured JSON:

```bash
rencons-cli naks parse-kleymos --input-path kleymos.json --output-path certs.json
```

3) Append results into the registry workbook:

```bash
rencons-cli welder-regitry add-data \
  --data-path certs.json \
  --group "Baltics" \
  --group-key "Baltics 11" \
  --registry-path static/welder-registry.xlsx
```

## Commands

### `status`

```bash
rencons-cli status
```

### `naks parse-kleymos`

```bash
rencons-cli naks parse-kleymos --input-path kleymos.json --output-path certs.json
```

`certs.json` output is a list of objects with fields:

- `kleymo`, `name`, `company`, `cert_number`, `exp_date`
- `gtds`, `method`, `materials`
- `thikness`, `outer_diameter`, `detail_diameter`, `rod_diameter`
- `detail_type`, `joint_type`

### `welder-regitry add-data`

Appends `certs.json` rows into an `.xlsx` workbook (default: `static/welder-registry.xlsx`).

```bash
rencons-cli welder-regitry add-data \
  --data-path certs.json \
  --group "Baltics" \
  --group-key "Baltics 11" \
  --sub-group "-" \
  --save-path out.xlsx
```

Note: the command name is `welder-regitry` (typo preserved in CLI).

### `templater generate-welder-naks-attestation-docs`

Generates `.docx` files into per-welder subfolders inside a directory containing `data.json`.

Example directory in this repo:

- `static/templater-data/welder-naks-attestation/Baltics 1/`

Run:

```bash
rencons-cli templater generate-welder-naks-attestation-docs \
  --dir "static/templater-data/welder-naks-attestation/Baltics 1" \
  --templates-dir static/templates
```

Templates:

- Required:
  - `static/templates/personal-naks-request-template.docx`
  - `static/templates/experience-cert-template.docx`
- Optional (used for attestation types `П1`/`П2` when present):
  - `static/templates/renewal-personal-naks-request-template.docx`

`data.json` shape (simplified):

```json
{
  "requestDate": "DD.MM.YYYY",
  "templates": [
    {
      "id": "t1",
      "profTraining": "",
      "specialTraining": "",
      "method": "",
      "gtds": "",
      "nds": "",
      "materials": "",
      "detailTypes": "",
      "jointTypes": "",
      "connectionTypes": "",
      "thikness": "",
      "diameter": "",
      "positions": "",
      "weldingMaterials": ""
    }
  ],
  "personals": [
    {
      "name": "Иван Иванов",
      "birthday": "DD.MM.YYYY",
      "expAge": "N лет",
      "passNumber": "AB123456",
      "issuePlace": "",
      "issueDate": "DD.MM.YYYY",
      "regAdress": "",
      "nation": "",
      "requests": [{ "attestationType": "Пв", "template_id": "t1" }]
    }
  ]
}
```

## Development

```bash
poetry run ruff check .
poetry run ruff format .
```
