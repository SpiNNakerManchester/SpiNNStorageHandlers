import spinn_utilities.package_loader as package_loader


def test_import_all():
    package_loader.load_module("spinn_storage_handlers")

if __name__ == '__main__':
    test_import_all()
