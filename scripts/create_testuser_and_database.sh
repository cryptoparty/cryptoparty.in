echo "create user test with password 'test';" | psql
echo "create database test;" | psql
echo "grant all on database test to test;" | psql
psql -d test -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
psql -d test -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql
echo "grant all on spatial_ref_sys to test;" | psql -d test
echo "grant all on geometry_columns to test;" | psql -d test
