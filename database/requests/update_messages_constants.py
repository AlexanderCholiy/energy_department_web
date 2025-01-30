def update_messages_constants(
    message_id: int, constant_type: int, constant_value: str
) -> str:

    part_1 = (f'''
    WITH selected_claim AS (
    SELECT id
    FROM claims
    WHERE claim_number IN (
        SELECT constant_text
        FROM messages_constants
        WHERE constant_type = 2070
        AND message_id = {message_id}
    )
    AND (declarant_id, personal_area_id) IN (
        SELECT declarant_id, personal_area_id
        FROM messages
        WHERE id = {message_id}
    )
    )
    INSERT INTO constants (
        claim_id, constant_type, constant_text, time_stamp
    )
    SELECT
        id,
        1000,
        '{constant_value}',
        CURRENT_TIMESTAMP
    FROM selected_claim
    WHERE EXISTS (SELECT 1 FROM selected_claim)
    ON CONFLICT (claim_id, constant_type)
    DO UPDATE SET
    constant_text = EXCLUDED.constant_text,
    time_stamp = CURRENT_TIMESTAMP;
    ''')

    part_2 = (f'''
    INSERT INTO messages_constants (
        message_id, constant_type, constant_text, time_stamp
    )
    VALUES (
        {message_id}, {constant_type}, '{constant_value}', CURRENT_TIMESTAMP
    )
    ON CONFLICT (message_id, constant_type)
    DO UPDATE SET
        constant_text = EXCLUDED.constant_text,
        time_stamp = CURRENT_TIMESTAMP;
    ''')

    if constant_type == 1000:
        return f'{part_1}\n{part_2}'
    return part_2
