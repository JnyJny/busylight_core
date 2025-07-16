"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

src = Path(__file__).parent.parent / "src"
package_name = "busylight_core"

# Define device vendors and their main classes for better organization
VENDOR_INFO = {
    "agile_innovative": ("Agile Innovative", "BlinkStick devices with multi-LED support"),
    "embrava": ("Embrava", "Blynclight series with audio capabilities"),
    "kuando": ("Kuando", "Busylight Alpha and Omega devices"),
    "luxafor": ("Luxafor", "Flag, Mute, Orb, and Bluetooth devices"),
    "thingm": ("ThingM", "Blink(1) devices with fade effects"),
    "muteme": ("MuteMe", "MuteMe devices with button input"),
    "mutesync": ("MuteSync", "MuteSync button devices"),
    "plantronics": ("Plantronics", "Status indicator devices"),
    "compulab": ("CompuLab", "fit-statUSB devices"),
    "busytag": ("BusyTag", "Busy Tag devices"),
    "epos": ("EPOS", "EPOS status devices"),
}

# Build a mapping of all modules as we process them
nav_dict = {}

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()
    # Store in our dict for later use
    nav_dict[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

# Create an index page for the reference section
with mkdocs_gen_files.open("reference/index.md", "w") as index_file:
    index_file.write("# API Reference\n\n")
    index_file.write("**Primary interface for controlling busylights:**\n\n")

    # Main Light class
    light_parts = ("busylight_core", "light")
    if light_parts in nav_dict:
        index_file.write(f"- **[Light Class]({nav_dict[light_parts]})** - Main abstract base class for all busylight devices\n\n")

    index_file.write("## Core Components\n\n")

    # Core modules (excluding light since it's featured above)
    core_modules = [
        ("busylight_core", "Busylight_Core"),
        ("busylight_core.hardware", "Hardware"),
        ("busylight_core.exceptions", "Exceptions"),
        ("busylight_core.settings", "Settings"),
    ]

    for module, display_name in core_modules:
        parts = tuple(module.split("."))
        if parts in nav_dict:
            index_file.write(f"- [{display_name}]({nav_dict[parts]})\n")

    index_file.write("\n## Mixins\n\n")

    # Mixins
    mixin_modules = [
        ("busylight_core.mixins.colorable", "Colorable"),
        ("busylight_core.mixins.taskable", "Taskable"),
    ]

    for module, display_name in mixin_modules:
        parts = tuple(module.split("."))
        if parts in nav_dict:
            index_file.write(f"- [{display_name}]({nav_dict[parts]})\n")

    index_file.write("\n## Hardware Vendors\n\n")

    # Vendor modules - abbreviated for index page
    for vendor_module, (vendor_name, vendor_desc) in VENDOR_INFO.items():
        vendor_parts = ("busylight_core", "vendors", vendor_module)
        if vendor_parts in nav_dict:
            index_file.write(f"### {vendor_name}\n\n")
            index_file.write(f"{vendor_desc}\n\n")

            # Find all submodules for this vendor (limit to prevent overwhelming)
            vendor_submodules = []
            for parts, path in nav_dict.items():
                if (len(parts) >= 4 and
                    parts[0] == "busylight_core" and
                    parts[1] == "vendors" and
                    parts[2] == vendor_module and
                    parts != vendor_parts):

                    # Get the actual class name (last part)
                    class_name = parts[-1]
                    # Convert snake_case to Title Case and clean up
                    display_name = class_name.replace("_", " ").title()
                    if display_name.startswith("Blynclight"):
                        display_name = display_name.replace("Blynclight", "Blynclight ")
                    vendor_submodules.append((display_name, path, parts))

            # Sort and display submodules
            for display_name, path, parts in sorted(vendor_submodules):
                index_file.write(f"- [{display_name}]({path})\n")

            index_file.write("\n")

    index_file.write("## Utilities\n\n")

    # Utility modules
    utility_modules = [
        ("busylight_core.hid", "HID"),
        ("busylight_core.word", "Word"),
    ]

    for module, display_name in utility_modules:
        parts = tuple(module.split("."))
        if parts in nav_dict:
            index_file.write(f"- [{display_name}]({nav_dict[parts]})\n")

# Create custom SUMMARY with better organization
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.write("# API Reference\n\n")

    # Highlight the main Light class first
    nav_file.write("## Main Classes\n\n")
    nav_file.write("**Primary interface for controlling busylights:**\n\n")

    # Main Light class
    light_parts = ("busylight_core", "light")
    if light_parts in nav_dict:
        nav_file.write(f"- **[Light Class]({nav_dict[light_parts]})** - Main abstract base class for all busylight devices\n")

    nav_file.write("\n## Core Components\n\n")

    # Core modules (excluding light since it's featured above)
    core_modules = [
        ("busylight_core", "Busylight_Core"),
        ("busylight_core.hardware", "Hardware"),
        ("busylight_core.exceptions", "Exceptions"),
        ("busylight_core.settings", "Settings"),
    ]

    for module, display_name in core_modules:
        parts = tuple(module.split("."))
        if parts in nav_dict:
            nav_file.write(f"- [{display_name}]({nav_dict[parts]})\n")

    nav_file.write("\n## Mixins\n\n")

    # Mixins
    mixin_modules = [
        ("busylight_core.mixins.colorable", "Colorable"),
        ("busylight_core.mixins.taskable", "Taskable"),
    ]

    for module, display_name in mixin_modules:
        parts = tuple(module.split("."))
        if parts in nav_dict:
            nav_file.write(f"- [{display_name}]({nav_dict[parts]})\n")

    nav_file.write("\n## Hardware Vendors\n\n")

    # Vendor modules
    for vendor_module, (vendor_name, vendor_desc) in VENDOR_INFO.items():
        vendor_parts = ("busylight_core", "vendors", vendor_module)
        if vendor_parts in nav_dict:
            nav_file.write(f"### {vendor_name}\n\n")

            # Find all submodules for this vendor
            vendor_submodules = []
            for parts, path in nav_dict.items():
                if (len(parts) >= 4 and
                    parts[0] == "busylight_core" and
                    parts[1] == "vendors" and
                    parts[2] == vendor_module and
                    parts != vendor_parts):

                    # Get the actual class name (last part)
                    class_name = parts[-1]
                    # Convert snake_case to Title Case and clean up
                    display_name = class_name.replace("_", " ").title()
                    if display_name.startswith("Blynclight"):
                        display_name = display_name.replace("Blynclight", "Blynclight ")
                    vendor_submodules.append((display_name, path, parts))

            # Sort and display submodules
            for display_name, path, parts in sorted(vendor_submodules):
                nav_file.write(f"- [{display_name}]({path})\n")

            nav_file.write("\n")

    nav_file.write("## Utilities\n\n")

    # Utility modules
    utility_modules = [
        ("busylight_core.hid", "HID"),
        ("busylight_core.word", "Word"),
    ]

    for module, display_name in utility_modules:
        parts = tuple(module.split("."))
        if parts in nav_dict:
            nav_file.write(f"- [{display_name}]({nav_dict[parts]})\n")
