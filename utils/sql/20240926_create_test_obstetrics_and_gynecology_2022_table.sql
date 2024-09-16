CREATE OR REPLACE TABLE TgBot_tests.test_obstetrics_and_gynecology_2022
(
    questionNum			Int64			-- номер вопроса
	, question 			Varchar(1024)	-- вопрос
	, a					Varchar(1024)	-- ответ 1
	, b					Varchar(1024)	-- ответ 2
	, c					Varchar(1024)	-- ответ 3
	, d					Varchar(1024)	-- ответ 4
	
)
ENGINE = MergeTree()
ORDER BY questionNum