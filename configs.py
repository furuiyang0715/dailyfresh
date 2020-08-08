import configparser
import os

env = os.environ

cf = configparser.ConfigParser()
thisdir = os.path.dirname(__file__)
cf.read(os.path.join(thisdir, '.conf'))

# test
TEST_MYSQL_HOST = env.get("TEST_MYSQL_HOST", cf.get('test', 'TEST_MYSQL_HOST'))
TEST_MYSQL_PORT = int(env.get("TEST_MYSQL_PORT", cf.get('test', 'TEST_MYSQL_PORT')))
TEST_MYSQL_USER = env.get("TEST_MYSQL_USER", cf.get('test', 'TEST_MYSQL_USER'))
TEST_MYSQL_PASSWORD = env.get("TEST_MYSQL_PASSWORD", cf.get('test', 'TEST_MYSQL_PASSWORD'))
TEST_MYSQL_DB = env.get("TEST_MYSQL_DB", cf.get('test', 'TEST_MYSQL_DB'))


if __name__ == "__main__":
    import sys
    mod = sys.modules[__name__]
    attrs = dir(mod)
    attrs = [attr for attr in attrs if not attr.startswith("__") and attr.isupper()]
    for attr in attrs:
        print(attr, ":", getattr(mod, attr))
