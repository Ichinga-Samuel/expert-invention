from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aggregators` (
    `name` VARCHAR(255) NOT NULL,
    `username` VARCHAR(255) NOT NULL  PRIMARY KEY,
    `email` VARCHAR(255)   DEFAULT '',
    `password` VARCHAR(255) NOT NULL,
    `mobile` BIGINT NOT NULL,
    `target` DOUBLE NOT NULL,
    `token` LONGTEXT,
    UNIQUE KEY `uid_aggregators_usernam_58d601` (`username`, `mobile`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `agents` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `agent_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `mobile` BIGINT NOT NULL,
    `aggregator_id` VARCHAR(255) NOT NULL,
    CONSTRAINT `fk_agents_aggregat_d086c13f` FOREIGN KEY (`aggregator_id`) REFERENCES `aggregators` (`username`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
