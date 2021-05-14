import ip_attribute

assert ip_attribute.IP.ip_normalize('255.255.0.3') == '11111111111111110000000000000011'
assert ip_attribute.IP.ip_standardize('11111111111111110000000000000011') == '255.255.0.3'
assert ip_attribute.IP.ip_normalize_hex('255.255.0.0') == 'ffff0000'