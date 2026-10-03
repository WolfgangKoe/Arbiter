"""Baut `arbitersprung.vsix` aus diesem Ordner."""

import json
import zipfile
from pathlib import Path

ordner = Path(__file__).resolve().parent
dateien = ("package.json", "extension.js", "suche.js")

inhaltstypen = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/Content-Types">'
    '<Default Extension=".json" ContentType="application/json"/>'
    '<Default Extension=".js" ContentType="application/javascript"/>'
    '<Default Extension=".vsixmanifest" ContentType="text/xml"/></Types>'
)

manifest = """<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="{name}" Version="{version}" Publisher="{publisher}"/>
    <DisplayName>{displayName}</DisplayName>
    <Description xml:space="preserve">{description}</Description>
  </Metadata>
  <Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
  <Dependencies/>
  <Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json"
    Addressable="true"/></Assets>
</PackageManifest>
"""


def bauen() -> Path:
    paket = json.loads((ordner / "package.json").read_text(encoding="utf-8"))
    ziel = ordner / "arbitersprung.vsix"
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as archiv:
        archiv.writestr("[Content_Types].xml", inhaltstypen)
        archiv.writestr("extension.vsixmanifest", manifest.format(**paket))
        for name in dateien:
            archiv.write(ordner / name, f"extension/{name}")
    return ziel


if __name__ == "__main__":
    print(bauen())
