CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    damage_dealt INT DEFAULT 0,
    spells_cast INT DEFAULT 0
);

CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE
);