DROP DATABASE IF EXISTS test_sql_dmrf;
CREATE DATABASE test_sql_dmrf;

USE test_sql_dmrf;

DROP TABLE IF EXISTS table_cards_transfer;
CREATE TABLE table_cards_transfer (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  old_card VARCHAR(3),
  new_card VARCHAR(3),
  dt DATE,
  PRIMARY KEY (id),
  UNIQUE KEY (id)
) ENGINE=InnoDB;

LOCK TABLES table_cards_transfer WRITE;
INSERT INTO table_cards_transfer (old_card, new_card, dt)
VALUES
	('111','555','2020-01-09'),
	('222','223','2020-02-10'),
	('333','334','2020-03-11'),
	('444','222','2020-04-12'),
	('555','666','2020-05-12'),
	('666','777','2020-06-13'),
	('777','888','2020-07-14'),
	('888','000','2020-08-15'),
	('999','333','2020-09-16'),
	('223','111','2020-10-16')
UNLOCK TABLES;

SELECT * FROM table_cards_transfer;

DELIMITER //

DROP PROCEDURE IF EXISTS test_procedure//
CREATE PROCEDURE test_procedure (param1 INT, param2 INT)
BEGIN  
	
	SET @transfers = 0; 
	SET @old_card = param1;
    SET @new_card = param2;

	WITH RECURSIVE cte AS
	(
	  SELECT old_card, new_card, dt, 1 AS transfers
	  FROM table_cards_transfer
	  WHERE old_card = (SELECT old_card FROM table_cards_transfer LIMIT 1)
	  UNION ALL
	  SELECT c.old_card, c.new_card, cte.dt, cte.transfers+1
	  FROM table_cards_transfer c JOIN cte ON
	    cte.new_card=c.old_card
	)
	SELECT dt, transfers
	INTO
	@dt, @transfers
	FROM cte WHERE new_card = @old_card;
	
	IF (@transfers < 5) THEN
		IF (@new_card NOT IN (SELECT new_card FROM table_cards_transfer)
			OR @new_card IN (SELECT old_card FROM table_cards_transfer))
			THEN SELECT 'operation approved' AS note;
		ELSE
 			SELECT CONCAT('card ', @new_card, ' is already use') AS note;
 		END IF;
	ELSE
		SELECT CONCAT('operation denied until: ', DATE_ADD(@dt, INTERVAL 1 YEAR)) AS note;
	END IF;

END // 

DELIMITER ;


CALL test_procedure('000', '222');
CALL test_procedure('666', '999');
CALL test_procedure('555', '334');
