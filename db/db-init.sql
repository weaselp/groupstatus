
REVOKE ALL ON DATABASE "groupstatus" FROM PUBLIC;
GRANT ALL ON DATABASE "groupstatus" TO "groupstatus";
GRANT CONNECT, TEMPORARY ON DATABASE "groupstatus" TO PUBLIC;

REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO "groupstatus";
GRANT USAGE ON SCHEMA public TO PUBLIC;

