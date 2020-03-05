DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Inventory;


CREATE Table Players(
	ID	INTEGER PRIMARY KEY	AUTOINCREMENT,
	Username	nvarchar(10)	NOT NULL,
	Password	nvarchar(15)	NOT NULL,
	x	int	DEFAULT 0,
	y	int	DEFAULT 0
);

CREATE Table Inventory(
	ID	INTEGER PRIMARY KEY	AUTOINCREMENT,
	PlayerID INTEGER,
	item0 INTEGER DEFAULT NULL,
	item1 INTEGER DEFAULT NULL,
	item2 INTEGER DEFAULT NULL,
	FOREIGN KEY(PlayerID) REFERENCES Players(PlayerID)
);


insert into Players(ID,Username,Password) values(NULL, "fred", "123");
insert into Inventory(ID, PlayerID) values(NULL, 1);

insert into Players(ID,Username,Password) values(NULL, "bob", "123");
insert into Inventory(ID, PlayerID) values(NULL, 2);