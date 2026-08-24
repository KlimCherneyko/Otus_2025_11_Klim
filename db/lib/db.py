from datetime import datetime


def create_customer(connection, customer_data: dict) -> int:
    data = {
        "customer_group_id": 1,
        "store_id": 0,
        "language_id": 1,
        "firstname": "",
        "lastname": "",
        "email": "",
        "telephone": "",
        "password": "",
        "custom_field": "",
        "newsletter": 0,
        "ip": "127.0.0.1",
        "status": 1,
        "safe": 0,
        "token": "",
        "code": "",
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    data.update(customer_data)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO oc_customer (
                customer_group_id, store_id, language_id,
                firstname, lastname, email, telephone,
                password, custom_field, newsletter, ip, status, safe,
                token, code, date_added
            ) VALUES (
                %(customer_group_id)s, %(store_id)s, %(language_id)s,
                %(firstname)s, %(lastname)s, %(email)s, %(telephone)s,
                %(password)s, %(custom_field)s, %(newsletter)s, %(ip)s,
                %(status)s, %(safe)s, %(token)s, %(code)s, %(date_added)s
            )
            """,
            data,
        )
        return cursor.lastrowid


def get_customer_by_id(connection, customer_id: int) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM oc_customer WHERE customer_id = %s",
            (customer_id,),
        )
        return cursor.fetchone()


def update_customer(connection, customer_id: int, data: dict) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE oc_customer
            SET firstname = %(firstname)s,
                lastname = %(lastname)s,
                email = %(email)s,
                telephone = %(telephone)s
            WHERE customer_id = %(customer_id)s
            """,
            {
                "customer_id": customer_id,
                "firstname": data["firstname"],
                "lastname": data["lastname"],
                "email": data["email"],
                "telephone": data["telephone"],
            },
        )
        return cursor.rowcount


def delete_customer(connection, customer_id: int) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM oc_customer WHERE customer_id = %s",
            (customer_id,),
        )
        return cursor.rowcount
