--liquibase formatted sql

--changeset vivavi:1 labels:init
--comment: create table wallet
CREATE TABLE IF NOT EXISTS wallet (
  id UUID NOT NULL,
  balance DECIMAL NOT NULL DEFAULT '0',
  PRIMARY KEY (id)
);
--rollback DROP TABLE wallet;


--changeset vivavi:2 labels:index
--comment: create index
CREATE UNIQUE INDEX wallet_id_index
ON wallet (id);
--rollback DROP INDEX wallet_id_index;