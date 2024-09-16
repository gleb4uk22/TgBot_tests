CREATE OR REPLACE TABLE TgBot_tests.Anatomy_kollok7
(
    num_q Int64	            -- номер вопроса
	, correct boolean	    -- корректный или нет
    , name Varchar2(300)    -- тема вопрос или ответ
    , what VARCHAR2(10)     -- вопрос или ответ
    , num_a Int64           -- номер ответа
)
ENGINE = MergeTree()
ORDER BY num_q