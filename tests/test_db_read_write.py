from tttg_utils.licensing.license_handler_classes import LicenseHandler

def test_init():
    user_name = 'new_name'
    purchased_months = 2
    license_generator = LicenseHandler()
    new_key = license_generator.generate_new_license_key(user_name, purchased_months)
    assert len(new_key) == 36
    assert True == license_generator.is_valid(user_name)
