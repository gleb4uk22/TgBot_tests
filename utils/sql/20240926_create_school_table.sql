CREATE OR REPLACE TABLE school
(
    a Int64	-- множ a
	, b Int64	-- множ b
    , c Int64  -- результат c
    , wrong1 Int64  -- некор 1
    , wrong2 Int64  -- некор 2
    , wrong3 Int64  -- некор 3
    , id Int64 -- id
)
ENGINE = MergeTree()
ORDER BY id
;

INSERT INTO school (a,b,c,id,wrong1,wrong2,wrong3)
WITH
    arrayMap(i -> (0 + i)),
    range(11) AS Num,
    a AS
    (
        SELECT arrayJoin(Num) AS n
    )
SELECT
    *,
    rowNumberInAllBlocks() + 1 AS id,
    z - 1,
    z - 2,
    z - 3
FROM
(
    SELECT
        a.n AS x,
        b.n AS y,
        a.n * b.n AS z
    FROM a
    CROSS JOIN a AS b
)