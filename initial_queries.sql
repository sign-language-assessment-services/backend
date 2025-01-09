DO $$
DECLARE
    var_bucket_object_id UUID;
    var_multiple_choice_id UUID;
    var_choice_id UUID;
    var_exercise_id UUID;
    var_primer_id UUID;
    var_assessment_id UUID;
    var_submission_id UUID;
    var_user_id UUID;
    var_testfile_number INT;

BEGIN
    -- Insert assessment
    ----------------------------------------------------------------------------------------------
    var_assessment_id := gen_random_uuid();
    INSERT INTO assessments (id, created_at, name)
    VALUES
        (var_assessment_id, now(), 'Initial Queries Test Assessment');

    -- Insert bucket objects (16 choices, 2 primers and 2 exercises)
    ----------------------------------------------------------------------------------------------
    FOR bucket_number IN 1..20 LOOP
        var_bucket_object_id := gen_random_uuid();

        INSERT INTO bucket_objects (id, created_at, bucket, key, media_type)
        VALUES
            (var_bucket_object_id, now(), 'slportal', 'testfile-' || bucket_number || '.mp4', 'VIDEO');
    END LOOP;

    -- Insert 4 multiple choices, each with 4 choices
    ----------------------------------------------------------------------------------------------
    FOR mc_number in 1..4 LOOP
        var_multiple_choice_id := gen_random_uuid();

        INSERT INTO multiple_choices (id, created_at)
        VALUES
            (var_multiple_choice_id, now());

        FOR choice_number in 1..4 LOOP
            var_choice_id := gen_random_uuid();
            var_testfile_number := (mc_number - 1) * 4 + choice_number; -- get numbers (1-4, 5-8, 9-12, 13-16)
            SELECT id INTO var_bucket_object_id FROM bucket_objects WHERE key = 'testfile-' || var_testfile_number || '.mp4';

            INSERT INTO choices (id, created_at, bucket_object_id)
            VALUES
                (var_choice_id, now(), var_bucket_object_id);

            INSERT INTO multiple_choices_choices (position, is_correct, choice_id, multiple_choice_id)
            VALUES
                -- For simplicity, only first choice is correct
                (choice_number, CASE WHEN choice_number = 1 THEN true ELSE false END, var_choice_id, var_multiple_choice_id);
        END LOOP;
    END LOOP;

    -- Insert primers (with testfile-{17..18}.mp4)
    ----------------------------------------------------------------------------------------------
    FOR primer_number in 1..2 LOOP
        var_primer_id := gen_random_uuid();
        var_testfile_number := 16 + primer_number;
        SELECT id INTO var_bucket_object_id FROM bucket_objects WHERE key = 'testfile-' || var_testfile_number || '.mp4';

        INSERT INTO tasks (id, created_at, task_type)
        VALUES
            (var_primer_id, now(), 'primer');

        INSERT INTO primers (id, bucket_object_id)
        VALUES
            (var_primer_id, var_bucket_object_id);

        INSERT INTO assessments_tasks (position, assessment_id, task_id)
        VALUES
            (primer_number, var_assessment_id, var_primer_id);
    END LOOP;

    -- Insert exercises (with testfile-{19..20}.mp4)
    ----------------------------------------------------------------------------------------------
    FOR exercise_number in 1..2 LOOP
        var_exercise_id := gen_random_uuid();
        var_testfile_number := 18 + exercise_number;
        SELECT id INTO var_bucket_object_id FROM bucket_objects WHERE key = 'testfile-' || var_testfile_number || '.mp4';
        SELECT id INTO var_multiple_choice_id FROM multiple_choices ORDER BY id LIMIT 1 OFFSET exercise_number;

        INSERT INTO tasks (id, created_at, task_type)
        VALUES
            (var_exercise_id, now(), 'exercise');

        INSERT INTO exercises (points, id, bucket_object_id, multiple_choice_id)
        VALUES
            (1, var_exercise_id, var_bucket_object_id, var_multiple_choice_id);

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

        SELECT multiple_choice_id INTO var_multiple_choice_id FROM exercises WHERE id = var_exercise_id LIMIT 1;
        SELECT choice_id INTO var_choice_id FROM multiple_choices_choices WHERE multiple_choice_id = var_multiple_choice_id ORDER BY random() LIMIT 1;

        RAISE NOTICE 'submission id: %', var_submission_id;
        RAISE NOTICE 'user_id: %', var_user_id;
        RAISE NOTICE 'assessment_id: %', var_assessment_id;
        RAISE NOTICE 'exercise id: %', var_exercise_id;
        RAISE NOTICE 'multiple choice id: %', var_multiple_choice_id;
        RAISE NOTICE 'choice id: %', var_choice_id;

        INSERT INTO submissions (id, created_at, user_id, assessment_id, exercise_id, multiple_choice_id, choices)
        VALUES
            (var_submission_id, now(), var_user_id, var_assessment_id, var_exercise_id, var_multiple_choice_id, ARRAY[var_choice_id]);
    END LOOP;

END $$;
