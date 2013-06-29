echo "create user test with password 'test';" | psql
echo "create database test;" | psql
echo "grant all on database test to test;" | psql
psql -d test -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d test -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
echo "grant all on spatial_ref_sys to test;" | psql -d test
echo "grant all on geometry_columns to test;" | psql -d test
