def select_pole_from_ts(pole: str) -> str:
    return (f'''
    SELECT ts_id FROM towerstore WHERE ts_id LIKE '{pole}%' LIMIT 2
    ''')
