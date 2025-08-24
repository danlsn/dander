from xml.dom import minidom
from pathlib import Path
from loguru import logger


def pretty_print_xml(xml: str, indent: int = 2):
    reparsed = minidom.parseString(xml)
    return reparsed.toprettyxml(indent=" " * indent)


def get_xml_file_contents(file_path: str, strict: bool = True):
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    if strict and not file_path.suffix == ".xml":
        raise ValueError(f"File is not an XML file: {file_path}")
    with file_path.open() as f:
        return f.read()


def reformat_xml_file(
    file_path: str,
    strict: bool = True,
    indent: int = 2,
    write_file: bool = False,
    verbose: bool = False,
):
    """Reformat an XML file. Optionally write in-place or print to console."""
    import rich

    xml_file_path = Path(file_path)
    if not xml_file_path.is_file():
        raise FileNotFoundError(f"File not found: {xml_file_path}")
    if strict and not xml_file_path.suffix == ".xml":
        raise ValueError(f"File is not an XML file: {xml_file_path}")

    xml_file_content = get_xml_file_contents(file_path, strict=strict)
    xml_data = pretty_print_xml(xml_file_content, indent=indent)
    logger.debug(
        f"Reformatted XML file: {xml_file_path.name} (strict={strict}, indent={indent})"
    )

    if not write_file or verbose:
        logger.debug("Printing formatted XML to console")
        rich.print(xml_data)
    else:
        logger.debug("Writing formatted XML to file in-place")
        xml_file_path.write_text(xml_data)


if __name__ == "__main__":
    file = r"C:\Users\E124584\Downloads\denodo__v_enrol_all__diagram.svg"
    reformat_xml_file(file, strict=False, write_file=True)
