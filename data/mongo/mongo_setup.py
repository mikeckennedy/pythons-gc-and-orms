import mongoengine


def global_init(server='localhost', port=27017, username=None, password=None, use_ssl=False):
    connect_via_alias('core', 'mongo_gc_test', password, port, server, use_ssl, username)


def connect_via_alias(alias, db, password, port, server, use_ssl, username):
    if username or password:
        data = dict(
            username=username,
            password=password,
            host=server,
            port=port,
            authentication_source='admin',
            authentication_mechanism='SCRAM-SHA-1',
            ssl=True,
            tlsAllowInvalidCertificates=True)
    else:
        data = dict(
            host=server,
            port=port,
            ssl=use_ssl,
            tlsAllowInvalidCertificates=True)

    mongoengine.register_connection(alias=alias, name=db, **data)
