invalid_test_data = [
    {
        "charge_point_vendor": "vendor123",
        "charge_point_model": "Model123"
    },
    {
        "charge_point_vendor": "Vendor123",
        "charge_point_model": 12345
    },
    {
        "charge_point_vendor": 12345,
        "charge_point_model": 12345
    },
    {
        "charge_point_vendor": "",
        "charge_point_model": ""
    },
    {
        "charge_point_vendor": "",
        "charge_point_model": "Model123"

    },
    {
        "charge_point_vendor": "Vendor123",
        "charge_point_model": ""
    },
    {},
    {
        "charge_point_vendor": "Vendor123",
        "charge_point_model": "Model123",
        "unknownField": "Invalid"
    },
    {
        "charge_point_vendor": 12345,
        "charge_point_model": "",
        "unknownField": 12345
    }
]

