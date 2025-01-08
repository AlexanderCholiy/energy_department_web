class URLS:
    """Список доступных URL"""
    UPTC_PREFIX: str = '/UPTC'
    AVR_PREFIX: str = '/AVR'
    UPTC_CLAIMS: str = '/claims'
    UPTC_APPEALS: str = '/appeals'

    index: str = '/'
    authorize: str = '/authorize'
    token: str = '/token'
    logout: str = '/logout'
    user: str = '/user'

    home_avr: str = AVR_PREFIX
    home_uptc: str = UPTC_PREFIX

    uptc_claims_all: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}'
    uptc_claims_mosoblenergo: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}/mosoblenergo'
    uptc_claims_portal: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}/portal'
    uptc_claims_tatarstan: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}/tatarstan'
    uptc_claims_oboronenergo: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}/oboronenergo'
    uptc_claims_rzd: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}/rzd'
    uptc_claims_rossetimr: str = f'{UPTC_PREFIX}{UPTC_CLAIMS}/rossetimr'

    uptc_appeals_all: str = f'{UPTC_PREFIX}{UPTC_APPEALS}'
    uptc_appeals_portal: str = f'{UPTC_PREFIX}{UPTC_APPEALS}/portal'
    uptc_appeals_oboronenergo: str = (
        f'{UPTC_PREFIX}{UPTC_APPEALS}/oboronenergo'
    )
    uptc_appeals_rossetimr: str = f'{UPTC_PREFIX}{UPTC_APPEALS}/rossetimr'


urls = URLS
