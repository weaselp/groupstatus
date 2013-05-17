
CREATE TABLE config (
    name        TEXT    PRIMARY KEY,
    value       TEXT
);
INSERT INTO config VALUES ('db_revision', '1');
GRANT SELECT ON config TO public;


CREATE TABLE message (
    message_id  SERIAL  PRIMARY KEY,
    ts          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    channel     TEXT NOT NULL,
    person      TEXT NOT NULL,
    message     TEXT NOT NULL
);
CREATE INDEX message_ts_idx ON message(ts);
CREATE INDEX message_channel_idx ON message(channel);
CREATE INDEX message_person_idx ON message(person);
GRANT SELECT ON message TO public;

CREATE TABLE tag (
    tag_id      SERIAL  PRIMARY KEY,
    tag         TEXT NOT NULL,
    UNIQUE(tag)
);
CREATE INDEX tag_tag_idx ON tag(tag);
GRANT SELECT ON tag TO public;

CREATE TABLE message_tag (
    message_id INTEGER NOT NULL REFERENCES message(message_id),
    tag_id     INTEGER NOT NULL REFERENCES tag(tag_id),
    PRIMARY KEY (message_id, tag_id)
);
CREATE INDEX message_tag_message_id ON message_tag(message_id);
CREATE INDEX message_tag_tag_id ON message_tag(tag_id);
GRANT SELECT ON message_tag TO public;
