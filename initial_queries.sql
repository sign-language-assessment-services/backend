DO $$
DECLARE
    var_bucket_id UUID;
    var_text_id UUID;
    var_multiple_choice_id UUID;
    var_choice_id UUID;
    var_exercise_id UUID;
    var_primer_id UUID;
    var_assessment_id UUID;
    var_submission_id UUID;
    var_multiple_choice_submission_id UUID;
    var_user_id UUID;
    var_testfile_number INT;

BEGIN
    -- Insert assessment
    ----------------------------------------------------------------------------------------------
    var_assessment_id := gen_random_uuid();
    INSERT INTO assessments (id, created_at, name)
    VALUES
        (var_assessment_id, now(), 'Initial Queries Test Assessment');

    -- Insert buckets (16 choices, 2 primers and 2 exercises)
    ----------------------------------------------------------------------------------------------
    FOR bucket_number IN 1..20 LOOP
        var_bucket_id := gen_random_uuid();

        INSERT INTO buckets (id, created_at, bucket, key, content_type)
        VALUES
            (var_bucket_id, now(), 'slportal', 'testfile-' || bucket_number || '.mp4', 'VIDEO');
    END LOOP;

    -- Insert texts (not used, just for completeness)
    ----------------------------------------------------------------------------------------------
    FOR text_number IN 1..10000 LOOP
        var_text_id := gen_random_uuid();

        INSERT INTO texts (id, created_at, text)
        VALUES
            (var_text_id, now(), 'Test text ' || text_number);
    END LOOP;

    -- Insert multiple choices with choices
    ----------------------------------------------------------------------------------------------
    FOR mc_number in 1..4 LOOP
        var_multiple_choice_id := gen_random_uuid();

        INSERT INTO multiple_choices (id, created_at, random)
        VALUES
            (var_multiple_choice_id, now(), FALSE);

        FOR choice_number in 1..4 LOOP
            var_choice_id := gen_random_uuid();
            var_testfile_number := (mc_number - 1) * 4 + choice_number; -- get numbers (1-4, 5-8, 9-12, 13-16)
            SELECT id INTO var_bucket_id FROM buckets WHERE key = 'testfile-' || var_testfile_number || '.mp4';

            INSERT INTO choices (id, created_at, is_correct, position, bucket_id, text_id, multiple_choice_id)
            VALUES
                -- each first choice is correct, others are false
                (var_choice_id, now(), CASE WHEN var_testfile_number = 1 THEN true ELSE false END, choice_number, var_bucket_id, null, var_multiple_choice_id);
        END LOOP;
    END LOOP;

    -- Insert primers (with testfile-{17..18}.mp4)
    ----------------------------------------------------------------------------------------------
    FOR primer_number in 1..2 LOOP
        var_primer_id := gen_random_uuid();
        var_testfile_number := 16 + primer_number;
        SELECT id INTO var_bucket_id FROM buckets WHERE key = 'testfile-' || var_testfile_number || '.mp4';

        INSERT INTO tasks (id, created_at, task_type)
        VALUES
            (var_primer_id, now(), 'primer');

        INSERT INTO primers (id, bucket_id, text_id)
        VALUES
            (var_primer_id, var_bucket_id, null);

        INSERT INTO assessments_tasks (position, assessment_id, task_id)
        VALUES
            (primer_number, var_assessment_id, var_primer_id);
    END LOOP;

    -- Insert exercises (with testfile-{19..20}.mp4)
    ----------------------------------------------------------------------------------------------
    FOR exercise_number in 1..2 LOOP
        var_exercise_id := gen_random_uuid();
        var_testfile_number := 18 + exercise_number;
        SELECT id INTO var_bucket_id FROM buckets WHERE key = 'testfile-' || var_testfile_number || '.mp4';
        SELECT id INTO var_multiple_choice_id FROM multiple_choices ORDER BY id LIMIT 1 OFFSET exercise_number;

        INSERT INTO tasks (id, created_at, task_type)
        VALUES
            (var_exercise_id, now(), 'exercise');

        INSERT INTO exercises (id, bucket_id, multiple_choice_id, text_id)
        VALUES
            (var_exercise_id, var_bucket_id, var_multiple_choice_id, null);

        INSERT INTO assessments_tasks (position, assessment_id, task_id)
        VALUES
            -- offset 2 = number of primers before exercise
            (exercise_number + 2, var_assessment_id, var_exercise_id);
    END LOOP;

    -- Insert (multiple choice) submissions for one user for all exercises
    ----------------------------------------------------------------------------------------------
    var_user_id := gen_random_uuid();
    FOR var_exercise_id IN SELECT id from exercises LOOP
        var_submission_id := gen_random_uuid();
        var_multiple_choice_submission_id := gen_random_uuid();
        SELECT var_multiple_choice_id INTO var_multiple_choice_id FROM exercises WHERE id = var_exercise_id LIMIT 1;
        SELECT id INTO var_choice_id FROM choices WHERE multiple_choice_id = var_multiple_choice_id ORDER BY random() LIMIT 1;

        RAISE NOTICE 'exercise id: %', var_exercise_id;
        RAISE NOTICE 'submission id: %', var_submission_id;
        RAISE NOTICE 'multiple choice submission id: %', var_multiple_choice_submission_id;
        RAISE NOTICE 'multiple choice id: %', var_multiple_choice_id;
        RAISE NOTICE 'choice id: %', var_choice_id;

        INSERT INTO submissions (id, created_at, submission_type, user_name, exercise_id)
        VALUES
            (var_submission_id, now(), 'multiple_choice_submission', var_user_id, var_exercise_id);

        INSERT INTO multiple_choice_submissions (id, multiple_choice_id)
        VALUES
            (var_submission_id, var_multiple_choice_id);

        INSERT INTO multiple_choice_submissions_choices (submission_id, choice_id)
        VALUES
            (var_submission_id, var_choice_id);
    END LOOP;

END $$;
